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

import yaml

from configure import make_config
from interactive import interactive
from lib.helpers import make_tarfiles
from lib.logger import get_logger


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


def main(mkpkg_config, algo_config, configure):
    if configure:
        make_config()

    try:
        config_path = Path(mkpkg_config).expanduser()
    except Exception as err:
        # TODO: Need to specify which errors to catch
        pass

    config = parse_config(config_path)
    logger = get_logger(config)

    logger.debug(f"Arguments: {mkpkg_config}\t{algo_config}")
    logger.debug(f"config_path: {config_path}")
    logger.debug(f"config: {config}")

    if algo_config is not None:
        algo_config_path = Path(algo_config)
        algo_configuration = parse_config(algo_config_path)
        make_tarfiles(algo_configuration)
    else:
        interactive(config, logger)


class Namespace:
    configure: bool
    mkpkg_config: str
    algo_config: str


if __name__ == '__main__':
    serial = Namespace()
    parser = ArgumentParser(description="mkpkg - Suckless package creation")
    parser.add_argument("--configure", action="store_true", default=False, help="Configure mkpkg")
    parser.add_argument("algo_config", nargs="?",
                        default=None,
                        help="Algorithm config file. Stores the files contained in each tar.")
    parser.add_argument("-c", "--config", dest="mkpkg_config",
                        default="~/.config/mkpkg/config.yaml",
                        help="Config file used for default values across algorithms. To create this file run "
                             "$mkpkg --configure")
    parser.add_argument("--keep-vcs-files")
    args = parser.parse_args(namespace=serial)
    main(args.mkpkg_config, args.algo_config, args.configure)
