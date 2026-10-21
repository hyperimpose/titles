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

from titles.as_http import browser


class HttpBrowser(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await browser.init()

    async def asyncTearDown(self):
        await browser.destroy()

    async def test_amazon(self):
        u = "https://www.amazon.com/dp/0500027358"
        e = {'t': 'A to Z of The Designers Republic: Anderson, Ian: 9780500027356: Amazon.com: Books'}  # noqa
        self.assertEqual(await browser.get_title(u), e)

    async def test_reddit(self):
        u = "https://www.reddit.com/r/synthesizers/comments/1nw6aeh/thoughts_on_roland_tr1000/"  # noqa
        e = {'t': 'Thoughts on Roland TR-1000? : r/synthesizers'}
        self.assertEqual(await browser.get_title(u), e)
