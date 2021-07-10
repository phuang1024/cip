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
import argparse
from utils import *
from account import account
from build import build
from upload import upload
from install import install


def main():
    parser = argparse.ArgumentParser(description="cip client")
    parser.add_argument("-i", "--ip", default="localhost", help="IP address to connect to")
    parser.add_argument("-p", "--port", type=int, default=5555, help="Port to connect to")
    parser.add_argument("mode", nargs="?", choices=["ping", "install", "uninstall", "account", "build", "upload"])
    parser.add_argument("options", nargs="*")
    args = parser.parse_args()

    addr = (args.ip, args.port)

    if args.mode is None:
        parser.print_help(sys.stderr)
    elif args.mode == "ping":
        r = get(addr, "/ping")
        print(r.text)
    elif args.mode == "install":
        install(args.options, addr)
    elif args.mode == "account":
        account(args.options, addr)
    elif args.mode == "build":
        build(args.options, addr)
    elif args.mode == "upload":
        upload(args.options, addr)


main()
