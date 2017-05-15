import argparse
import logging
import sys
import json
import os
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

    source_broker_credentials = os.getenv('SOURCE_BROKER_CREDENTIALS')
    target_broker_credentials = os.getenv('TARGET_BROKER_CREDENTIALS')
    source_user, source_password = (
        source_broker_credentials.split(':') if source_broker_credentials
        else (None, None)
    )
    target_user, target_password = (
        target_broker_credentials.split(':') if target_broker_credentials
        else (None, None)
    )

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
                userid=source_user,
                password=source_password,
            )
        )
        dst_conn = stack.enter_context(
            Connection(
                args.target_broker_url,
                transport_options=args.target_transport_options,
                userid=target_user,
                password=target_password,
            )
        )

        for source_exchange, target_queue in args.exchange_queue_pair:
            cloner = Cloner(
                source_connection=src_conn,
                target_connection=dst_conn,
                source_exchange_name=source_exchange,
                target_queue_name=target_queue,
            )
            logger.info('Setting up cloner: {}'.format(cloner))

            cloner.clone()

        logger.info('Starting cloners')
        while True:
            src_conn.drain_events()
