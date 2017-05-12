import argparse
import logging
import sys
import json
from contextlib import ExitStack

from kombu import Connection

from messagecloner.cloner import Cloner

logger = logging.getLogger(__name__)


def main():

    parser = argparse.ArgumentParser(description="Message cloner.")
    parser.add_argument('source_broker_url', help='address of source broker')
    parser.add_argument('target_broker_url', help='address of target broker')
    parser.add_argument('--source-transport-options', type=json.loads)
    parser.add_argument('--target-transport-options', type=json.loads)
    parser.add_argument('--exchange-queue-pair', nargs=2, action='append',
                        required=True)
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")

    args = parser.parse_args()

    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG if args.verbose else logging.INFO
    )

    with ExitStack() as stack:
        src_conn = stack.enter_context(
            Connection(
                args.source_broker_url,
                transport_options=args.source_transport_options,
            )
        )
        dst_conn = stack.enter_context(
            Connection(
                args.target_broker_url,
                transport_options=args.target_transport_options,
            )
        )

        for source_exchange, target_queue in args.exchange_queue_pair:
            cloner = Cloner(
                source_broker_url=args.source_broker_url,
                target_broker_url=args.target_broker_url,
                source_exchange_name=source_exchange,
                target_queue_name=target_queue,
            )
            logger.info('Setting up cloner: {}'.format(cloner))

            cloner.clone(src_conn, dst_conn)

        logger.info('Starting cloners')
        while True:
            src_conn.drain_events()
