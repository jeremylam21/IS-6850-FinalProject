from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'stock_events',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='test-group'
)

print("Listening for stock_events...\n")

for message in consumer:
    print(message.value)
