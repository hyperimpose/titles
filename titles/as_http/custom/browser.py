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

# Sites that must be handled immediately by the browser.

from .. import browser


SITES = ["amazon.com/*", "utcc.utoronto.ca/~cks/*"]


async def handler(url: str, **_kwargs):
    return await browser.get_title(url)
