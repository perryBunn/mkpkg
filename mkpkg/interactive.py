from datetime import datetime
from logging import Logger
from pathlib import Path

import yaml

from .lib.helpers import get_response, insert_into, make_tarfiles, ordinal, parse_path


def __name_list_fmt(name_list: list) -> str:
    """ Formats a list of strings into a list
    Parameters
    ----------
    name_list

    Returns
    -------

    """
    res = ""
    for name in name_list:
        res += f"\n\t{name}"
    return res


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
    default_content = ["CODE", "DOCS", "DATA", "other"]
    terminals = ["", "!", "?"]
    tar_names = []

    current_dir = Path("./")
    dir_name = current_dir.resolve().name
    date = datetime.now().strftime("%Y%m%d")
    name = get_response("What is the name of this package?", default=dir_name)
    version = get_response("What is the package version? e.g. v1.0, v1r0")
    suffix = get_response("What type of archive do you want to create?",
                          choices=["tar", "tar.gz", "tar.bz2", "tar.xz"],
                          default="tar.gz")
    num_tars = int(get_response("How many archives should be made?", default='3'))
    # TODO: Replace with config default template
    tar_template = f"{name}_[CONTENT]_{date}.{suffix}"

    # Get tar content
    for i in range(num_tars):
        content = get_response(question=f"What is the content of the {ordinal(i+1)} archive?",
                               choices=default_content,
                               default=default_content[i])
        custom_type = None
        if content == "other":
            custom_type = get_response("What is the custom type?")

        if custom_type:
            tar_names.append(insert_into(tar_template, custom_type))
        tar_names.append(insert_into(tar_template, content))

    print(f"Date: {date}")
    print(f"Name: {name}")
    print(f"Version: {version}")
    print(f"Tar Names: {__name_list_fmt(tar_names)}")

    store_str = get_response("Where would you like to store the tars?",
                             default=config["default_release_dir"])
    store = parse_path(path=store_str, DATE=date, NAME=name, VERSION=version)
    store.mkdir(exist_ok=True, parents=True)
    config = {
        "date": date,
        "name": name,
        "version": version,
        "numtars": num_tars,
        "storestr": store_str,
        # TODO: Make sure that this works across OS
        "storepath": store.as_posix(),
        "archivetype": suffix,
        "tars": {}
    }

    for tar in tar_names:
        print(f"{tar}:")
        data = "start"
        config["tars"][tar] = []
        while data not in terminals:
            data = get_response("Path to include:")
            if data.strip() or data not in terminals:
                path = Path(data)
                if not path.resolve().exists():
                    print(f"{path} does not exist or could not be found.")
                    continue
                config["tars"][tar].append(path.relative_to('.').as_posix())

    make_tarfiles(config)

    config_res = get_response("Do you want to save this configuration to a file?",
                              default='n', choices=['y', 'n'])
    if config_res == 'y':
        config_str = get_response("Where would you like to save this config?",
                                  default=f"./{name}.mkpkg-conf")
        config_path = parse_path(path=config_str, DATE=date, NAME=name,
                                 VERSION=version)
        with open(config_path, mode="w+", encoding="utf-8") as file:
            yaml.safe_dump(config, stream=file)
