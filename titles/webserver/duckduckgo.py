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

import msgspec
from starlette.responses import JSONResponse, Response

from titles.as_http.external import duckduckgo


class Search(msgspec.Struct):
    q: str


async def search(request):
    try:
        q = msgspec.convert(dict(request.query_params), type=Search)
    except msgspec.ValidationError as e:
        return Response(str(e), status_code=400)

    return JSONResponse(await duckduckgo.search(q.q))
