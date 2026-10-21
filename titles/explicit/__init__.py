from pathlib import Path
from typing import BinaryIO

from . import image_safety_classifier_xs, video


def init() -> None:
    image_safety_classifier_xs.init()


def destroy() -> None:
    image_safety_classifier_xs.destroy()


async def score_image(fp: str | Path | BinaryIO) -> float:
    return await image_safety_classifier_xs.score_image(fp)


async def score_video(fp: str | Path, duration=0) -> float:
    return await video.score_video(fp, duration)
