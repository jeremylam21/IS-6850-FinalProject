FROM flink:1.17

USER root
WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip curl unzip && \
    ln -sf /usr/bin/python3 /usr/bin/python

RUN pip3 install --no-cache-dir apache-flink==1.17.1

RUN mkdir -p /opt/flink/plugins/kafka && \
    curl -fLo /opt/flink/plugins/kafka/flink-sql-connector-kafka-1.17.1.jar \
    https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/1.17.1/flink-sql-connector-kafka-1.17.1.jar

COPY flink_anomalies.py /app/flink_anomalies.py

ENV FLINK_PLUGINS_DIR=/opt/flink/plugins

CMD ["flink", "run", "-py", "/app/flink_anomalies.py", "-m", "flink-jobmanager:8081"]