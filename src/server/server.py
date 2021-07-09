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
import time
import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

PARENT = os.path.dirname(os.path.realpath(__file__))
DATA = os.path.join(PARENT, "data")


class Data:
    @staticmethod
    def run():
        with open(os.path.join(PARENT, "run"), "r") as file:
            return file.read().strip() == "run"
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
    get_funcs = {
        "/ping": "get_ping",
        "/account/exists": "get_acctexists",
    }

    post_funcs = {
        "/account/new": "post_newacct",
    }

    def check_run(self):
        run = Data.run()
        if not run:
            self.send_response(503)
            self.send_header("content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"The server is shutting down. Please try again in 5 minutes.")
        return run

    def get_ping(self):
        self.send_response(200)
        self.send_header("content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Ping successful")

    def get_acctexists(self):
        self.send_response(200)
        self.send_header("content-type", "text/json")
        self.end_headers()

        uname = self.headers["uname"]
        exists = Data.isfile(f"accounts/{uname}.json")
        self.wfile.write(json.dumps({"exists": exists}).encode())

    def post_newacct(self):
        uname = self.headers["uname"]
        password = self.headers["password"]
        email = self.headers["email"]

        if Data.isfile(f"accounts/{uname}.json"):
            self.send_response(405)
            self.send_header("content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"The username already exists.")
        else:
            Data.dump(f"accounts/{uname}.json", {"uname": uname, "password": password,
                "email": email, "create_time": time.time(), "create_date": get_date()})
            self.send_response(200)
            self.send_header("content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Success!")

    def do_GET(self):
        if not self.check_run():
            return

        path = os.path.realpath(self.path)
        for key in self.get_funcs:
            if os.path.realpath(key) == path:
                getattr(self, self.get_funcs[key])()
                return

        self.send_response(404)
        self.send_header("content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Invalid path.")

    def do_POST(self):
        if not self.check_run():
            return

        path = os.path.realpath(self.path)
        for key in self.post_funcs:
            if os.path.realpath(key) == path:
                getattr(self, self.post_funcs[key])()
                return

        self.send_response(404)
        self.send_header("content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Invalid path.")


def get_date():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")


def main():
    ip = sys.argv[1]
    port = int(sys.argv[2])

    Data.makedirs("")
    Data.makedirs("accounts")

    server = HTTPServer((ip, port), Handler)
    server.serve_forever()


main()
