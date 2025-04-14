FROM python:3.10-slim

WORKDIR /app

# Install Python dependencies directly
RUN pip install --no-cache-dir kafka-python influxdb-client

# Copy your writer script
COPY stock_anomalies_influx.py .

CMD ["python", "stock_anomalies_influx.py"]
