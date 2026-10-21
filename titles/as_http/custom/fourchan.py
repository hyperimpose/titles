# --------------------------------------------------------------------
# Copyright (C) 2023,2026 hyperimpose.org
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

import re

from async_lru import alru_cache

from titles.common import Title
from .. import default, shared


# ====================================================================
# File
# ====================================================================

FILE = ["https://i.4cdn.org/*", "https://is2.4chan.org/*"]

I_4CDN_BOARD = re.compile(r"i.4cdn.org/+([^/]*)")
IS2_4CHAN_BOARD = re.compile(r"is2.4chan.org/+([^/]*)")


async def file(url: str, *, headers={}) -> Title | None:
    match = re.search(I_4CDN_BOARD, url) or re.search(IS2_4CHAN_BOARD, url)
    if not match:
        return None

    board = match.group(1)
    if not board:
        return None

    result = await default.get(url, headers=headers)
    if result and not (await is_worksafe(board)):
        result["explicit"] = 1.0

    return result


# ====================================================================
# Helpers
# ====================================================================

async def is_worksafe(board):
    board = board.lower()

    for i in await get_boards():
        if i["board"] == board:
            return i["ws_board"] == 1

    return None


@alru_cache(maxsize=1, ttl=60*60*24*14)  # 14 days
async def get_boards():
    global BOARDS

    boards_url = "https://a.4cdn.org/boards.json"

    r = await shared.client.get(boards_url)
    j = r.json()

    BOARDS = j["boards"]
