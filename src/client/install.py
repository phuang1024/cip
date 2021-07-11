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
import json
import argparse
from ast import literal_eval
from utils import *


def install_pkg(addr, pkg):
    with open(INFO, "r") as file:
        info = json.load(file)
    installed_files = {f for key in info for f in info[key]["files"] if info[key]["files"][f]}

    print(f"Installing {pkg}")

    if pkg in info:
        sys.stdout.write(YELLOW)
        print(f"  Skipping {pkg} (already installed)")
        sys.stdout.write(RESET)
        return

    r = get(addr, "/project/download", headers={"project": pkg})
    if r.status_code == 404:
        print(f"  Package not found")
        return

    ext = r.headers["ftype"]
    tmp_path = os.path.join(TMP, "cip_"+randstr()+ext)
    depends = literal_eval(r.headers["depends"])
    with open(tmp_path, "wb") as file:
        file.write(literal_eval(r.headers["data"]))

    tmp_dir = tmp_path+"_dir"
    shutil.unpack_archive(tmp_path, tmp_dir)

    pkg_files = []
    for file in os.listdir(tmp_dir):
        abspath = os.path.join(tmp_dir, file)
        if os.path.isfile(abspath):
            print(f"  Found file {file}")

            valid = True
            if file in installed_files:
                valid = False
                sys.stdout.write(YELLOW)
                print(f"    Skipping {file} (file already exists from another package)")
                sys.stdout.write(RESET)
            elif file.endswith(HEADER_EXTS):
                print(f"    Copying {file} to include")
                os.rename(abspath, os.path.join(INCLUDE, file))
            elif file.endswith(LIB_EXTS):
                print(f"    Copying {file} to lib")
                os.rename(abspath, os.path.join(LIB, file))
            else:
                valid = False
                sys.stdout.write(YELLOW)
                print(f"    Skipping {file} (invalid extension)")
                sys.stdout.write(RESET)

            pkg_files.append((file, valid))

    info[pkg] = {
        "files": {f: i for f, i in pkg_files},
        "depends": depends,
    }
    with open(INFO, "w") as file:
        json.dump(info, file, indent=4)

    if len(depends) > 0:
        print("  Installing dependencies: "+" ".join(depends))
        for pkg in depends:
            install_pkg(addr, pkg)


def uninstall_pkg(addr, pkg):
    with open(INFO, "r") as file:
        info = json.load(file)

    print(f"Uninstalling {pkg}")
    dependents = [p for p in info if pkg in info[p]["depends"] and p != pkg]

    if len(dependents) > 0:
        sys.stdout.write(YELLOW)
        print(f"  These packages depend on {pkg}: "+" ".join(dependents))
        print(f"  Uninstalling {pkg} may cause them to lose functionality.")
        if input("  Proceed with uninstallation? [y/N] ").lower().strip() != "y":
            return

    files = [f for f in info[pkg]["files"] if info[pkg]["files"][f]]
    print(f"  Uninstalling {pkg} will remove:")
    for f in files:
        print(f"    {f}")
    if input("  Uninstall? [y/N] ").lower().strip() != "y":
            return

    for f in files:
        print(f"  Removing {f}")
        if f.endswith(HEADER_EXTS):
            os.remove(os.path.join(INCLUDE, f))
        elif f.endswith(LIB_EXTS):
            os.remove(os.path.join(LIB, f))

    info.pop(pkg, None)
    with open(INFO, "w") as file:
        json.dump(info, file)


def install(args, addr):
    parser = argparse.ArgumentParser()
    parser.add_argument("packages", nargs="*", help="Packages to install.")
    args = parser.parse_args(args)

    if len(args.packages) == 0:
        parser.print_help(sys.stderr)
        return

    for pkg in args.packages:
        install_pkg(addr, pkg)


def uninstall(args, addr):
    parser = argparse.ArgumentParser()
    parser.add_argument("packages", nargs="*", help="Packages to install.")
    args = parser.parse_args(args)

    if len(args.packages) == 0:
        parser.print_help(sys.stderr)
        return

    for pkg in args.packages:
        uninstall_pkg(addr, pkg)
