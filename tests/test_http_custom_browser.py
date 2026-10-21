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


class CustomHttpBrowser(unittest.TestCase):
    def test_amazon(self):
        u = "https://www.amazon.com/dp/0500027358"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            t = "A to Z of The Designers Republic: Anderson, Ian: 9780500027356: Amazon.com: Books"  # noqa
            self.assertEqual(r.json()["t"], t)

    def test_chris_siebenmann(self):
        u = "https://utcc.utoronto.ca/~cks"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json()["t"], "Chris Siebenmann")

        u = "https://utcc.utoronto.ca/~cks/space/"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json()["t"], "Chris's Wiki :: FrontPage")

        u = "https://utcc.utoronto.ca/~cks/space/blog/sysadmin/ConsiderVerboseUsageMessages"  # noqa
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json()["t"], "Chris's Wiki :: blog/sysadmin/ConsiderVerboseUsageMessages")  # noqa
