FROM flink:1.17

USER root
WORKDIR /app

# Install Python and dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip curl && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    pip3 install --no-cache-dir apache-flink==1.17.1

# ✅ Place Kafka + JSON connector JARs into FLINK_LIB_DIR
RUN curl -fLo /opt/flink/lib/flink-sql-connector-kafka-1.17.1.jar \
      https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/1.17.1/flink-sql-connector-kafka-1.17.1.jar && \
    curl -fLo /opt/flink/lib/flink-json-1.17.1.jar \
      https://repo1.maven.org/maven2/org/apache/flink/flink-json/1.17.1/flink-json-1.17.1.jar

# Copy your PyFlink job into the image
COPY flink_anomalies.py .

# Optional: debug what JARs are available
RUN ls -lh /opt/flink/lib

# Run the job against the jobmanager
CMD ["flink", "run", "-py", "/app/flink_anomalies.py", "-m", "flink-jobmanager:8081"]
