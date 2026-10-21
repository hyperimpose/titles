import json
import logging
import re
from collections import defaultdict
from typing import Pattern
from urllib.parse import urlsplit

import niquests
from async_lru import alru_cache

from titles import config


logger = logging.getLogger(__name__)


async def get_providers():
    try:
        async with niquests.AsyncSession() as client:
            r = await client.get("https://oembed.com/providers.json")
            r.raise_for_status()
            return r.json()
    except Exception:
        logger.exception("[titles] Failed to fetch oEmbed providers."
                         " Using local copy.")

    path = config.PROJECT_ROOT / "as_http" / "oembed" / "providers.json"
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


@alru_cache(maxsize=1, ttl=60*60*24*14)  # 14 days
async def get_index():
    acc = defaultdict(list)
    for provider in await get_providers():
        for endpoint in provider.get("endpoints", []):
            for scheme in endpoint.get("schemes", []):
                acc[_key(scheme)].append((_re(scheme), endpoint["url"]))

    logger.info("[titles] Updated oEmbed index")
    return acc


async def get_endpoint(url: str):
    candidates = (await get_index()).get(_key(url), ())
    for pattern, endpoint_url in candidates:
        if pattern.fullmatch(url):
            return endpoint_url

    return None


# ====================================================================
# Helpers
# ====================================================================

def _key(s: str):
    o = urlsplit(s)

    # URL scheme only
    if not o.hostname:
        return o.scheme.lower()  # E.g. spotify:*

    # URL hostname
    parts = o.hostname.lower().split(".")
    return ".".join(parts[-2:])  # E.g.: youtube.com, co.uk


def _re(scheme: str) -> Pattern:
    """Convert oEmbed schemes to compiled regex."""
    def wildcard(s: str):
        return re.escape(s).replace(r"\*", ".*")

    o = urlsplit(scheme)

    pattern = rf"(?i:{wildcard(o.scheme)}):"

    if o.netloc:
        userinfo, at, hostport = o.netloc.rpartition("@")
        pattern += rf"//{wildcard(userinfo)}{at}(?i:{wildcard(hostport)})"

    pattern += wildcard(o.path)

    if o.query:
        pattern += rf"\?{wildcard(o.query)}"
    if o.fragment:
        pattern += rf"\#{wildcard(o.fragment)}"

    return re.compile(rf"^{pattern}$")
