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


class ExternalHTTPDuckDuckGo(unittest.TestCase):
    def test_search(self):
        with TestClient(app) as client:
            r = client.get("/duckduckgo", params={"q": "irc"})
            self.assertEqual(r.status_code, 200)
            results = r.json()
            self.assertIsInstance(results, list)
            self.assertGreater(len(results), 0)
            self.assertIsInstance(results[0], dict)
            self.assertIsInstance(results[0]["title"], str)
            self.assertIsInstance(results[0]["link"], str)
            self.assertIsInstance(results[0]["description"], str)
