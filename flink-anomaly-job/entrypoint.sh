#!/bin/bash

echo "🟢 Starting Flink JobManager..."
/docker-entrypoint.sh jobmanager &

# Wait for Flink JobManager REST API to be ready
echo "⏳ Waiting for Flink REST API..."
until curl -s localhost:8081/overview; do
  sleep 2
done

echo "🚀 Submitting PyFlink job..."
flink run -py /app/flink_anomalies.py
wait

chmod +x flink-anomaly-job/entrypoint.sh