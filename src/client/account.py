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


def account(args, addr):
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", nargs="?", choices=["help", "create"])
    args = parser.parse_args(args)

    if args.mode is None or args.mode == "help":
        parser.print_help(sys.stderr)

    elif args.mode == "create":
        uname = input("Username: ")
        while get(addr, "/account/exists", {"uname": uname}).json()["exists"]:
            uname = input("Username already exists. Try again: ")
        while (password:=getpass()) != getpass("Confirm password: "):
            print("These do not match. Please try again.")
        email = input("Email (leave blank for none): ")

        r = post(addr, "/account/new", headers={"uname": uname, "password": password, "email": email})
        print(r.text)
