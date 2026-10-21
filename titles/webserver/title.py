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

from urllib.parse import urlsplit

import msgspec
from starlette.responses import JSONResponse, Response

from titles import as_http
from titles.common import Title
from titles.as_http import oembed


class Get(msgspec.Struct):
    u: str
    lang: str = ""


async def get(request):
    # NOTE: consider using a TypedDict for validation after Python 3.15
    #       adds the closed=True option.
    try:
        q = msgspec.convert(dict(request.query_params), type=Get)
    except msgspec.ValidationError as e:
        return Response(str(e), status_code=400)

    match urlsplit(q.u).scheme:
        case "http" | "https":
            t = await as_http.get(q.u, lang=q.lang)
        case _:  # oEmbed providers may include URL scheme patterns.
            t = await oembed.get_title(q.u)

    if not t:
        return JSONResponse(Title(t="Not Found"), status_code=404)

    return JSONResponse(t)
