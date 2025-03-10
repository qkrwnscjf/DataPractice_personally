import requests
import json
import time
from kafka import KafkaProducer

API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"
STOCK_SYMBOL = "AAPL"
KAFKA_TOPIC = "stock_prices"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def fetch_stock_data():
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={STOCK_SYMBOL}&interval=1min&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json().get("Time Series (1min)", {})

    for timestamp, values in data.items():
        stock_data = {
            "timestamp": timestamp,
            "symbol": STOCK_SYMBOL,
            "open": values["1. open"],
            "high": values["2. high"],
            "low": values["3. low"],
            "close": values["4. close"],
            "volume": values["5. volume"]
        }
        producer.send(KAFKA_TOPIC, stock_data)
        print(f"Sent: {stock_data}")

if __name__ == "__main__":
    while True:
        fetch_stock_data()
        time.sleep(60)  # 1분 간격으로 데이터 수집
