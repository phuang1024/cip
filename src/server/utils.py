#
#  cip
#  C++ library installer
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import os
import random
import string
from datetime import datetime

def get_date():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")

def randstr(k=30):
    return "".join(random.choices("0123456789abcdef", k=k))

VERSION = "0.0.3"
PARENT = os.path.dirname(os.path.realpath(__file__))
DATA = os.path.join(PARENT, "data")

REQUIRED_FIELDS = (
    "name",
    "version",
    "files",
    "dependencies",
)
NAME_CHARS = string.ascii_letters+string.digits
