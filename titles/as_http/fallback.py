# --------------------------------------------------------------------
# Copyright (C) 2023-2024, 2026 hyperimpose.org
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

from titles.common import Title
from . import hparser, shared


async def handle(r) -> Title:
    mimetype = hparser.mimetype(r.headers) or "application/octet-stream"
    filename = hparser.filename(r.headers)
    size = hparser.filesize(r.headers)

    p = []

    if filename:
        p.append(filename)

    t = ", ".join([*p, mimetype])

    if size:
        t += f", Size: {size}"

    return Title(t=t, explicit=await shared.get_explicit(r))
