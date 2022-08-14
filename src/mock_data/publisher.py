from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from confluent_kafka.avro.cached_schema_registry_client import (
    CachedSchemaRegistryClient,
)
from settings import KAFKA_PRODUCER_CONFIG, SCHEMA_REGISTRY_CONFIG
from typing import Dict, List


def delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush()."""
    if err is not None:
        print("Message delivery failed: {}".format(err))
    else:
        print(
            "Message delivered to {} [{}]".format(msg.topic(), msg.partition())
        )


def bulk_publish(value_schema: str, values: List[Dict]):
    value_schema = avro.loads(value_schema)

    avroProducer = AvroProducer(
        KAFKA_PRODUCER_CONFIG,
        default_value_schema=value_schema,
        schema_registry=CachedSchemaRegistryClient(SCHEMA_REGISTRY_CONFIG),
    )
    for value in values:

        avroProducer.produce(
            topic="user", value=value, on_delivery=delivery_report
        )
    avroProducer.flush()
