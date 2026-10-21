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

# The following tests are based on https://irc-bot-science.clsr.net/

import unittest

from starlette.testclient import TestClient
from titles.webserver import app


class IrcBotScience(unittest.TestCase):
    def test_carriage_return(self):
        u = "https://irc-bot-science.clsr.net/test"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            t = ("test QUIT :Look at me, I'm an IRC bot with security holes!"
                 " (ignore this if it's all in one line)")
            self.assertEqual(r.json()["t"], t)

    def test_uncommon(self):
        u = "https://irc-bot-science.clsr.net/tags"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json()["t"], "this is a site <title>")

    def test_uncommon_hard(self):
        u = "https://irc-bot-science.clsr.net/hardmode"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            t = "this is a <title> site title < /title> but <title> not just this part</title>"  # noqa
            self.assertEqual(r.json()["t"], t)

    def test_notitle(self):
        u = "https://irc-bot-science.clsr.net/notitle"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            # There is no title set, but browser.get_title() falls back to
            # text in the body of the document.
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json()["t"], "no title here")

    # Skipped the long title test. This is the responsibility of the caller.
    # Length is handled by the max_htmlsize config option.

    def test_large_filesize(self):
        u = "https://irc-bot-science.clsr.net/internet.gz"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            t = "the-internet.gz, application/x-gzip, Size: 1.1 EB"
            self.assertEqual(r.json()["t"], t)

    def test_ctcp_messages(self):
        u = "https://irc-bot-science.clsr.net/ctcp"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json()["t"], "ACTION is a shit bot")

    def test_redirect(self):
        u = "https://irc-bot-science.clsr.net/redirect"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json()["t"], "The page isn’t redirecting properly")  # noqa

    def test_redirect_to_other_urls(self):
        u = "https://irc-bot-science.clsr.net/redirect/0"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json()["t"], "The page isn’t redirecting properly")  # noqa

    def test_1gb_html_fake_content_length(self):
        u = "https://irc-bot-science.clsr.net/fakelength"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 404)

    def test_1gb_html_with_title(self):
        u = "https://irc-bot-science.clsr.net/large"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 200)
            t = "If this title is printed, it works correctly."
            self.assertEqual(r.json()["t"], t)

    def test_1gb_headers(self):
        u = "https://irc-bot-science.clsr.net/longheaders"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 404)

    def test_extremely_long_header(self):
        u = "https://irc-bot-science.clsr.net/bigheader"
        with TestClient(app) as client:
            r = client.get("/title", params={"u": u})
            self.assertEqual(r.status_code, 404)
