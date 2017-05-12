import logging

from kombu import Queue, Connection, Consumer, Exchange


logger = logging.getLogger(__name__)
logging.getLogger("boto").setLevel(logging.WARNING)
logging.getLogger("kombu").setLevel(logging.WARNING)


class Cloner(object):
    def __init__(self, source_broker_url, target_broker_url,
                 source_exchange_name, target_queue_name,
                 target_transport_options=None, intermediate_queue_name=None):

        self.source_broker_url = source_broker_url
        self.target_broker_url = target_broker_url
        self.source_exchange_name = source_exchange_name
        self.target_queue_name = target_queue_name
        self.target_transport_options = target_transport_options
        self.intermediate_queue_name = (
            intermediate_queue_name or source_exchange_name + '_cloner'
        )

    def __str__(self):
        return (
            '{} @ {} > {} @ {}'.format(
                self.source_exchange_name, self.source_broker_url,
                self.target_queue_name, self.target_broker_url
            )
        )

    def _setup_queues(self, src_conn, dst_conn):
        src_channel = src_conn.channel()
        self.intermediate_queue = Queue(
            name=self.intermediate_queue_name,
            exchange=Exchange(self.source_exchange_name),
            routing_key=self.source_exchange_name,
            channel=src_channel,
            auto_delete=False,
        )
        self.intermediate_queue.declare()

        self.target_queue = dst_conn.SimpleQueue(self.target_queue_name)

    def copy_message(self, body, msg):
        logger.debug('{} - Copying message {}'.format(self, body))
        self.target_queue.put(body)
        msg.ack()

    def clone(self):
        with Connection(self.source_broker_url) as src_conn, Connection(self.target_broker_url, transport_options=self.target_transport_options) as dst_conn:
            self._setup_queues(src_conn, dst_conn)
            src_channel = src_conn.channel()
            self.target_queue.put({'test': 'ting'})
            with Consumer(src_channel, self.intermediate_queue, callbacks=[self.copy_message]):
                while True:
                    src_conn.drain_events()
