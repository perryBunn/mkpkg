"""
Name:           logger.py
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
import sys
from datetime import datetime
from logging import Logger
from pathlib import Path

import logging

class ColoredFormatter(logging.Formatter):
    """ Logging colored formatter
        Adapted from Alexandra Zaharia, who adapted
        this post https://stackoverflow.com/a/56944256/3638629
    """

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.formats = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(config) -> Logger:
    """
      Method will return a logging object with stdout and file handlers

      Parameters:
      None

      Returns:
      Logger: logging.Logger object
    """
    log = logging.getLogger("mkpkg")
    log.setLevel("DEBUG")

    fmt = "%(asctime)s: %(name)s: %(levelname)s: %(message)s"

    # Time formatted as YYYYmmddHHMM
    date = datetime.now()
    time = date.strftime("%Y%m%d%H%M")

    log_dir = Path(f"{config['logging_dir']}/{time[:8]}/").expanduser()
    try:
        log_dir.mkdir(exist_ok=True, parents=True)
    except PermissionError:
        if input(f"Couldnt create {log_dir}, do you want to continue without "
                 f"file logs? [N/y] ").lower() != "y":
            sys.exit(2)
    else:
        file_name = (log_dir / f"{time}_mkpkg.log").as_posix()
        file_handle = logging.FileHandler(file_name, encoding="utf-8")
        file_handle.setLevel(config["file_level"])
        file_fmt = logging.Formatter(fmt)
        file_handle.setFormatter(file_fmt)
        log.addHandler(file_handle)

    stream_handle = logging.StreamHandler()
    stream_handle.setLevel(config["stream_level"])

    stream_fmt = ColoredFormatter(fmt)
    stream_handle.setFormatter(stream_fmt)

    log.addHandler(stream_handle)

    return log
