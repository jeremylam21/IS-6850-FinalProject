from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import os

# --- Kafka Setup ---
consumer = KafkaConsumer(
    os.getenv("KAFKA_TOPIC","stock_anomalies"),
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id=os.getenv("KAFKA_GROUP_ID", "anomaly-writer-group")
)

# --- InfluxDB Setup ---
bucket = os.getenv("INFLUX_BUCKET", "stock_data")
org = os.getenv("INFLUX_ORG", "default-org")
token = os.getenv("INFLUX_TOKEN", "mytoken")
url = os.getenv("INFLUX_URL", "http://influxdb:8086")

influx = InfluxDBClient(url=url, token=token, org=org)
write_api = influx.write_api(write_options=SYNCHRONOUS)


# --- Process Messages ---
for message in consumer:
    data = message.value

    point = (
        Point("anomaly_events")
        .tag("ticker", data["ticker"])
        .tag("event_type", data["event_type"])
        .tag("anomaly_flag", data.get("anomaly_flag", "unknown"))
        .field("price", float(data["price"]))
        .field("volume", int(data["volume"]))
        .field("avg_price", float(data.get("avg_price", 0)))
        .field("price_std", float(data.get("price_std", 0)))
        .field("avg_volume", float(data.get("avg_volume", 0)))
        .field("vol_std", float(data.get("vol_std", 0)))
    )

    write_api.write(bucket=bucket, org=org, record=point)
    print(f"Wrote: {data['ticker']} - {data['anomaly_flag']}")
