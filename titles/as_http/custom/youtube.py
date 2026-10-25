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

import logging

from titles.common import Title
from .. import oembed


logger = logging.getLogger(__name__)


YT = ["youtube.com/*", "*.youtube.com/*", "youtu.be/*"]


async def handler(url: str, **_kwargs) -> Title | None:
    result = await oembed.get(url)
    if not result:
        return None

    title = result["title"]
    channel = result.get("author_name")

    t = title
    if channel:
        t += f" :: {channel}"

    irc = f"\x0300,04 ▶ \x0F: {title}"
    if channel:
        irc += f" \x0315|\x0F \x02Channel\x0F: {channel}"

    return Title(t=t, irc=irc)
