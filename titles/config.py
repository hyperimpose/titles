# --------------------------------------------------------------------
# Copyright (C) 2024,2026 hyperimpose.org
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

from pathlib import Path

from starlette.config import Config


config = Config(".env")


PROJECT_ROOT = Path(__file__).absolute().parent
DEBUG = config("DEBUG", cast=bool, default=False)


# Webserver
# ---------
HOST = config("HOST", default="127.0.0.1")
PORT = config("PORT", default=11557, cast=int)


# General Settings
# ----------------
lang = config("LANGUAGE", default="en")  # Default language used

# The following default is based on the TCP slow start algorithm used by most
# webservers.
# It attempts to minimize latency, but you may want to increase it so that more
# files are processed.

# 14.6 kB max size for downloaded html documents
max_htmlsize = config("MAX_HTMLSIZE", default=14_600, cast=int)
# 14.6 kB max filesize for downloaded files
max_filesize = config("MAX_FILESIZE", default=14_600, cast=int)


# HTTP Settings
# -------------
http_useragent = config("HTTP_USERAGENT", default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36")  # noqa
