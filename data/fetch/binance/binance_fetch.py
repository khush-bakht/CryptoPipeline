#data/fetch/binance/binance_fetch.py
import pandas as pd
import time
from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_SECRET_KEY")

client = Client(API_KEY, API_SECRET)


class BinanceFetcher:
    def __init__(self, symbol, interval, start_time, end_time="now"):
        symbol = symbol.upper()
        if not symbol.endswith('USDT'):
            symbol += 'USDT'
        self.symbol = symbol     
        self.interval = interval
        self.start_time = start_time
        self.end_time = end_time

    def get_klines(self):
        print(f"Fetching data (Binance) {self.symbol} {self.interval}...")
        all_data = []
        limit = 1000
        start_ts = int(pd.to_datetime(self.start_time).timestamp() * 1000)
        end_ts = int(pd.Timestamp.now().timestamp() * 1000) if self.end_time == "now" else int(pd.to_datetime(self.end_time).timestamp() * 1000)

        while True:
            klines = client.futures_klines(
                symbol=self.symbol,
                interval=self.interval,
                limit=limit,
                startTime=start_ts,
                endTime=end_ts
            )

            if not klines:
                break

            all_data.extend(klines)
            start_ts = klines[-1][6] + 1  # Next millisecond (Close time+1)
            time.sleep(0.2)  

            if start_ts >= end_ts:
                break

        # Convert to DataFrame
        df = pd.DataFrame(all_data, columns=[
            "datetime", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "num_trades",
            "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
        ])

        df["datetime"] = pd.to_datetime(df["datetime"], unit="ms")
        df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
       

        df = df[["datetime", "open", "high", "low", "close", "volume"]]

        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].round(3)

        df.set_index("datetime", inplace=True)


        # Dropping the last record as often it's incomplete
        df = df.iloc[:-1]

        print(f"\nFetched {len(df)} rows for {self.symbol.upper()} - {self.interval}")

        return df


if __name__ == "__main__":
    fetcher = BinanceFetcher(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, start_time="2020-01-01")
    df = fetcher.get_klines()

    print("DataFrame Shape:", df.shape)
    print("DataFrame Head:")
    print(df.head())