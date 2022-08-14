from typing import Any, Dict, List
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
import psycopg2
import psycopg2.extras

MAX_CHUNK_SIZE = 4


conn = psycopg2.connect(
    database="sampledb",
    host="localhost",
    user="baeldung",
    password="baeldung",
    port="5432"
)
cur = conn.cursor()

c = AvroConsumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'consumer-test',
    'schema.registry.url': 'http://127.0.0.1:8081',
    'auto.offset.reset': 'earliest',
    # To avoid commiting offset in local and always read messages from beggining
    'enable.auto.commit': False 
    })


def insert_to_database(conf: Dict[str, Any], bulk_data: List[Dict[str, Any]]):
    print('Inserting to DB...')
    data = []

    # TODO: Refactor this part
    for i in bulk_data:
        tmp = {k: i[k] for k in conf['event_field_to_table_mapping'].keys()}.values()
        data.append(tuple(tmp))

    db_tables = ','.join(conf['event_field_to_table_mapping'].values())
    query = f"INSERT INTO {conf['table_name']} ({db_tables}) values %s"
    psycopg2.extras.execute_values(
        cur, query, data
    )
    conn.commit()
    

def consume_and_process_message(conf: Dict[str, Any]):
    """
    Consume and insert messages from given topic to given
    database table.
    """
    # TODO: investigate to see how can we handle multiple topics multithreaded
    c.subscribe([conf['topic_name']])
    bulk_msg = []
    while True:
        print("Running")
        try:
            msg = c.poll(5)

        except SerializerError as e:
            print("Message deserialization failed for {}: {}".format(msg, e))
            break

        if msg is None:
            continue

        if msg.error():
            print("AvroConsumer error: {}".format(msg.error()))
            continue
        
        bulk_msg.append(msg.value())
        if len(bulk_msg) == MAX_CHUNK_SIZE:
            print('Inserting to db...')
            insert_to_database(conf, bulk_msg)
            bulk_msg.clear()



conf = {
    'topic_name': 'sea_vessel_position_reports',
    'table_name': 'sea_vessel_positions',
    'table_schema': [
        "id SERIAL PRIMARY KEY",
        "MMSI INTEGER",
        "Longitude real",
        "Latitude real",
        "Type char(1))"
    ],
    'event_field_to_table_mapping': {
        'MMSI': 'MMSI',
        'Longitude': 'Longitude',
        'Latitude': 'Latitude',
        'Type': 'Type'
    }
}

print("Starting...")

consume_and_process_message(conf)

c.close()