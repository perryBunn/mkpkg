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
                http://mozilla.org/MPL/2.0/.
"""

from argparse import ArgumentParser
from datetime import datetime
from logging import Logger
from pathlib import Path
from typing import Union

import tarfile
import re
import yaml

from lib.logger import get_logger


def get_response(question: str, valid_res: list=None, default=None, tries: int=1,
                 not_valid: list=None, permutations: bool=False) -> Union[None, str]:
    """ Gets response to a question asked.
        Parameters
        ----------
        question: str
            Question to be asked to the user.
        valid_res: list
            List of valid responses.
        tries: int
            Number of tries that the user has to answer the question.
        not_valid: list
            List of not valid responses.
        permutations: bool
            Creates permutations of valid responses. Useful for questions where
            multiple responses could be possible/

        Returns
        -------
        None | str
            if an int is returned then the response from the user is not valid.
    """
    if permutations and 2 <= len(valid_res):
        upb = len(valid_res)
        for i in range(0, upb - 1):
            temp = valid_res[i]
            for j in range(1, upb):
                if i == j:
                    continue
                temp+=valid_res[j]
                valid_res.append(temp)

    # Strips chars ' ' and ':' from the question
    _question = question.strip()
    _question = _question.strip(":")

    quest = f"{_question}"
    if valid_res:
        quest += " ("
        for res in valid_res:
            quest += f"{res} "
        quest = quest[:-1]  # Remove trailing ' '
        quest += ")"
    if default:
        quest += f" [{default}]"

    for i in range(tries):
        res = input(f"{quest} ")
        if not res.strip() and default:
            res = default
        if not_valid:
            for npat in not_valid:
                nmatch = re.search(npat, res)
                if nmatch:
                    print(f"{res} is an invalid response.")
                    continue

        if valid_res is None or res in valid_res:
            return res
        print(f"{res} is an invalid response.")
    return None


def insert_into(template, string, pattern=r"\[CONTENT\]") -> str:
    type_pattern = re.compile(pattern)
    match = type_pattern.search(template)

    return f"{template[:match.start()]}{string}{template[match.end():]}"


def name_list_fmt(name_list: list) -> str:
    res = ""
    for name in name_list:
        res += f"\n\t{name}"
    return res


def parse_path(path: str, **kargs) -> Path:
    """
        %NAME%      Inserts the name of the package into the path
        %VERSION%   Inserts the version of the package into the path
        %REVISION%  Inserts the revision of the package into the path
        %DATE%      Inserts the date into the path
    """

    path_variables = {
        "NAME": r"@NAME",
        "VERSION": r"@VERSION",
        "REVISION": r"@REVISION",
        "DATE": r"@DATE"
    }
    tmp_str = path
    for var, pat in path_variables.items():
        try:
            tmp_str = insert_into(tmp_str, kargs[var], pat)
        except AttributeError:
            pass

    return Path(tmp_str)


def interactive(config: dict, logger: Logger):
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
    deafult_content = ["CODE", "DOCS", "DATA", "other"]
    terminals = ["", "!", "?"]
    tar_names = []

    current_dir = Path("./")
    dir_name = current_dir.resolve().name
    date = datetime.now().strftime("%Y%m%d")
    name = get_response("What is the name of this package?", default=dir_name)
    version = get_response("What is the package version?")
    revision = get_response("What is the package revision?")
    num_tars = int(get_response("How many tars should be made?", default='3'))
    tar_template = f"{name}_[CONTENT]_{date}.tar.gz"

    for i in range(num_tars):
        content = get_response(question="What is the type of tar content?",
                               valid_res=deafult_content,
                               default=deafult_content[i])
        custom_type = None
        if content == "other":
            custom_type = get_response("What is the custom type?")

        if custom_type:
            tar_names.append(insert_into(tar_template, custom_type))
        tar_names.append(insert_into(tar_template, content))

    print(f"Date: {date}")
    print(f"Name: {name}")
    print(f"Version: {version}")
    print(f"Revision: {revision}")
    print(f"Tar Names: {name_list_fmt(tar_names)}")

    store_str = get_response("Where would you like to store the tars?",
                             default=config["default_release_dir"])
    store = parse_path(path=store_str, DATE=date, NAME=name, VERSION=version,
                        REVISION=revision)
    store.mkdir(exist_ok=True, parents=True)
    config = {
        "date": date,
        "name": name,
        "version": version,
        "revision": revision,
        "numtars": num_tars,
        "storestr": store_str,
        "storepath": store.as_posix()
    }

    for tar in tar_names:
        tar_path = store / tar
        print(f"{tar}:")
        files = []
        data = "start"
        config[tar] = []
        while data not in terminals:
            data = get_response("Path to include:")
            if data.strip():
                path = Path(data)
                if not path.resolve().exists():
                    print(f"{path} does not exist or could not be found.")
                    continue
                files.append(path)
                config[tar] += path.resolve()

        with tarfile.open(tar_path, "w:gz") as tar_file:
            for file in files:
                tar_file.add(file)

    config_res = get_response("Do you want to save this configuration to a file?",
                              default='n', valid_res=['y', 'n'])
    if config_res == 'y':
        config_str = get_response("Where would you like to save this config?",
            default=f"./{name}.mkpkg-conf")
        config_path = parse_path(path=config_str, DATE=date, NAME=name,
                                  VERSION=version, REVISION=revision)
        with open(config_path, mode='w', encoding="utf-8") as file:
            yaml.safe_dump(config, file)


def parse_config(path: Path):
    with open(path, mode='r', encoding="utf-8") as file:
        return yaml.safe_load(file)


def main(mkpkg_config="~/.config/mkpkg/config.yaml", algo_config=None):
    config_path = Path(mkpkg_config).expanduser()
    config = parse_config(config_path)
    logger = get_logger(config)

    logger.debug(f"Arguments: {mkpkg_config}\t{algo_config}")
    logger.debug(f"config_path: {config_path}")
    logger.debug(f"config: {config}")


    if algo_config is not None:
        algo_config_path = Path(algo_config)

    interactive(config, logger)


if __name__ == '__main__':
    parser = ArgumentParser(description="mkpkg")
    parser.add_argument("-c", "--config", dest="mkpkg_config",
        default="~/.config/mkpkg/config.yaml",
        help="Config file used for default values across algorithms.")
    parser.add_argument("ALGO_CONFIG", nargs="?",
        help="Algorithm config file. Stores the files contained in each tar.")
    args = parser.parse_args()
    main(args.mkpkg_config, args.ALGO_CONFIG)
