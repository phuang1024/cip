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
import time
import shutil
import json
from utils import *
from data import Data


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


def get_ping(self):
    self.send_response(200)
    self.send_header("content-type", "text/plain")
    self.end_headers()
    self.wfile.write(b"Ping successful")

def get_version(self):
    self.send_response(200)
    self.send_header("content-type", "text/plain")
    self.send_header("version", VERSION)
    self.end_headers()
    self.wfile.write(VERSION.encode())

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
        latest_info = info["versions"][latest]

        src = Data.realpath(f"projects/{project}/{latest}")
        tmp = Data.realpath(f"tmp/{randstr()}")
        shutil.make_archive(tmp, "xztar", src)

        self.send_response(200)
        self.send_header("content-type", "text/plain")
        self.send_header("ftype", ".tar.xz")
        self.send_header("depends", str(latest_info["dependencies"]))
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
    ftype = os.path.basename(self.headers["ftype"])
    uname = self.headers["uname"]
    password = self.headers["password"]

    path = f"tmp/{randstr()}.{ftype}"
    Data.write(path, data, mode="wb")

    success, msg = process_pkg(path, uname, password)

    self.send_response((201 if success else 405))
    self.send_header("content-type", "text/plain")
    self.end_headers()
    self.wfile.write(msg.encode())
