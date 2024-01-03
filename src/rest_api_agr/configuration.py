"""
    This module is to define the global parameters



eeempty
"""

import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

import pika
from flask import Flask

APP = Flask(__name__)
UNIQUE_URL_VISITS = {}

CONNECTION, CHANNEL = None, None


PROCESS_RUNNING = {}
STATUS_MANAGEMENT = True
STATUS_CHANNEL = True


def define_connection():
    global CONNECTION, CHANNEL

    CONNECTION = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost',
                                  port=5672,
                                  heartbeat=10))
    CHANNEL = CONNECTION.channel(channel_number=0)
    CHANNEL.queue_declare(queue='api_amqp', durable=False)


LOGGER_NAME = "amqp_api"


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