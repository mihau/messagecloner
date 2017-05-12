import argparse
import logging
import sys


from messagecloner.cloner import Cloner

logger = logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    parser = argparse.ArgumentParser(description="Message cloner.")
    parser.add_argument('source_broker_url', help='address of source broker')
    parser.add_argument('target_broker_url', help='address of target broker')
    parser.add_argument(
        'source_exchange_name',
        help='name of the exchange to copy messages from',
    )
    parser.add_argument(
        'target_queue_name',
        help='name of the queue to copy messages to',
    )

    args = parser.parse_args()

    cloner = Cloner(
        source_broker_url=args.source_broker_url,
        target_broker_url=args.target_broker_url,
        source_exchange_name=args.source_exchange_name,
        target_queue_name=args.target_queue_name,
        target_transport_options={'region': 'us-west-2'},
    )

    cloner.clone()

