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
import tempfile

from titles import config
from titles.common import convert_time, Title
from .. import fallback, hparser, shared

logger = logging.getLogger(__name__)

try:
    from pymediainfo import MediaInfo  # type: ignore
except ImportError:
    _has_mediainfo = False
    logger.warning("[titles] video: unavailable")
else:
    _has_mediainfo = True


async def handle(r) -> Title:
    if not _has_mediainfo:
        return await fallback.handle(r)

    try:
        length = int(r.headers.get("content-length", None))
    except TypeError:
        length = None

    if (not length) or (length > config.max_filesize):
        return await fallback.handle(r)

    with tempfile.NamedTemporaryFile() as fp:
        filesize = 0
        async for chunk in await r.iter_content():
            filesize += len(chunk)
            if filesize >= config.max_filesize:
                return await fallback.handle(r)
            fp.write(chunk)

        fp.seek(0)
        title, duration, width, height = get_mediainfo(fp.name)

        fp.seek(0)
        explicit = await shared.get_explicit(r, fp.name, duration=duration)

    duration = convert_time(duration)
    name = hparser.filename(r.headers)
    size = hparser.filesize(r.headers)
    mt = hparser.mimetype(r.headers)

    t = f"{title} ({duration}), {mt}, {name}, {width}x{height}, Size: {size}"
    t = t.replace("None ", "")  # No title
    t = t.replace("None, ", "")  # No name

    return Title(t=t, explicit=explicit)


def get_mediainfo(path: str):
    title = None
    duration = None
    width = None
    height = None

    mediainfo = MediaInfo.parse(path)
    for track in mediainfo.tracks:
        if not title:
            title = track.title or track.movie_name or track.track_name
        if not width:
            width = track.width
        if not height:
            height = track.height
        if not duration:
            try:
                duration = int(track.duration)
            except TypeError:
                duration = None

    return title, duration, width, height
