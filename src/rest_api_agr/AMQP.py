import threading

from .functions import count_unique_visits
from .configuration import LOGGER, define_connection, CHANNEL


def run_amqp():
    """
    Start a AMQP queue

    :return: Nothing
    """
    define_connection()

    def callback(ch, method, properties,
                 body: bytes = b''):
        """
        This function is called when the message has arrived


        :param ch: channel
        :param method:
        :param properties:
        :param body: message

        :return:
        """
        try:
            if body == b'stop_consuming':
                """ or ch.stop_consuming """
                CHANNEL.stop_consuming()
            else:
                try:
                    user, base_url, meth = body.decode('utf8').split('-')

                    LOGGER.debug(f'VISITS: The user {user} has visited the url {base_url} '
                                 f'under the method {meth}')

                    count_unique_visits(base_url=base_url, user=user)

                except ValueError:
                    LOGGER.debug(body.decode('utf8'))
        except Exception as e:
            LOGGER.error('Error doing things. {}'.format(e))

        CHANNEL.basic_ack(method.delivery_tag)

    CHANNEL.basic_consume(
        queue='api_amqp',
        on_message_callback=callback,
        auto_ack=False)

    LOGGER.info(' [*] Waiting for messages.')
    CHANNEL.basic_qos(prefetch_count=1)
    CHANNEL.start_consuming()


def declare_thread_ampq() -> None:
    """
    Just declare the amqp thread.

    :return: Nothing
    """

    th = threading.Thread(target=run_amqp,
                          name='Thread_AMPQ',
                          )
    th.start()
