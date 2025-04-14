from pyflink.table import EnvironmentSettings, TableEnvironment

env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

print("🛠️ START: Attempting to create Kafka table...")

table_env.execute_sql("""
CREATE TABLE stock_trades (
    value STRING
) WITH (
    'connector' = 'kafka',
    'topic' = 'stock_events',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json',
    'scan.startup.mode' = 'earliest-offset'
)
""")

print("✅ Kafka connector worked!")
