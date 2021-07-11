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


def install_pkg(addr, pkg):
    print(f"Installing {pkg}")

    r = get(addr, "/project/download", headers={"project": pkg})
    if r.status_code == 404:
        print(f"  Package not found")
        return

    ext = r.headers["ftype"]
    tmp_path = os.path.join(TMP, "cip_"+randstr()+ext)
    with open(tmp_path, "wb") as file:
        file.write(literal_eval(r.headers["data"]))

    tmp_dir = tmp_path+"_dir"
    shutil.unpack_archive(tmp_path, tmp_dir)

    for file in os.listdir(tmp_dir):
        abspath = os.path.join(tmp_dir, file)
        if os.path.isfile(abspath):
            print(f"  Found file {file}")
            if file.endswith(HEADER_EXTS):
                print(f"    Copying {file} to include")
                os.rename(abspath, os.path.join(INCLUDE, file))
            elif file.endswith(LIB_EXTS):
                print(f"    Copying {file} to lib")
                os.rename(abspath, os.path.join(LIB, file))
            else:
                print(f"    Skipping {file}")

    depends = literal_eval(r.headers["depends"])
    if len(depends) > 0:
        print("  Installing dependencies: "+" ".join(depends))
        for pkg in depends:
            install_pkg(addr, pkg)


def install(args, addr):
    parser = argparse.ArgumentParser()
    parser.add_argument("packages", nargs="*", help="Packages to install.")
    args = parser.parse_args(args)

    if len(args.packages) == 0:
        parser.print_help(sys.stderr)
        return

    for pkg in args.packages:
        install_pkg(addr, pkg)
