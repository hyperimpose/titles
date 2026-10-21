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

from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route

from titles import as_http, config, explicit
from . import title, duckduckgo, youtube


async def health(request):
    return Response("ok", status_code=200)


routes = [
    Route("/health", health, methods=["GET"]),

    Route("/title", title.get, methods=["GET"]),

    Route("/duckduckgo", duckduckgo.search, methods=["GET"]),
    Route("/youtube/search", youtube.search, methods=["GET"])
]


@asynccontextmanager
async def lifespan(app):
    await as_http.init()
    explicit.init()
    yield
    await as_http.destroy()
    explicit.destroy()


app = Starlette(debug=config.DEBUG, routes=routes, lifespan=lifespan)
