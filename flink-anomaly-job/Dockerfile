FROM flink:1.18

USER root
WORKDIR /app

# Install Python + PyFlink
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    pip3 install --no-cache-dir apache-flink==1.18.0

# Copy your PyFlink job
COPY flink_anomalies.py .

# Submit the job using Flink CLI (now included in this image)
CMD ["flink", "run", "-py", "/app/flink_anomalies.py", "-m", "flink-jobmanager:8081"]
