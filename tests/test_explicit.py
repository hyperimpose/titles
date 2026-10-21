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

from titles import explicit


class Explicit(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        explicit.init()

    async def asyncTearDown(self):
        explicit.destroy()

    # async def test_image(self):
    #     path = "/path/to/image.jpg"
    #     self.assertIsInstance(await explicit.score_image(path), float)

    # async def test_video(self):
    #     path = "/path/to/video.mkv"
    #     print(await explicit.score_video(path))
