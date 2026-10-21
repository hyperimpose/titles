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

# Try to find a title for the given link using a customized method.
#
# This method is preferable for some links because:
# 1) It may require specialized methods for title extraction.
# 2) We may want to get more than just the title.
# 3) It may be faster to handle the service with a custom mechanism.

import logging
import re
from collections import defaultdict
from functools import cache
from typing import Awaitable, Pattern, Protocol
from urllib.parse import urlsplit

from titles.common import Title
from ..shared import Headers
from . import (
    browser, fourchan, lainchan, toro, x, youtube
)


logger = logging.getLogger(__name__)


# ====================================================================
# Registry / Index
# ====================================================================

class CustomHandler(Protocol):
    def __call__(
            self, url: str, *, headers: Headers
    ) -> Awaitable[Title | None]:
        ...


REGISTRY: list[tuple[list[str], CustomHandler]] = [
    (browser.SITES, browser.handler),
    (fourchan.FILE, fourchan.file),
    (lainchan.THREAD, lainchan.thread),
    (toro.UPLOADS, toro.uploads),
    (x.X, x.handler),
    (youtube.YT, youtube.handler)
]


@cache
def get_index() -> defaultdict[str, list[tuple[Pattern, CustomHandler]]]:
    acc = defaultdict(list)
    for patterns, handler in REGISTRY:
        if isinstance(patterns, str):
            patterns = [patterns]

        for pattern in patterns:
            if not urlsplit(pattern).scheme:
                pattern = "http://" + pattern  # See _re(): Also matches https.
            acc[_key(pattern)].append((_re(pattern), handler))

    logger.debug("[titles] Loaded custom handlers")
    return acc


# ====================================================================
# API
# ====================================================================

async def get(url: str, *, headers={}) -> Title | None:
    for pattern, handler in get_index().get(_key(url), []):
        if pattern.fullmatch(url):
            return await handler(url, headers=headers)

    return None


# ====================================================================
# Helpers
# ====================================================================

def _key(s: str) -> str:
    hostname = urlsplit(s).hostname
    assert hostname is not None
    parts = hostname.lower().split(".")
    # It is NOT https://publicsuffix.org aware.
    return ".".join(parts[-2:])  # E.g.: youtube.com, co.uk


def _re(url: str) -> Pattern:
    """
    Convert URLs with wildcards to a compiled regex.

    The pattern will match both http and https schemes.
    """
    def wildcard(s: str) -> str:
        return re.escape(s).replace(r"\*", ".*")

    o = urlsplit(url)
    userinfo, at, hostport = o.netloc.rpartition("@")

    pattern = (r"(?i:https?)://"
               f"{wildcard(userinfo)}{at}"
               f"(?i:{wildcard(hostport)})"
               f"{wildcard(o.path)}")
    if o.query:
        pattern += rf"\?{wildcard(o.query)}"
    if o.fragment:
        pattern += rf"\#{wildcard(o.fragment)}"

    return re.compile(rf"^{pattern}$")
