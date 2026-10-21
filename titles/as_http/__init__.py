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

from titles import config
from titles.common import Title
from . import custom, default, shared, oembed


# ====================================================================
# API
# ====================================================================

async def init() -> None:
    await shared.init()


async def destroy() -> None:
    await shared.destroy()


async def get(url: str, *, lang="") -> Title | None:
    headers = {
        "Accept-Language": lang or config.lang,
        "User-Agent": config.http_useragent
    }
    return (
        await custom.get(url, headers=headers)
        or await oembed.get_title(url)
        or await default.get(url, headers=headers)
    )
