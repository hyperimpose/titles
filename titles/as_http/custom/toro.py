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

from .. import default


UPLOADS = ["toro.lain.la/u/*", "toro.lain.la/uploads/*"]


async def uploads(url: str, *, headers={}):
    file_url = url.replace("/u/", "/f/", 1)

    result = await default.get(file_url, headers=headers)
    if result:
        result["t"] += ", " + file_url

    return result
