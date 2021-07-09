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
import requests
from getpass import getpass as _getpass
from hashlib import sha256, sha384, sha512


def secure_hash(data: bytes, hex=False):
    """
    A function that calls SHA2 algorithms many times.
    This makes it harder to brute force reverse hashes,
    as each hash will take longer.

    Currently, one CPU core can manage 10 hashes per second.
    """
    for _ in range(100000):
        data = sha384(data).digest()
    for _ in range(100000):
        data = sha256(data).digest()
    for _ in range(100000):
        data = sha512(data).digest()
    return sha512(data).hexdigest() if hex else sha512(data).digest()

def getpass(prompt="Password: "):
    return secure_hash(_getpass(prompt).encode(), hex=True)


def get(addr, path, headers={}):
    r = requests.get(f"http://{addr[0]}:{addr[1]}{path}", headers=headers)
    return r

def post(addr, path, headers={}):
    r = requests.post(f"http://{addr[0]}:{addr[1]}{path}", headers=headers)
    return r


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

        r = post(addr, "/account/new", {"uname": uname, "password": password, "email": email})
        print(r.text)


def main():
    parser = argparse.ArgumentParser(description="cip client")
    parser.add_argument("-i", "--ip", default="localhost", help="IP address to connect to")
    parser.add_argument("-p", "--port", type=int, default=5555, help="Port to connect to")
    parser.add_argument("mode", nargs="?", choices=["ping", "install", "uninstall", "account"])
    parser.add_argument("options", nargs="*")
    args = parser.parse_args()

    addr = (args.ip, args.port)

    if args.mode is None:
        parser.print_help(sys.stderr)

    elif args.mode == "ping":
        r = get(addr, "/ping")
        print(r.text)

    elif args.mode == "account":
        account(args.options, addr)


main()
