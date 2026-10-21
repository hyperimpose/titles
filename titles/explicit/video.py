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
import subprocess
import tempfile
from pathlib import Path

from .image_safety_classifier_xs import score_image


logger = logging.getLogger(__name__)


try:
    a = subprocess.run(["ffmpeg", "-version"], capture_output=True)
    b = subprocess.run(["ffprobe", "-version"], capture_output=True)
    _has_ffmpeg = (a.returncode == 0) and (b.returncode == 0)
except FileNotFoundError:
    _has_ffmpeg = False
finally:
    if not _has_ffmpeg:
        logger.warning("[titles/explicit] ffmpeg: unavailable")


async def score_video(inpath: str | Path, duration=0) -> float:
    if not _has_ffmpeg:
        logger.warning("ffmpeg: unavailable. Returning 0.0")
        return 0.0

    if duration:
        duration = duration / 1000  # duration is in milliseconds
    else:
        duration = _video_duration(inpath)

    times = [
        duration * 0.5,
        duration * 0.75
    ]
    acc = [0.0]

    # We need to add a suffix so that FFmpeg knows what format to output
    with tempfile.NamedTemporaryFile(suffix=".png") as outfp:
        for time in times:
            if _video_frame(str(inpath), outfp.name, time):
                return max(acc)  # stop on error
            acc.append(await score_image(outfp.name))

    return max(acc)


def _video_duration(path: str | Path) -> float:
    r = subprocess.run(
        ["ffprobe",
         "-v", "error",
         "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1",
         path],
        capture_output=True,
        text=True
    )
    return float(r.stdout.strip())


def _video_frame(inp: str, outp: str, at: int | float) -> int:
    r = subprocess.run(
        ["ffmpeg",
         "-y",  # automatically overwrite output
         "-hide_banner", "-loglevel", "warning",
         "-ss", str(at),  # -ss before the input is faster
         "-i", inp,
         "-frames:v", "1",
         "-update", "1",  # Only one image
         outp],
        capture_output=True
    )
    return r.returncode  # non-zero means error
