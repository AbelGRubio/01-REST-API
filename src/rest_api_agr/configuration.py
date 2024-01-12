"""
    This module is to define the global parameters



eeempty
"""

import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

from fastapi import FastAPI, HTTPException


APP = FastAPI()

UNIQUE_URL_VISITS = {}

LOGGER_NAME = "fastapi"


def set_logger() -> logging.Logger:
    """
    Start a logger in debug level to know what happening in the programme.
    Create a logger for each day.

    :return: An initialize logger
    """

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    folder = 'log'
    if not os.path.exists(folder):
        os.mkdir(folder)
    fh = TimedRotatingFileHandler(os.path.join(folder,
                                               '.'.join([LOGGER_NAME, folder])),
                                  when='midnight')
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s '
                                  # '[%(processName)s:%(threadName)s]'
                                  # '<.%(funcName)s>'
                                  ' %(message)s',
                                  datefmt='%d/%b/%Y %H:%M:%S')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger


LOGGER = set_logger()