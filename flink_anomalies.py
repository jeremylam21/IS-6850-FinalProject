from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.window import Tumble
from pyflink.table.expressions import col, lit, expr

# 1. Set up streaming environment
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

# 2. Define source table (Kafka)
table_env.execute_sql("""
CREATE TABLE stock_trades (
    ticker STRING,
    price DOUBLE,
    volume INT,
    event_type STRING,
    trader_id STRING,
    event_time TIMESTAMP_LTZ(3),
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'stock_events',
    'properties.bootstrap.servers' = 'localhost:9092',
    'format' = 'json',
    'scan.startup.mode' = 'earliest-offset'
)
""")

table_env.execute_sql("""
CREATE TABLE flagged_trades (
    ticker STRING,
    price DOUBLE,
    volume INT,
    event_type STRING,
    trader_id STRING,
    event_time TIMESTAMP_LTZ(3),
    avg_price DOUBLE,
    price_std DOUBLE,
    avg_volume DOUBLE,
    vol_std DOUBLE,
    anomaly_flag STRING
) WITH (
    'connector' = 'kafka',
    'topic' = 'stock_anomalies',
    'properties.bootstrap.servers' = 'localhost:9092',
    'format' = 'json',
    'sink.partitioner' = 'round-robin',
    'scan.startup.mode' = 'earliest-offset'
)
""")


# 3. Create a Table object for stock_trades
stock_trades = table_env.from_path("stock_trades")

# 4. Create windowed aggregation: trade_stats
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

# 5. Register it for reuse
table_env.create_temporary_view("trade_stats", trade_stats)

# 6. Create and register base view as well
table_env.create_temporary_view("stock_trades_view", stock_trades)

# 7. Use SQL to join and apply anomaly logic (better syntax handling)
table_env.execute_sql("""
CREATE TEMPORARY VIEW trade_with_flags AS
SELECT
  t.ticker,
  t.price,
  t.volume,
  t.event_type,
  t.trader_id,
  t.event_time,
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

# 8. Push results to new table linked to Kafka new topic
table_env.execute_sql("""
INSERT INTO flagged_trades
SELECT * FROM trade_with_flags
""")