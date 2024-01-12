"""
    This module is used for define the REST API endpoints



"""

from flask import jsonify

from .functions import record_visit
from .configuration import APP


@APP.route('/')
def main_route():
    """
    Example main route

    :return: a json file
    """

    base_url, meth, _ = record_visit()

    return jsonify(f'You have visited {base_url} under the method {meth}')


@APP.route('/start_<channel_num>')
def start_endpoint(channel_num: str):
    """
    Example path 1 route

    :return: a json file
    """

    base_url, meth, _ = record_visit()

    name_process = 'process-{}'.format(channel_num)

    return jsonify(f'You have visited {base_url} under the method {meth} '
                   f'and you started the process channel {channel_num}')


@APP.route('/stop_<channel_num>')
def stop_endpoint(channel_num: str):
    """
    Example path 2 route

    :return: a json file
    """

    base_url, meth, _ = record_visit()

    name_process = 'process-{}'.format(channel_num)

    return jsonify(f'You have visited {base_url} under the method {meth}'
                   f'and you finished the process channel {channel_num}')


@APP.route('/restart_<channel_num>')
def restart_endpoint(channel_num: str):
    """
    Example sub-path from path 1

    :return: a json file
    """

    base_url, meth, _ = record_visit()

    return jsonify(f'You have visited {base_url} under the method {meth}')


@APP.route('/result_<channel_num>')
def result_endpoint(channel_num: str):

    base_url, meth, _ = record_visit()

    return jsonify(f'You have visited {base_url} under the method {meth}')

