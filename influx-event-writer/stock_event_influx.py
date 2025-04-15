from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import json

# Create Kafka consumer
consumer = KafkaConsumer(
    os.getenv("KAFKA_TOPIC", "stock_events"),                      # Topic name
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"), # Your Kafka broker
    auto_offset_reset='earliest',       # Read from the beginning
    enable_auto_commit=True,
    group_id=os.getenv("KAFKA_GROUP_ID", "event-writer-group"),
    value_deserializer=lambda x: json.loads(x.decode('utf-8')) # Parse JSON
)

# --- InfluxDB Setup ---
bucket = os.getenv("INFLUX_BUCKET", "stock_data")
org = os.getenv("INFLUX_ORG", "default-org")
token = os.getenv("INFLUX_TOKEN", "mytoken")
url = os.getenv("INFLUX_URL", "http://influxdb:8086")

influx = InfluxDBClient(url=url, token=token, org=org)
write_api = influx.write_api(write_options=SYNCHRONOUS)

# Loop through messages
for message in consumer:
    data = message.value

    point = (
        Point("stock_events")
        .tag("ticker", data["ticker"])
        .tag("event_type", data["event_type"])
        .field("price", float(data["price"]))
        .field("volume", int(data["volume"]))
        .time(data["timestamp"])
    )

    write_api.write(bucket=bucket, org=org, record=point)