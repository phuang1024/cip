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
import argparse
from ast import literal_eval
from utils import *


def install(args, addr):
    parser = argparse.ArgumentParser()
    parser.add_argument("packages", nargs="*", help="Packages to install.")
    args = parser.parse_args(args)

    if len(args.packages) == 0:
        parser.print_help(sys.stderr)
        return

    for pkg in args.packages:
        r = get(addr, "/project/download", headers={"project": pkg})
        if r.status_code == 404:
            print(f"Not found: {pkg}")
            continue

        ext = r.headers["ftype"]
        tmp_path = os.path.join("/tmp", randstr()+ext)
        with open(tmp_path, "wb") as file:
            file.write(literal_eval(r.headers["data"]))

        tmp_dir = tmp_path+"_dir"
        shutil.unpack_archive(tmp_path, tmp_dir)
