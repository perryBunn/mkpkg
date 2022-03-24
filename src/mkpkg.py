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
    _question = question.trim()
    _question = _question.strip(":")

    quest = f"{_question}"
    if valid_res:
        quest += " ("
        for res in valid_res:
            quest += f"{res} "
        quest.trim()
        quest += ")"
    if default:
        quest += f" [{default}]"

    for i in range(tries):
        res = input()
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


def insert_type_into_name() -> str:
    pass


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
    date = datetime.datetime.now().strftime("%Y%m%d")
    name = get_response("What is the name of this package?")
    version = get_response("What is the package version?")
    revision = get_response("What is the package revision?")

    tar_template = f"{name}_[CONTENT]_{date}.tar.gz"

    num_tars = get_response("How many tars should be made?")

    deafult_content = ["CODE", "DOCS", "DATA", "other"]
    for i in range(num_tars):
        content = get_response(question="What are the tar contents?",
                               valid_res=deafult_content,
                               default=deafult_content[i])
        custom_type = None
        if content == "other":
            custom_type = get_response("What is the custom type?")

        print(f"Date: {date}")
        print(f"Name: {name}")
        print(f"Version: {version}")
        print(f"Revision: {revision}")
        print(f"Tar Names: {tar_template}")


def main():
    pass


if __name__ == '__main__':
    main()
