from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json

# --- Kafka Setup ---
consumer = KafkaConsumer(
    'stock_anomalies',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='influx-writer'
)

# --- InfluxDB Setup ---
bucket = "stock_data"
org = "default-org"
token = "mytoken"
url = "http://influxdb:8086"

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
