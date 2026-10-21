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

from typing import cast

import niquests

from titles import explicit
from . import browser, hparser


# ====================================================================
# Initialization
# ====================================================================

client = cast(niquests.AsyncSession, None)


async def init() -> None:
    global client
    client = niquests.AsyncSession()

    await browser.init()


async def destroy() -> None:
    await client.close()
    await browser.destroy()


# ====================================================================
# Types
# ====================================================================

Headers = dict[str, str]


# ====================================================================
# Explicit
# ====================================================================

async def get_explicit(r, path="", duration=0) -> float:
    if r.headers.get("rating", "") == "RTA-5042-1996-1400-1577-RTA":
        return 1.0

    if not path:
        return 0.0

    mimetype = hparser.mimetype(r.headers)
    if "image/" in mimetype:
        return await explicit.score_image(path)
    elif "video/" in mimetype:
        return await explicit.score_video(path, duration=duration)

    return 0.0
