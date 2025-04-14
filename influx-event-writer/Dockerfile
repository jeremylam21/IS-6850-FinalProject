FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir kafka-python influxdb-client

COPY stock_event_influx.py .

CMD ["python", "stock_event_influx.py"]