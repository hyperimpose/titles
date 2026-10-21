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

import unittest

from starlette.testclient import TestClient
from titles.webserver import app


class CustomHTTPToro(unittest.TestCase):
    def test_vomit(self):
        u = "https://toro.lain.la/u/6IQqTw.png"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            t = ("image/png, 1024x768, Size: 45.61 KB,"
                 " https://toro.lain.la/f/6IQqTw.png")
            self.assertEqual(r.json()["t"], t)
