#
#  Piano Video
#  Piano MIDI visualizer
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
import shutil
import subprocess

VERSION = "0.0-2"
PKG_NAME = f"cip_{VERSION}"
META = {
    "Package":      "cip",
    "Version":      VERSION,
    "Section":      "base",
    "Priority":     "optional",
    "Architecture": "i386",
    "Maintainer":   "Patrick Huang <huangpatrick16777216@gmail.com>",
    "Description":  "C++ library installer."
}

PARENT = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.join(PARENT, PKG_NAME)

CMDS = (
    ("cip", "/usr/local/bin/cip_utils/main.py"),
)
START_DATA = """
#!/usr/bin/python3.8
import sys
import os
cmd = "python3.8 {} "
for a in sys.argv[1:]:
    cmd += a
    cmd += " "
os.system(cmd.strip())
""".strip()


def makedirs():
    os.makedirs(os.path.join(ROOT, "DEBIAN"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "usr/local/bin/cip_utils"), exist_ok=True)


def write_control():
    path = os.path.join(ROOT, "DEBIAN", "control")
    with open(path, "w") as file:
        for key in META:
            file.write("{}: {}\n".format(key, META[key]))


def copy_files():
    src = os.path.join(os.path.dirname(PARENT), "src", "client")
    dirs = [""]
    while len(dirs) > 0:
        d = dirs.pop(0)
        for f in os.listdir(os.path.join(src, d)):
            if f not in ("__pycache__", "config", "tmp"):
                relpath = os.path.join(d, f)
                abspath = os.path.join(src, relpath)
                dstpath = os.path.join(ROOT, "usr/local/bin/cip_utils", relpath)
                if os.path.isfile(abspath):
                    os.makedirs(os.path.dirname(dstpath), exist_ok=True)
                    shutil.copy(abspath, dstpath)
                elif os.path.isdir(abspath):
                    dirs.append(relpath)


def write_command(cmd, target):
    start_path = os.path.join(ROOT, "usr/local/bin", cmd)
    with open(start_path, "w") as file:
        file.write(START_DATA.format(target))
    subprocess.Popen(["chmod", "+x", start_path]).wait()


def build():
    subprocess.Popen(["dpkg-deb", "--build", PKG_NAME], cwd=PARENT).wait()


def cleanup():
    shutil.rmtree(ROOT)


def main():
    makedirs()
    write_control()
    copy_files()
    for cmd, target in CMDS:
        write_command(cmd, target)
    build()
    cleanup()


main()
