FROM flink:1.17

USER root
WORKDIR /app

# ✅ Install Python + pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip curl && \
    ln -sf /usr/bin/python3 /usr/bin/python

# ✅ Install PyFlink that matches Flink runtime
RUN pip3 install --no-cache-dir apache-flink==1.17.1


# ✅ Add Kafka + JSON connectors using shaded JARs in plugin structure
RUN mkdir -p /opt/flink/plugins/kafka && \
    curl -fLo /opt/flink/plugins/kafka/flink-connector-kafka-1.17.0-shaded.jar \
      https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/1.17.0/flink-connector-kafka-1.17.0-shaded.jar && \
    curl -fLo /opt/flink/plugins/kafka/flink-json-1.17.2.jar \
      https://repo1.maven.org/maven2/org/apache/flink/flink-json/1.17.2/flink-json-1.17.2.jar



# ✅ Debug: confirm JARs are present
RUN ls -lh /opt/flink/lib

# ✅ Copy your PyFlink job
COPY flink_anomalies.py .

# ✅ Submit job to Flink cluster
CMD ["flink", "run", "-py", "/app/flink_anomalies.py", "-m", "flink-jobmanager:8081"]
