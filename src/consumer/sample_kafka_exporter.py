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

c.subscribe(['sea_vessel_position_reports'])


def insert_to_database(bulk_data: List[Dict[str, Any]]):
    data = [(i['MMSI'], i['Longitude'], i['Latitude'], str(i['Type'])) for i in bulk_data]

    query = 'INSERT INTO sea_vessel_positions (MMSI, Longitude, Latitude, Type) values %s'
    psycopg2.extras.execute_values(
        cur, query, data
    )
    conn.commit()
    

print("Starting...")


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
        insert_to_database(bulk_msg)
        bulk_msg.clear()

c.close()