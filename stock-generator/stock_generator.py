import time
import random
import json
from datetime import datetime, timedelta, UTC
from faker import Faker

# Initialize Faker for trader IDs
faker = Faker()

TICKERS = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
DURATION_MINUTES = 20
SLEEP_SECONDS = 1  # adjust for more/less frequent events

def generate_trade_events():
    end_time = datetime.now(UTC) + timedelta(minutes=DURATION_MINUTES)
    price_memory = {ticker: random.uniform(100, 300) for ticker in TICKERS}

    while datetime.now(UTC) < end_time:
        stock = random.choice(TICKERS)

        # Random walk for price movement
        last_price = price_memory[stock]
        new_price = round(last_price + random.uniform(-1.5, 1.5), 2)
        price_memory[stock] = max(new_price, 0.01)

        event = {
            "ticker": stock,
            "price": price_memory[stock],
            "volume": random.randint(10, 1000),
            "event_type": random.choice(["buy", "sell"]),
            "trader_id": str(random.randint(100000, 999999)),
            "timestamp": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S")
        }

        print(json.dumps(event))
        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    generate_trade_events()