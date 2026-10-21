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

import json
import logging
from typing import TypedDict

from titles import config
from .. import shared


logger = logging.getLogger(__name__)


# ====================================================================
# Search
# ====================================================================

class Result(TypedDict):
    short_url: str
    name: str
    date: str
    views: str
    channel: str
    duration: str
    yt_id: str


async def search(q: str, *, lang="") -> list[Result]:
    r = await shared.client.get(
        "https://youtube.com/results", params={"search_query": q},
        headers={
            "Accept-Language": lang or config.lang,
            "User-Agent": config.http_useragent
        }
    )
    if not r.text:
        logger.error("[youtube] Empty response for: %s", q)
        return []

    try:
        st = 'var ytInitialData = '
        st_i = r.text.index(st) + len(st)
    except ValueError:
        st = 'window["ytInitialData"] = '
        st_i = r.text.index(st) + len(st)

    j_data = r.text[st_i:]

    st = '};'
    st_i = j_data.index(st)

    j_data = j_data[:st_i+1]
    j = json.loads(j_data)

    sections = filter(lambda x: "itemSectionRenderer" in x,
                      (j["contents"]
                       ["twoColumnSearchResultsRenderer"]
                       ["primaryContents"]
                       ["sectionListRenderer"]
                       ["contents"]))
    item_lists = map(lambda x: x["itemSectionRenderer"]["contents"], sections)
    items = [i for item_list in item_lists for i in item_list]  # flatten
    videos = filter(lambda x: "videoRenderer" in x, items)  # filter ads/shorts
    results = list(map(lambda x: s_vid_info(x["videoRenderer"]), videos))

    return results


def s_vid_info(v) -> Result:
    yt_id = v["videoId"]
    short_url = f"https://youtu.be/{yt_id}"
    name = v["title"]["runs"][0]["text"]
    # Usually youtube's automated music uploads do not have dates.
    try:
        date = v["publishedTimeText"]["simpleText"]
    except KeyError:
        date = ""
    # Sometimes lives do not have a duration, or a view counter.
    #
    # It has also been observed that sometimes a live will show up as
    # being ongoing in the search (where we get this info from), but
    # when opened it will have ended.
    try:
        duration = v["lengthText"]["simpleText"]
    except KeyError:
        duration = ""
    try:
        views = v["viewCountText"]["simpleText"]
    except KeyError:
        views = ""

    channel = v["ownerText"]["runs"][0]["text"]

    return {
        "short_url": short_url, "name": name, "date": date, "views": views,
        "channel": channel, "duration": duration, "yt_id": yt_id
    }
