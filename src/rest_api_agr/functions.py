"""
    This module is to register useful functions.


    emtpy

"""
import time
from flask import request

from .configuration import UNIQUE_URL_VISITS


def count_unique_visits(base_url: str = '',
                        user: str = '') -> None:
    """
    Count the unique visit on the website

    :param base_url: url to count the visits
    :param user: id of the user

    :return: Nothing
    """

    if base_url in UNIQUE_URL_VISITS:
        if user not in UNIQUE_URL_VISITS[base_url]:
            UNIQUE_URL_VISITS[base_url].append(user)
    else:
        UNIQUE_URL_VISITS[base_url] = [user]


def record_visit() -> (str, str, str):
    """
    Function that register who is visit the path

    :return: tuple with basic information
    """

    meth = request.method
    user = request.remote_addr
    base_url = request.base_url

    CHANNEL.basic_publish(
        exchange='',
        routing_key='api_amqp',
        body='{}-{}-{}'.format(user, base_url, meth))

    return base_url, meth, user

