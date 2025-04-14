from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.window import Tumble
from pyflink.table.expressions import col, lit

env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

import os
print("🛠️ FLINK_PLUGINS_DIR =", os.environ.get("FLINK_PLUGINS_DIR"))

# ✅ Define raw source table with STRING timestamp
table_env.execute_sql("""
CREATE TABLE stock_trades (
    ticker STRING,
    price DOUBLE,
    volume INT,
    event_type STRING,
    trader_id STRING,
    `timestamp` STRING,
    WATERMARK FOR `timestamp` AS TO_TIMESTAMP_LTZ(`timestamp`, 0) - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'stock_events',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json',
    'scan.startup.mode' = 'earliest-offset',
    'json.timestamp-format.standard' = 'ISO-8601'
)
""")

# ✅ Sink table
table_env.execute_sql("""
CREATE TABLE flagged_trades (
    ticker STRING,
    price DOUBLE,
    volume INT,
    event_type STRING,
    trader_id STRING,
    `timestamp` TIMESTAMP_LTZ(3),
    avg_price DOUBLE,
    price_std DOUBLE,
    avg_volume DOUBLE,
    vol_std DOUBLE,
    anomaly_flag STRING
) WITH (
    'connector' = 'kafka',
    'topic' = 'stock_anomalies',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json',
    'sink.partitioner' = 'round-robin',
    'scan.startup.mode' = 'earliest-offset'
)
""")

# ✅ Create view with parsed timestamp
table_env.execute_sql("""
CREATE TEMPORARY VIEW stock_trades_view AS
SELECT
  ticker,
  price,
  volume,
  event_type,
  trader_id,
  TO_TIMESTAMP_LTZ(`timestamp`, 0) AS event_time
FROM stock_trades
""")

# ✅ Use event_time for windowing
stock_trades = table_env.from_path("stock_trades_view")

trade_stats = stock_trades.window(
    Tumble.over(lit(1).minute).on(col("event_time")).alias("w")
).group_by(
    col("ticker"), col("w")
).select(
    col("ticker"),
    col("w").start.alias("window_start"),
    col("price").avg.alias("avg_price"),
    col("price").stddev_pop.alias("price_std"),
    col("volume").avg.alias("avg_volume"),
    col("volume").stddev_pop.alias("vol_std")
)

table_env.create_temporary_view("trade_stats", trade_stats)

# ✅ Join logic using parsed event_time
table_env.execute_sql("""
CREATE TEMPORARY VIEW trade_with_flags AS
SELECT
  t.ticker,
  t.price,
  t.volume,
  t.event_type,
  t.trader_id,
  t.event_time AS `timestamp`,
  s.avg_price,
  s.price_std,
  s.avg_volume,
  s.vol_std,
  CASE
    WHEN ABS(t.price - s.avg_price) > 2 * s.price_std THEN 'price_outlier'
    WHEN t.volume > s.avg_volume + 2 * s.vol_std THEN 'volume_spike'
    ELSE 'normal'
  END AS anomaly_flag
FROM stock_trades_view t
JOIN trade_stats s
ON t.ticker = s.ticker
AND FLOOR(t.event_time TO MINUTE) = s.window_start
""")

# ✅ Write to Kafka sink
table_env.execute_sql("""
INSERT INTO flagged_trades
SELECT * FROM trade_with_flags
""")
