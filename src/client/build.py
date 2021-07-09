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

import json
import tarfile
from pathlib import Path


def build(settings_path, output):
    with open(settings_path, "r") as file:
        settings = json.load(file)

    with tarfile.open(output, "w:gz") as tar:
        tar.add(settings_path)
        for pattern in settings["files"]:
            for file in Path(".").glob(pattern):
                tar.add(file)
