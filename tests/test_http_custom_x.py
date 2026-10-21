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


class CustomHTTPX(unittest.TestCase):
    def test_status(self):
        u = "https://twitter.com/Google/status/1224134123519868932"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            t = (
                "A love story about the moments that matter most, told with a"
                " little help from Google."
                " #SuperBowlLIV  pic.twitter.com/JXbcKpGSH5"
                " — Google (@Google) February 3, 2020"
            )
            self.assertEqual(r.json()["t"], t)

    def test_profile(self):
        u = "https://twitter.com/Google"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json()["t"], "Posts by Google")

    def test_photo(self):
        u = "https://x.com/Google/status/1948434032645050665/photo/1"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            self.assertStartsWith(r.json()["t"], "Our latest shopping feature")
