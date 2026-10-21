# --------------------------------------------------------------------
# Copyright (C) 2024, 2026 hyperimpose.org
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
from urllib.parse import quote_plus
from typing import TypedDict

import html5lib

from .. import shared


logger = logging.getLogger(__name__)


# ====================================================================
# Search
# ====================================================================

class Result(TypedDict):
    link: str
    title: str
    description: str


async def search(q: str) -> list[Result]:
    headers = {"User-Agent": "w3m"}  # Helps avoid captcha

    # Adding this 'magic' string makes duckduckgo return output that is
    # easier to extract information from.
    magic = "&kl=wt-wt&kp=-2&kaf=1&kh=1&k1=-1&kd=-1"

    u = f"https://html.duckduckgo.com/html?q={quote_plus(q)}" + magic

    r = await shared.client.get(u, headers=headers)
    if not r.text:
        logger.error("[duckduckgo] Empty response for: %s", q)
        return []

    d = html5lib.parse(r.text, namespaceHTMLElements=False)

    # title = d.find(".//title").text.strip()

    links = []
    for a in d.findall(".//a[@class='result__url']"):
        links.append(a.attrib["href"].strip())

    titles = []
    for h2 in d.findall(".//h2[@class='result__title']"):
        titles.append("".join(h2.itertext()).strip())

    descriptions = []
    for a in d.findall(".//a[@class='result__snippet']"):
        descriptions.append("".join(a.itertext()).strip())

    results = []
    if len(links) == len(titles) == len(descriptions):
        for link, t, c in zip(links, titles, descriptions):
            results.append(Result(link=link, title=t, description=c))
    else:
        logger.error("[duckduckgo] Incomplete results for: %s", q)

    return results
