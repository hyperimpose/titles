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

import asyncio
import logging
from pathlib import Path
from typing import cast, BinaryIO


logger = logging.getLogger(__name__)


try:
    from PIL import Image
    import numpy as np
    import onnxruntime as ort  # type: ignore
    from huggingface_hub import hf_hub_download
except ImportError:
    _has_model = False
    logger.warning("[titles] explicit: unavailable")
else:
    _has_model = True


# Initialization =====================================================

session = cast(ort.InferenceSession, None)


def init() -> None:
    if not _has_model:
        return None

    global session
    model_path = hf_hub_download("OwenElliott/image-safety-classifier-xs",
                                 "onnx/image-safety-classifier-xs.onnx")
    session = ort.InferenceSession(model_path)


def destroy() -> None:
    global session
    session = None


# API ================================================================

inference_limit = asyncio.Semaphore(1)


async def score_image(fp: str | Path | BinaryIO) -> float:
    if not session:
        return 0.0

    async with inference_limit:
        return await asyncio.to_thread(_infer, fp)


def _infer(fp: str | Path | BinaryIO) -> float:
    """See: https://huggingface.co/OwenElliott/image-safety-classifier-xs"""
    with Image.open(fp) as img:
        img = img.convert("RGB").resize((224, 224), Image.BILINEAR)
        pixels = np.array(img, dtype=np.float32).transpose(2, 0, 1)[np.newaxis]
        probs = session.run(None, {"image": pixels})[0][0]
        return float(probs[0] + probs[1])  # probs = [NSFL, NSFW, SFW]
