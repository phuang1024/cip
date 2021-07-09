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
from utils import *


def upload(args, addr):
    parser = argparse.ArgumentParser()
    parser.add_argument("tarball", nargs="?", help="Tarball file path")
    args = parser.parse_args(args)

    if args.tarball is None:
        parser.print_help(sys.stderr)
        return

    with open(args.tarball, "rb") as file:
        data = file.read()
    r = post(addr, "/project/upload", data=data, headers={"ftype": args.tarball})
    print(r.text)
