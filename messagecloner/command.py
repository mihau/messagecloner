import argparse
import logging
import sys
import json

from kombu import Connection

from messagecloner.cloner import Cloner

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    parser = argparse.ArgumentParser(description="Message cloner.")
    parser.add_argument('source_broker_url', help='address of source broker')
    parser.add_argument('target_broker_url', help='address of target broker')
    parser.add_argument(
        '--source-transport-options', type=json.loads
    )
    parser.add_argument(
        '--target-transport-options', type=json.loads
    )
    parser.add_argument(
        '--exchange-queue-pair',
        nargs=2,
        action='append',
        required=True,
    )

    args = parser.parse_args()

    with Connection(args.source_broker_url) as src_conn, Connection(args.target_broker_url, transport_options=args.target_transport_options) as dst_conn:
        for source_exchange, target_queue in args.exchange_queue_pair:
            cloner = Cloner(
                source_broker_url=args.source_broker_url,
                target_broker_url=args.target_broker_url,
                source_exchange_name=source_exchange,
                target_queue_name=target_queue,
                target_transport_options={'region': 'us-west-2'},
            )
            logger.info('Setting up cloner: {}'.format(cloner))

            cloner.clone(src_conn, dst_conn)

        while True:
            src_conn.drain_events()
