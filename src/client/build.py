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
import argparse
import json
import tarfile
from pathlib import Path


def build(args, addr):
    parser = argparse.ArgumentParser()
    parser.add_argument("settings", nargs="?", help="cip.json path")
    args = parser.parse_args(args)

    if args.settings is None:
        parser.print_help(sys.stderr)
        return

    if not os.path.isfile(args.settings):
        print(f"No file: {args.settings}")
    else:
        with open(args.settings, "r") as file:
            settings = json.load(file)
        fname = settings["name"] + "-" + settings["version"] + ".tar.gz"

        dist = os.path.join(os.getcwd(), "dist")
        os.makedirs(dist, exist_ok=True)

        make_tar(args.settings, os.path.join(dist, fname))


def make_tar(settings_path, output):
    with open(settings_path, "r") as file:
        settings = json.load(file)

    with tarfile.open(output, "w:gz") as tar:
        tar.add(settings_path)
        for pattern in settings["files"]:
            for file in Path(".").glob(pattern):
                tar.add(file)
