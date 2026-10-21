# --------------------------------------------------------------------
# Copyright (C) 2026 hyperimpose.org
#
# This file is part of titles.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# --------------------------------------------------------------------

import asyncio
import logging
import re
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import cast

from titles.common import cleanup, Title
from titles import config


logger = logging.getLogger(__name__)


try:
    from playwright.async_api import (
        async_playwright,
        Browser, BrowserContext, Error, Playwright, Page
    )
except ImportError:
    _has_playwright = False
    logger.warning("[titles] browser: unavailable")
else:
    _has_playwright = True


# ====================================================================
# Setup
# ====================================================================

BLOCKED_RESOURCES = {
    "image",
    "media",
    "font",
    "stylesheet",
}


@dataclass
class PoolItem:
    context: BrowserContext
    page: Page


class BrowserPool:
    def __init__(self, size: int = 8):
        self.size = size
        self.queue: asyncio.Queue[PoolItem] = asyncio.Queue(maxsize=size)

        self._closed = False

        self.playwright: Playwright | None = None
        self.browser: Browser | None = None

    async def start(self) -> None:
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.firefox.launch(headless=True)

        items = await asyncio.gather(*(self._new() for _ in range(self.size)))
        for item in items:
            await self.queue.put(item)

    async def close(self):
        self._closed = True

        while not self.queue.empty():
            item = await self.queue.get()
            try:
                await item.context.close()
            except Error:
                pass

        if self.browser is not None:
            await self.browser.close()
        if self.playwright is not None:
            await self.playwright.stop()

    async def _new(self) -> PoolItem:
        assert self.browser is not None

        context = await self.browser.new_context(
            locale=config.lang,
            java_script_enabled=True,
            service_workers="block",
        )

        async def route_handler(route):
            if route.request.resource_type in BLOCKED_RESOURCES:
                await route.abort()
            else:
                await route.continue_()

        await context.route("**/*", route_handler)
        page = await context.new_page()
        return PoolItem(context=context, page=page)

    @asynccontextmanager
    async def get_page(self):
        if self._closed:
            raise RuntimeError("Pool's closed")

        item = await self.queue.get()

        try:
            yield item.page
        finally:
            await item.context.close()
            if not self._closed:
                await self.queue.put(await self._new())


# Initialization =====================================================

_pool = cast(BrowserPool, None)


async def init() -> None:
    if not _has_playwright:
        return None

    global _pool
    _pool = BrowserPool(size=8)
    await _pool.start()


async def destroy() -> None:
    if not _pool:
        return None

    await _pool.close()


# ====================================================================
# API
# ====================================================================

async def get_title(url: str) -> Title | None:
    if not _has_playwright:
        return None

    async with _pool.get_page() as page:
        try:
            await page.goto(url, wait_until="commit", timeout=5000)

            if title := cleanup(await page.title()):
                return Title(t=title)

            await page.wait_for_load_state("domcontentloaded", timeout=5000)
            if title := cleanup(await page.title()):
                return Title(t=title)

            try:
                await page.wait_for_selector("title", timeout=3500)
                if title := cleanup(await page.title()):
                    return Title(t=title)
            except Error:
                pass

            await page.wait_for_load_state("networkidle", timeout=10_000)
            if title := await _content_title(page):
                return Title(t=title)

            return None
        except Exception:
            logger.exception("[browser] Error getting title for %s", url)

    return None


# ====================================================================
# Helpers
# ====================================================================

async def _content_title(page: Page) -> str:
    if t := cleanup(await page.title()):
        return t

    h1 = page.locator("h1").first
    if (await h1.count()) and (t := cleanup(await h1.inner_text())):
        return t

    if text := await page.locator("body").inner_text():
        text = re.split(r'[\n.!?]+', text, maxsplit=1)[0]
        return cleanup(text)[:100]

    return ""
