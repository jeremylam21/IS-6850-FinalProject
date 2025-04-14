FROM python:3.10-slim

WORKDIR /app

# Install PyFlink
RUN pip install --no-cache-dir apache-flink

# Copy the PyFlink job script
COPY flink_anomalies.py .

# Submit the job to the running Flink cluster
CMD ["pyflink", "job", "run", "/app/flink_anomalies.py", "--jobmanager", "flink-jobmanager:8081"]

