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
import shutil
import time
import json
import random
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

PARENT = os.path.dirname(os.path.realpath(__file__))
DATA = os.path.join(PARENT, "data")

REQUIRED_FIELDS = (
    "name",
    "version",
    "files",
)


class Data:
    @staticmethod
    def realpath(path):
        return os.path.join(DATA, path)
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

    def get_download(self):
        project = self.headers["project"]

        if Data.isdir(f"projects/{project}"):
            info = Data.load(f"projects/{project}/info.json")
            latest = info["latest"]

            src = Data.realpath(f"projects/{project}/{latest}")
            tmp = Data.realpath(f"tmp/{randstr()}")
            shutil.make_archive(tmp, "xztar", src)

            self.send_response(200)
            self.send_header("content-type", "text/plain")
            self.send_header("ftype", ".tar.xz")
            with open(tmp+".tar.xz", "rb") as file:
                self.send_header("data", str(file.read()))
            self.end_headers()
            self.wfile.write(b"Success!")

        else:
            self.send_response(404)
            self.send_header("content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Project not found.")

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

    def post_upload(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        ftype = self.headers["ftype"]
        uname = self.headers["uname"]
        password = self.headers["password"]

        path = f"tmp/{randstr()}.{ftype}"
        Data.write(path, data, mode="wb")

        success, msg = process_pkg(path, uname, password)

        self.send_response((201 if success else 405))
        self.send_header("content-type", "text/plain")
        self.end_headers()
        self.wfile.write(msg.encode())

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


def process_pkg(path, uname, password):
    if not Data.isfile(f"accounts/{uname}.json"):
        return (False, "Account does not exist.")

    data = Data.load(f"accounts/{uname}.json")
    if data["password"] != password:
        return (False, "Password is incorrect.")

    try:
        realpath = Data.realpath(path)
        output = realpath + "_dir"
        shutil.unpack_archive(realpath, output)
    except ValueError:
        return (False, "Could not unpack archive.")

    if "cip.json" not in os.listdir(output):
        return (False, "cip.json not found.")

    with open(os.path.join(output, "cip.json"), "r") as file:
        settings = json.load(file)
    for field in REQUIRED_FIELDS:
        if field not in settings:
            return (False, f"Key {field} required in cip.json, but not found.")

    name = settings["name"]
    version = settings["version"]
    if Data.isdir(f"projects/{name}"):
        if version == "info.json":
            return (False, "Invalid version name.")

        project_info = Data.load(f"projects/{name}/info.json")
        if project_info["owner"] != uname:
            return (False, "The project already exists and is not owned by you.")
        if version in project_info["versions"]:
            return (False, "The version already exists.")

    else:
        Data.makedirs(f"projects/{name}")
        Data.dump(f"projects/{name}/info.json", {"owner": uname, "versions": {}})
        project_info = Data.load(f"projects/{name}/info.json")

    project_info["versions"][version] = settings
    project_info["latest"] = version
    Data.dump(f"projects/{name}/info.json", project_info)

    release_path = Data.realpath(f"projects/{name}/{version}")
    os.makedirs(release_path)
    shutil.unpack_archive(Data.realpath(path), release_path)

    return (True, "Success!")


def get_date():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")


def randstr(k=30):
    return "".join(random.choices("0123456789abcdef", k=k))


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
