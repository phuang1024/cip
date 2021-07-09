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

import sys
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

PARENT = os.path.dirname(os.path.realpath(__file__))
DATA = os.path.join(PARENT, "data")


class Data:
    @staticmethod
    def read(path, mode="r"):
        with open(os.path.join(DATA, path), mode) as file:
            return file.read()

    @staticmethod
    def write(path, data, mode="w"):
        with open(os.path.join(DATA, path), mode) as file:
            file.write(data)

    @staticmethod
    def isfile(path):
        return os.path.isfile(os.path.join(DATA, path))

    @staticmethod
    def isdir(path):
        return os.path.isdir(os.path.join(DATA, path))

    @staticmethod
    def makedirs(path, exist_ok=True):
        os.makedirs(os.path.join(DATA, path), exist_ok=exist_ok)

    @staticmethod
    def listdir(path):
        return os.listdir(os.path.join(DATA, path))

    @staticmethod
    def load(path):
        return json.loads(Data.read(path))

    @staticmethod
    def dump(path, obj):
        Data.write(path, json.dumps(obj, indent=4))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        pass

    def do_POST(self):
        pass


def main():
    ip = sys.argv[1]
    port = int(sys.argv[2])

    Data.makedirs("")

    server = HTTPServer((ip, port), Handler)
    server.serve_forever()


main()
