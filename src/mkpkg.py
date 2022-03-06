#! /usr/bin/ python3
"""
Name:           mkpkg.py
Description:    TODO: Add Description
Author:         Perry Bunn
Contact:        perry.bunn@noaa.gov
Version:        v1.0
History:        Original Copy
TODO:           See repository for project TODO and contributing guide.
License:        This Source Code Form is subject to the terms of the Mozilla
                Public License, v. 2.0. If a copy of the MPL was not distributed
                with this file, You can obtain one at
                http://mozilla.org/MPL/2.0/.
"""

from pathlib import Path
from typing import Union

import yaml


def interactive():
    """
      Flow:
        1. Ask for package information.
          a. Ask for package name; Default will be the parent directory name.
          b. Ask for package version
          c. Ask for revision number; Default is none - letting mkpkg decide.
        2. Ask how many tars to make. Default 3
        3. For each tar:
          a. Ask for content type. Default choices: CODE, DATA, DOCS
          b. Ask for files to include in this tar
          c. Ask if there are exclusions; pattern or file path
        4. Ask where you would like to place the tars;
           Default location being ./releases/<version>/<revision>/
        5. Ask if you would like to save the config to a file.
    """


def main():
    pass


if __name__ == '__main__':
    main()
