#! /usr/bin/python
"""
Name:           mkpkg.configure
Description:    This is the configuration script for `mkpkg`, It will create
                configuration files at ~/.config/mkpkg/. As well as ensure that
                all needed dependencies are available to make any source files
                that might need to be compiled.
Author:         Perry Bunn
Contact:        perry.bunn@noaa.gov
Version:        v1.0
History:        Original Copy
TODO:           See repository for project TODO and contributing guide.
License:        This Source Code Form is subject to the terms of the Mozilla
                Public License, v. 2.0. If a copy of the MPL was not distributed
                with this file, You can obtain one at
                https://mozilla.org/MPL/2.0/.
"""

from pathlib import Path

CONFIG_DIR = "~/.config/mkpkg/"
DEFAULT_CONFIG = """---
version: 1.0
args:
  pkg_templates:
    # NAME - Name of algorithm
    # CONTENT - Contents of file- CODE, DATA, DOCS, custom
    # DATE - Date in YYYYMMDD format
    # V - Algorithm Version
    # R - Algorithm Revision
    # H - Delivery hotfix revision
    &name_vrh_cont_date: "[NAME]_v[V]r[R]_deliv[H]_[CONTENT]_[DATE].tar.gz"
    &name_vrh_date:      "[NAME]_v[V]r[R]_deliv[H]_[DATE].tar.gz"
    &name_cont_date:     "[NAME]_[CONTENT]_[DATE].tar.gz"
    &name_vr_cont_date:  "[NAME]_v[V]r[R]_[CONTENT]_[DATE].tar.gz"
    &name_vr_date:       "[NAME]_v[V]r[R]_[DATE].tar.gz"
    &name_cont:          "[NAME]_[CONTENT].tar.gz"
    &name_vr_cont:       "[NAME]_v[V]r[R]_[CONTENT].tar.gz"
    &name_vr:            "[NAME]_v[V]r[R].tar.gz"

# Possible logging levels: DEBUG, INFO, WARNING, ERROR
file_level: DEBUG
stream_level: DEBUG
logging_dir: /var/log/mkpkg/

default_template: *name_cont_date
default_release_dir: ~/releases/@NAME/@VERSION/@REVISION/
"""


def make_config():
    """ Makes the default config file for mkpkg """
    config_path = Path(CONFIG_DIR).expanduser() / "config.yaml"
    if not config_path.exists():
        config_path.parent.mkdir(mode=0o755, exist_ok=True, parents=True)
        with open(config_path, mode="w+", encoding="utf-8") as file:
            file.write(DEFAULT_CONFIG)
