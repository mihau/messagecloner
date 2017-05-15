import logging

from kombu import Queue, Consumer, Exchange


logger = logging.getLogger(__name__)
logging.getLogger("boto").setLevel(logging.WARNING)
logging.getLogger("kombu").setLevel(logging.WARNING)


class Cloner(object):
    def __init__(self, source_connection, target_connection,
                 source_exchange_name, target_queue_name,
                 intermediate_queue_name=None):

        self.source_connection = source_connection
        self.target_connection = target_connection
        self.source_exchange_name = source_exchange_name
        self.target_queue_name = target_queue_name
        self.intermediate_queue_name = (
            intermediate_queue_name or source_exchange_name + '_cloner'
        )

    def __str__(self):
        return (
            '{} @ {} > {} @ {}'.format(
                self.source_exchange_name, self.source_connection,
                self.target_queue_name, self.target_connection,
            )
        )

    def _setup_queues(self):
        src_channel = self.source_connection.channel()
        self.intermediate_queue = Queue(
            name=self.intermediate_queue_name,
            exchange=Exchange(self.source_exchange_name),
            routing_key=self.source_exchange_name,
            channel=src_channel,
            auto_delete=False,
        )
        self.intermediate_queue.declare()

        self.target_queue = self.target_connection.SimpleQueue(
            self.target_queue_name
        )

    def copy_message(self, body, msg):
        logger.debug('{} - Copying message {}'.format(self, body))
        self.target_queue.put(body)
        msg.ack()

    def clone(self):
        self._setup_queues()
        src_channel = self.source_connection.channel()
        Consumer(
            src_channel,
            self.intermediate_queue,
            callbacks=[self.copy_message],
        ).consume()
