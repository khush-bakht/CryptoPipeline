#data/fetch/bybit/bybit_fetch.py
import pandas as pd
import time
from pybit.unified_trading import HTTP
import os
from dotenv import load_dotenv

load_dotenv()

# BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
# BYBIT_SECRET_KEY = os.getenv("BYBIT_SECRET_KEY")


# session = HTTP(testnet=False, api_key=BYBIT_API_KEY, api_secret=BYBIT_SECRET_KEY)
session = HTTP(testnet=False)


class BybitFetcher:
    def __init__(self, symbol, interval, start_time, end_time="now", category="spot"):
        self.symbol = symbol.upper()
        self.interval = interval
        self.start_time = int(pd.to_datetime(start_time).timestamp() * 1000)
        self.end_time = int(pd.Timestamp.now().timestamp() * 1000) if end_time == "now" else int(pd.to_datetime(end_time).timestamp() * 1000)
        self.category = category
        self.limit = 1000


    def get_klines(self):
        print(f"Fetching {self.symbol} {self.interval} from Bybit (pybit)...")
        all_data = []
        start = self.start_time

        while start < self.end_time:
            response = session.get_kline(
                category=self.category,
                symbol=self.symbol,
                interval=self.interval,
                start=start,
                end=self.end_time,
                limit=self.limit
            )

            klines = response.get("result", {}).get("list", [])

            if not klines:
                print("No more data or error in response.")
                break

            all_data.extend(klines)

            last_ts = int(klines[-1][0])
            start = last_ts + 1  # moving forward by 1 ms
            time.sleep(0.3)

        if not all_data:
            return pd.DataFrame()

        df = pd.DataFrame(all_data, columns=[
            "datetime", "open", "high", "low", "close", "volume", "turnover"
        ])

        df["datetime"] = pd.to_datetime(df["datetime"].astype(int), unit="ms")
        df = df.astype({
            "open": float,
            "high": float,
            "low": float,
            "close": float,
            "volume": float,
            "turnover": float
        })

        df = df[["datetime", "open", "high", "low", "close", "volume"]]
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].round(3)
        df.set_index("datetime", inplace=True)

        df = df.iloc[:-1]  # dropping the last record

        print(f"\nFetched {len(df)} rows for {self.symbol} - {self.interval}")
        return df


if __name__ == "__main__":
    fetcher = BybitFetcher(symbol="BTCUSDT", interval="1", start_time="2020-01-01")
    df = fetcher.get_klines()

    print("DataFrame Shape:", df.shape)
    print(df.head())
