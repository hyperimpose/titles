# --------------------------------------------------------------------
# Copyright (C) 2023-2026 hyperimpose.org
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
import xml.etree.ElementTree as ET

import html5lib

from titles.common import Title
from .. import oembed


X = ["x.com/*", "*.x.com/*", "twitter.com/*", "*.twitter.com/*"]


async def handler(url: str, **_kwargs) -> Title | None:
    # For tweets remove everything after the X ID, so the oembed API works
    # IDs are integers according to https://docs.x.com/fundamentals/x-ids
    url = re.sub(r'(/status/\d+).*', r'\1', url)

    result = await oembed.get(url)
    if not result:
        return None

    html = result.get("html")
    if not html:
        return None

    d = html5lib.parse(html, namespaceHTMLElements=False)
    text_l = ET.tostringlist(d, encoding="unicode", method="text")
    text_l = [x.strip() for x in text_l]
    text = " ".join(text_l).strip()

    return Title(t=text, irc=f"\x0300,01𝕏\x0F: {text}")
