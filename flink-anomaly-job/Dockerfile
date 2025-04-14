FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir apache-flink

# Add Flink CLI to PATH
ENV PATH="${PATH}:/root/.local/lib/python3.10/site-packages/pyflink/bin"

# Copy the job
COPY flink_anomalies.py .

# Submit the job
CMD ["flink", "run", "-py", "/app/flink_anomalies.py", "-m", "flink-jobmanager:8081"]
