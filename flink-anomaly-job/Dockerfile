FROM python:3.10-slim

WORKDIR /app

# Install Java and other required deps for PyFlink runtime
RUN apt-get update && \
    apt-get install -y default-jdk curl && \
    pip install --no-cache-dir apache-flink==1.18.0

# Set Java env vars for Flink
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Copy your PyFlink job
COPY flink_anomalies.py .

# Submit the job using the PyFlink CLI
CMD ["python", "-m", "pyflink.datastream", "/app/flink_anomalies.py", "--jobmanager", "flink-jobmanager:8081"]