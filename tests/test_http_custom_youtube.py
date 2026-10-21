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


class CustomHttpYouTube(unittest.TestCase):
    def test_homepage(self):
        u = "https://www.youtube.com"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            j = r.json()
            self.assertEqual(j["t"], "YouTube")

    def test_video(self):
        u = "https://www.youtube.com/watch?v=rdwz7QiG0lk"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            j = r.json()
            self.assertEqual(j["t"], "YouTube on the tube! :: YouTube")
            self.assertIsInstance(j["irc"], str)

    def test_m_video(self):
        u = "https://m.youtube.com/watch?v=rdwz7QiG0lk"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            j = r.json()
            self.assertEqual(j["t"], "YouTube on the tube! :: YouTube")
            self.assertIsInstance(j["irc"], str)

    def test_playlist(self):
        u = "https://www.youtube.com/playlist?list=OLAK5uy_nnc_rabu3dWK3t7ECn1GS3y4ShnwMz_sY"  # noqa
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            j = r.json()
            self.assertEqual(j["t"], "The Theory Of")

    def test_channel(self):
        u = "https://www.youtube.com/@YouTube"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            j = r.json()
            self.assertEqual(j["t"], "YouTube - YouTube")

    def test_music_homepage(self):
        u = "https://music.youtube.com"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            j = r.json()
            self.assertEqual(j["t"], "YouTube Music")

    def test_music_playlist(self):
        u = "https://music.youtube.com/playlist?list=RDCLAK5uy_ltlS29HmNHZb3oCsEjfXmZhIGaWpaDZck"  # noqa
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            j = r.json()
            self.assertEqual(j["t"], "'90s Dance")
