FROM flink:1.17

USER root
WORKDIR /app

# ✅ Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    ln -sf /usr/bin/python3 /usr/bin/python

# ✅ Install PyFlink version that matches Flink runtime
RUN pip3 install --no-cache-dir apache-flink==1.17.1

# ✅ Copy your PyFlink job into the container
COPY flink_anomalies.py .

# ✅ Submit your job to the Flink JobManager via CLI
CMD ["flink", "run", "-py", "/app/flink_anomalies.py", "-m", "flink-jobmanager:8081"]