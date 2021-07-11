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
import requests
from getpass import getpass as _getpass
from hashlib import sha256, sha384, sha512

VERSION = "0.0.3"

INCLUDE = os.path.expanduser("~/.cip/include")
LIB = os.path.expanduser("~/.cip/lib")
INFO = os.path.expanduser("~/.cip/info.json")
TMP = "/tmp"

HEADER_EXTS = (".h", ".hpp", ".hxx")
LIB_EXTS = (".so", ".o", ".a", ".obj")

BLACK = "\x1b[30m"
BLUE = "\x1b[34m"
CYAN = "\x1b[36m"
GREEN = "\x1b[32m"
MAGENTA = "\x1b[35m"
RED = "\x1b[31m"
RESET = "\x1b[39m"
WHITE = "\x1b[37m"
YELLOW = "\x1b[33m"


def randstr(k=30):
    return "".join(random.choices("0123456789abcdef", k=k))


def get(addr, path, headers={}):
    r = requests.get(f"http://{addr[0]}:{addr[1]}{path}", headers=headers)
    return r

def post(addr, path, data={}, headers={}):
    r = requests.post(f"http://{addr[0]}:{addr[1]}{path}", data=data, headers=headers)
    return r


def secure_hash(data: bytes, hex=False):
    """
    A function that calls SHA2 algorithms many times.
    This makes it harder to brute force reverse hashes,
    as each hash will take longer.

    Currently, one CPU core can manage 10 hashes per second.
    """
    for _ in range(100000):
        data = sha384(data).digest()
    for _ in range(100000):
        data = sha256(data).digest()
    for _ in range(100000):
        data = sha512(data).digest()
    return sha512(data).hexdigest() if hex else sha512(data).digest()

def getpass(prompt="Password: "):
    return secure_hash(_getpass(prompt).encode(), hex=True)
