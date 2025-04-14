FROM apache/flink:1.17-python

COPY flink_anomaly_detection.py /app/flink_anomaly_detection.py
WORKDIR /app

CMD ["pyflink", "job", "run", "/app/flink_anomaly_detection.py", "--jobmanager", "flink-jobmanager:8081"]
