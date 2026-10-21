# --------------------------------------------------------------------
# Copyright (C) 2023-2024,2026 hyperimpose.org
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
from urllib.parse import urlsplit

import html5lib

from titles.common import Title
from .. import shared


# ====================================================================
# Thread
# ====================================================================

THREAD = ["lainchan.org/*/res/*", "*.lainchan.org/*/res/*"]


async def thread(url: str, **_kwargs) -> Title | None:
    # Skip moderation paths
    if urlsplit(url).path.startswith("/mod.php"):
        return None

    # Extract info from the URL
    board = url.split("lainchan.org/")[1].split("/", 1)[0]

    url_l = url.rsplit("#", 1)
    if len(url_l) > 0:
        post_no = re.sub(r"\D", "", url_l[-1])  # Remove non digit characters
    else:
        post_no = ""

    # Prepare the JSON URL
    u = url_l[0]
    if u[-5:] == ".html":
        u = u[:-5]

    u = f"{u}.json"

    # HTTP Request
    r = await shared.client.get(u)
    if r.status_code != 200:
        return None

    j = r.json()

    post = j["posts"][0]  # Set the OP as the target post

    # Title
    if "sub" in post:
        title = post["sub"]

    if post_no:
        for i in j["posts"]:
            if int(post_no) == i["no"]:
                post = i
                break

    d = html5lib.parse(post["com"], namespaceHTMLElements=False)
    post_l = ET.tostringlist(d, encoding="unicode", method="text")
    post = " ".join(post_l)[:150] + "..."

    # File count
    files = 0
    for i in j["posts"]:
        if "filename" in i:
            files += 1
        if "extra_files" in i:
            files += len(i["extra_files"])

    # Reply count
    replies = len(j["posts"]) - 1

    # IRC formatted title
    irc = (f"\x0309lainchan\x0F \x0306/{board}/\x0F {title}"
           f" \x02->\x0F \x0302{post}\x0F"
           f" | \x02Replies:\x0F {replies}"
           f" - \x02Files:\x0F {files}")

    return Title(t=title, irc=irc)
