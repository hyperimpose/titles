# --------------------------------------------------------------------
# Copyright (C) 2023-2024, 2026 hyperimpose.org
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
from titles.common import convert_size, Title
from .. import fallback, hparser, shared

logger = logging.getLogger(__name__)

try:
    import pymupdf  # type: ignore
except ImportError:
    _has_pymupdf = False
    logger.warning("[titles] mupdf: unavailable")
else:
    _has_pymupdf = True


MIME_TO_TYPE = {
    "application/pdf": "pdf",
    "application/vnd.ms-xpsdocument": "xps",
    "application/oxps": "oxps",
    "application/epub+zip": "epub",
    "application/x-mobipocket-ebook": "mobi",
    "image/svg+xml": "svg"
}


async def handle(r) -> Title:
    if not _has_pymupdf:
        return await fallback.handle(r)

    length = r.headers.get("content-length", None)
    if not length:
        return await fallback.handle(r)

    try:
        length = int(length)
    except ValueError:
        return await fallback.handle(r)

    if length > config.max_filesize:
        return await fallback.handle(r)

    mimetype = hparser.mimetype(r.headers)
    assert mimetype is not None  # Mimetype ensured by the caller (default.py)
    filetype = MIME_TO_TYPE[mimetype]

    with tempfile.NamedTemporaryFile() as fp:
        filesize = 0
        async for chunk in await r.iter_content():
            filesize += len(chunk)
            if filesize >= config.max_filesize:
                return await fallback.handle(r)
            fp.write(chunk)

        fp.seek(0)

        with pymupdf.open(fp.name, filetype=filetype) as doc:
            if doc.metadata and doc.metadata["title"]:
                title = doc.metadata["title"]
            else:
                for page in doc:
                    title = page.get_text()[:30]
                    if title:
                        title = title.split("\n", 1)[0]
                        title = title.strip().replace("\r", "")
                        break

            # Prepare the "t" string
            parts = [title]
            if doc.page_count:
                parts.append(f"Pages: {doc.page_count}")
            parts.append(mimetype)
            size = convert_size(length)
            parts.append(f"Size: {size}")

            return Title(
                t=", ".join(parts),
                explicit=await shared.get_explicit(r)
            )
