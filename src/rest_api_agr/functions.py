"""
    This module is to register useful functions.


    emtpy

"""
import time
from flask import request

from .configuration import (
    LOGGER, LOGGER_NAME, UNIQUE_URL_VISITS, CHANNEL,
    STATUS_CHANNEL, define_connection, STATUS_MANAGEMENT)


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


def record_message(message: str) -> bool:
    """
    Function that register who is visit the path

    :return: tuple with basic information
    """

    state = True
    try:
        CHANNEL.basic_publish(
            exchange='',
            routing_key='api_amqp',
            body=message)
    except Exception as e:
        print(e)
        state = False

    return state


def read_logger_visits() -> list:
    """
    Read the logger to show the visit history.
    If the file not exists, the function will return

        'No history visit yet'

    :return: a list of visits
    """
    try:

        with open(r'log/{}.log'.format(LOGGER_NAME), 'r') as f:
            lines = f.readlines()

        lines = [line for line in lines if ' VISITS: ' in line]

    except FileNotFoundError:
        LOGGER.warning('No history visit yet')
        lines = ['No history visit yet']

    return lines


def process_management() -> None:
    count_time = 0

    define_connection()

    time.sleep(1)
    # set_channel_pika(channel_pika)

    record_message('Starting process management')

    while STATUS_MANAGEMENT:
        record_message('Doing stuff on process management. Time {}'.format(count_time))
        time.sleep(5)
        count_time += 1

    record_message('Finishing process management')
    CHANNEL.stop_consuming()

    return None


def process_channel(
        num_channel: int) -> None:
    count_time = 0

    define_connection()

    time.sleep(1)

    record_message('Starting process channel {}'.format(num_channel))

    while STATUS_CHANNEL:
        record_message('Doing stuff on process channel {}. '
                       'Time {}'.format(num_channel, count_time))
        time.sleep(1)
        count_time += 1

    record_message('Finishing process channel {}'.format(num_channel))

    CHANNEL.stop_consuming()

