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


class CustomHTTPLainchan(unittest.TestCase):
    def test_thread(self):
        u = "https://lainchan.org/%CE%BB/res/1.html"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json()["t"], "The Sticky: /λ/ 2.0")
            irc = (
                "\x0309lainchan\x0f \x0306/%CE%BB/\x0f The Sticky: /λ/ 2.0"
                " \x02->\x0f \x0302This is new /λ/, also addressable as"
                " /lambda/, the programming board.  The intent is that this"
                " board will be used to share and discuss programs that"
                " h...\x0f | \x02Replies:\x0f 0 - \x02Files:\x0f 1"
            )
            self.assertEqual(r.json()["irc"], irc)

    def test_mod_thread(self):
        u = "https://lainchan.org/mod.php?/%CE%A9/res/73638.html#76881"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json()["t"], "Login")
