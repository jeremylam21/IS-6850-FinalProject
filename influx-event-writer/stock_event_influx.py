from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json

# Create Kafka consumer
consumer = KafkaConsumer(
    'stock_events',                      # Topic name
    bootstrap_servers='localhost:9092', # Your Kafka broker
    auto_offset_reset='earliest',       # Read from the beginning
    enable_auto_commit=True,
    group_id='stock-debug-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')) # Parse JSON
)

# --- InfluxDB Setup ---
bucket = "stock_data"
org = "default-org"
token = "mytoken"
url = "http://localhost:8086"

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