FROM python:3.10-slim

WORKDIR /app

# Install PyFlink
RUN pip install --no-cache-dir apache-flink

# Copy the PyFlink job script
COPY flink_anomaly_detection.py .

# Submit the job to the running Flink cluster
CMD ["pyflink", "job", "run", "/app/flink_anomaly_detection.py", "--jobmanager", "flink-jobmanager:8081"]

