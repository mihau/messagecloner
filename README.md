# messagecloner
Simple utility to copy messages from one message broker to another.

The tool was created to allow creating copies of messages published to one
broker and send them to another one (supported by kombu). It binds to specified
exchanges on the source broker and publishes the messages to corresponding
queues on the target broker.

## usage
For the usage please refer to `messagecloner --help`. Note that in addition it
is possible to specify broker credentials by setting `SOURCE_BROKER_CREDENTIALS`
and `TARGET_BROKER_CREDENTIALS` environment variables as `user:password`.

    usage: messagecloner [-h]
                         [--source-transport-options SOURCE_TRANSPORT_OPTIONS]
                         [--target-transport-options TARGET_TRANSPORT_OPTIONS]
                         --exchange-queue-pair EXCHANGE_QUEUE_PAIR
                         EXCHANGE_QUEUE_PAIR [-v]
                         source_broker_url target_broker_url

    Message cloner.

    positional arguments:
      source_broker_url     address of source broker
      target_broker_url     address of target broker

    optional arguments:
      -h, --help            show this help message and exit
      --source-transport-options SOURCE_TRANSPORT_OPTIONS
      --target-transport-options TARGET_TRANSPORT_OPTIONS
      --exchange-queue-pair EXCHANGE_QUEUE_PAIR EXCHANGE_QUEUE_PAIR
      -v, --verbose         increase output verbosity

### Example:
    messagecloner amqp://localhost:5672/my_vhost sqs:// --exchange-queue-pair my_first_exchange my_first_queue_clone --exchange-queue-pair my_second_exchange my_second_queue_clone --source-transport-options "{\"region\":\"us-east-1\"}"  -v
