# https://oembed.com

import logging
import xml.etree.ElementTree as ET

from titles.common import Title
from .. import shared
from . import index


logger = logging.getLogger(__name__)


async def get_title(url: str) -> Title | None:
    r = await get(url)
    if not r:
        return None

    t = ""
    cs: list[str] = [x for x in (r.get("title"), r.get("author_name")) if x]
    if cs:
        if r.get("type") in ("photo", "video"):
            t = f"[{r.get('type')}] "
        t += " :: ".join(cs)

    return Title(t=t)


async def get(url: str) -> dict | None:
    try:
        return await _get(url)
    except Exception:
        logger.exception("[titles] oEmbed error")
        return None


async def _get(url: str) -> dict | None:
    endpoint = await index.get_endpoint(url)
    if not endpoint:
        return None

    r = await shared.client.get(endpoint, params={"url": url})
    r.raise_for_status()

    if "xml" in r.headers.get("Content-Type", "").lower():
        if not r.text:
            return None
        root = ET.fromstring(r.text)
        return {child.tag: child.text for child in root}

    return r.json()
