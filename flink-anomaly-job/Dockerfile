FROM flink:1.17

USER root
WORKDIR /app

# ✅ Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip curl && \
    ln -sf /usr/bin/python3 /usr/bin/python

# ✅ Install PyFlink version that matches Flink
RUN pip3 install --no-cache-dir apache-flink==1.17.1

# ✅ Add Kafka & JSON connector JARs
RUN curl -o /opt/flink/lib/flink-connector-kafka.jar \
      https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/1.17.0/flink-connector-kafka-1.17.0.jar && \
    curl -o /opt/flink/lib/flink-json.jar \
      https://repo1.maven.org/maven2/org/apache/flink/flink-json/1.17.0/flink-json-1.17.0.jar

# ✅ Copy your PyFlink job into the container
COPY flink_anomalies.py .

# ✅ Submit your job
CMD ["flink", "run", "-py", "/app/flink_anomalies.py", "-m", "flink-jobmanager:8081"]
