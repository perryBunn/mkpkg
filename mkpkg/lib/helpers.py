"""
Name:           mkpkg.lib.helpers
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

from pathlib import Path
from typing import Union

import re
import tarfile
import yaml


def get_response(question: str, choices: list = None, default=None, tries: int = 1,
                 not_valid: list = None, permutations: bool = False) -> Union[None, str]:
    """ Gets response to a question asked.
        Parameters
        ----------
        question: str
            Question to be asked to the user.
        choices: list
            List of valid responses.
        default
            Default response if tries are used or empty value is passed.
        tries: int
            Number of tries that the user has to answer the question.
        not_valid: list
            List of not valid responses.
        permutations: bool
            Creates permutations of valid responses. Useful for questions where
            multiple responses could be possible.

        Returns
        -------
        None | str
            if an int is returned then the response from the user is not valid.
    """
    if permutations and 2 <= len(choices):
        upb = len(choices)
        for i in range(0, upb - 1):
            temp = choices[i]
            for j in range(1, upb):
                if i == j:
                    continue
                temp += choices[j]
                choices.append(temp)

    # Strips chars ' ' and ':' from the question
    _question = question.strip()
    _question = _question.strip(":")

    quest = f"{_question}"
    if choices:
        quest += " ("
        for choice in choices:
            quest += f"{choice} "
        quest = quest.strip()  # Remove trailing ' '
        quest += ")"
    # TODO: Need to think of a better way to notate a default argument
    # Its particularly confusing when there are also choices available
    if default:
        quest += f" [{default}]"

    for i in range(tries):
        res = input(f"{quest}: ")
        if not res.strip() and default:
            res = default
        if not_valid:
            for npat in not_valid:
                negative_match = re.search(npat, res)
                if negative_match:
                    print(f"{res} is an invalid response.")
                    continue

        if choices is None or res in choices:
            return res
        print(f"{res} is an invalid response.")
    return None


def insert_into(template: str, content: str, pattern: str = r"\[CONTENT\]") -> str:
    """ Inserts content into a template string that matches some regex pattern
    Parameters
    ----------
    template: str
        Some string that is to be modified
    content: str
        Some string that is to inserted into the template
    pattern: str
        Some regex pattern that is to be matched in the template

    Returns
    -------
    str
        Returns the interpolated version of the template string once the content is injected
    """
    type_pattern = re.compile(pattern)
    match = type_pattern.search(template)

    return f"{template[:match.start()]}{content}{template[match.end():]}"


def make_tarfiles(config):
    """ Creates tar files based on a config passed.
    Parameters
    ----------
    config: dict
        Config file containing information about an algorithm package
    """
    write_modes = {
        "tar": 'x',
        "tar.gz": "x:gz",
        "tar.bz2": "x:bz2",
        "tar.xz": "x:xz"
    }
    store = Path(config["storepath"])
    store.mkdir(mode=0o755, exist_ok=True, parents=True)
    for tar in config["tars"]:
        tar_path = store / tar
        try:
            mode = write_modes[config["archivetype"]]
            with tarfile.open(tar_path, mode) as tar_file:
                for file in config["tars"][tar]:
                    tar_file.add(file)
        except FileExistsError:
            print(f"{tar_path} already exist, mkpkg will not overwrite archives.")


def ordinal(number):
    """ Convert an integer into its ordinal representation::
    Parameters
    ----------
    number: int
        Some number to get the ordinal of

    Returns
    -------
    str

    Examples
    --------
    ordinal(0)   => '0th'
    ordinal(3)   => '3rd'
    ordinal(122) => '122nd'
    ordinal(213) => '213th'
    """
    number = int(number)
    if 11 <= (number % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(number % 10, 4)]
    return str(number) + suffix


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
        "DATE": r"@DATE"
    }
    tmp_str = path
    for var, pat in path_variables.items():
        try:
            tmp_str = insert_into(tmp_str, kargs[var], pat)
        except AttributeError:
            pass

    return Path(tmp_str)
