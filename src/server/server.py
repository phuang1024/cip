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
import paths
from http.server import HTTPServer, BaseHTTPRequestHandler
from utils import *
from data import Data


class Handler(BaseHTTPRequestHandler):
    get_funcs = {
        "/ping": "get_ping",
        "/account/exists": "get_acctexists",
        "/project/download": "get_download",
    }

    post_funcs = {
        "/account/new": "post_newacct",
        "/project/upload": "post_upload",
    }

    def check_run(self):
        run = Data.run()
        if not run:
            self.send_response(503)
            self.send_header("content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"The server is shutting down. Please try again in 5 minutes.")
        return run

    def do_GET(self):
        if not self.check_run():
            return

        path = os.path.realpath(self.path)
        for key in self.get_funcs:
            if os.path.realpath(key) == path:
                getattr(paths, self.get_funcs[key])(self)
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
                getattr(paths, self.post_funcs[key])(self)
                return

        self.send_response(404)
        self.send_header("content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Invalid path.")


def main():
    ip = sys.argv[1]
    port = int(sys.argv[2])

    Data.makedirs("")
    Data.makedirs("accounts")
    Data.makedirs("projects")
    Data.makedirs("tmp")

    server = HTTPServer((ip, port), Handler)
    server.serve_forever()


main()
