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

from titles import config
from titles.webserver import app


class CustomHTTPExplicit(unittest.TestCase):
    def setUp(self):
        self.original_max_filesize = config.max_filesize
        config.max_filesize = 1_048_576  # 1M

    def tearDown(self):
        config.max_filesize = self.original_max_filesize

    def test_image(self):
        u = "https://pomf2.lain.la/f/56spi9wd.jpg"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            self.assertGreater(r.json()["explicit"], 0.0)

    def test_video(self):
        u = "https://pomf2.lain.la/f/m4itn25e.mp4"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            self.assertGreater(r.json()["explicit"], 0.0)
