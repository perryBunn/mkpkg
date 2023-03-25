#! /usr/bin/python3
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
                https://mozilla.org/MPL/2.0/.
"""
from argparse import ArgumentParser
from pathlib import Path

import os
import sys

try:
    from importlib_metadata import version
except ImportError:
    from importlib.metadata import version

import yaml

from .configure import make_config
from .interactive import interactive
from .lib.helpers import make_tarfiles
from .lib.logger import get_logger


def parse_config(path: Path) -> dict:
    """ Parses YAML files and returns their dictionary representation.
    Parameters
    ----------
    path: pathlib.Path
        Location of the config file

    Returns
    -------
    dict
    """
    with open(path, mode='r', encoding="utf-8") as file:
        return yaml.safe_load(file)


def main(mkpkg_config, algo_config, configure, version_flag):
    """ Main entry point for mkpkg script

    Parameters
    ----------
    mkpkg_config
    algo_config
    configure
    version_flag

    Returns
    -------

    """
    if version_flag:
        print(version("mkpkg"))
        sys.exit()

    if configure:
        try:
            make_config()
            sys.exit()
        except Exception as err:
            # TODO: Add additional catches for permissions etc
            raise err

    try:
        config_path = Path(mkpkg_config).expanduser()
        assert config_path.exists()
    except AssertionError:
        print("mkpkg cant find a config file. Run mkpkg --configure")
        sys.exit(1)

    config = parse_config(config_path)
    logger = get_logger(config)

    logger.debug(f"Arguments: {mkpkg_config}\t{algo_config}\t{configure}")
    logger.debug(f"config_path: {config_path}")
    logger.debug(f"config: {config}")

    if algo_config is not None:
        algo_config_path = Path(algo_config)
        algo_configuration = parse_config(algo_config_path)
        try:
            make_tarfiles(algo_configuration)
        except KeyError:
            print("Algorithm package config is malformed")
            sys.exit(1)
    else:
        interactive(config, logger)


class Namespace:
    """ Class for argparse """
    configure: bool
    mkpkg_config: str
    algo_config: str
    version_flag: bool


def terminal():
    """ Entry point for poetry and pipx installs """
    serial = Namespace()
    parser = ArgumentParser(description="mkpkg - Suckless package creation")
    parser.add_argument("--configure", action="store_true", default=False,
                        help="Configure mkpkg")
    parser.add_argument("algo_config", nargs="?",
                        default=None,
                        help="Algorithm config file. Stores the files "
                             "contained in each tar.")
    parser.add_argument("-c", "--config", dest="mkpkg_config",
                        default="~/.config/mkpkg/config.yaml",
                        help="Config file used for default values across "
                             "algorithms. To create this file run "
                             "$mkpkg --configure")
    parser.add_argument("--keep-vcs-files")
    parser.add_argument("-v", "--version_flag", action="store_true",
                        default=False, help="Prints the package version_flag")
    args = parser.parse_args(namespace=serial)
    main(args.mkpkg_config, args.algo_config, args.configure, args.version_flag)


if __name__ == '__main__':
    terminal()
