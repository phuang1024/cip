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
import subprocess
import argparse

PARENT = os.path.dirname(os.path.realpath(__file__))
RUN_FILE = os.path.join(PARENT, "run")


def remove():
    if os.path.isfile(RUN_FILE):
        os.remove(RUN_FILE)


def write(data):
    with open(RUN_FILE, "w") as file:
        file.write(data)


def main():
    parser = argparse.ArgumentParser(description="cip server")
    parser.add_argument("-i", "--ip", default="0.0.0.0", help="IP address to serve on")
    parser.add_argument("-p", "--port", type=int, default=5555, help="Port to serve on")
    parser.add_argument("-t", "--timeout", type=float, default=720, help="Minutes between server restart")
    args = parser.parse_args()

    ip = args.ip
    port = args.port

    remove()

    popen_args = ["python", os.path.join(PARENT, "server.py"), ip, str(port)]
    while True:
        write("run")
        proc = subprocess.Popen(popen_args)
        print(f"Starting on IP={ip}, PORT={port}")

        time.sleep(args.timeout*60)
        write("stop")
        time.sleep(300)

        proc.kill()
        print("Stopping server")


main()
