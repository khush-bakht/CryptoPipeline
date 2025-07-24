import pandas as pd
import time
import datetime
from pybit.unified_trading import HTTP
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_SECRET_KEY")

client = HTTP(
    demo=True,
    api_key=API_KEY,
    api_secret=API_SECRET
)

class BybitFetcher:
    def __init__(self, symbol, interval, start_time, end_time="now"):
        print(f"[DEBUG] Initializing BybitFetcher with symbol={symbol}, interval={interval}, start_time={start_time}, end_time={end_time}")
        symbol = symbol.upper()
        if not symbol.endswith('USDT'):
            symbol += 'USDT'
        self.symbol = symbol
        self.interval = interval
        self.start_time = start_time
        self.end_time = end_time

    def get_klines(self):
        print(f"[DEBUG] Starting data fetch for {self.symbol} with interval {self.interval}")
        all_data = []
        limit = 1000
        start_ts = int(pd.to_datetime(self.start_time).timestamp() * 1000)
        end_ts = int(pd.Timestamp.now().timestamp() * 1000) if self.end_time == "now" else int(pd.to_datetime(self.end_time).timestamp() * 1000)
        print(f"[DEBUG] Start timestamp: {start_ts} ({pd.to_datetime(start_ts, unit='ms')}), End timestamp: {end_ts} ({pd.to_datetime(end_ts, unit='ms')})")

        # Map Binance interval format to Bybit interval format
        interval_map = {
            '1m': '1',
            '5m': '5',
            '15m': '15',
            '30m': '30',
            '1h': '60',
            '4h': '240',
            '1d': 'D'
        }
        bybit_interval = interval_map.get(self.interval, '1')
        print(f"[DEBUG] Mapped interval {self.interval} to Bybit interval {bybit_interval}")

        iteration = 0
        max_iterations = 10000  # Safeguard to prevent infinite loops
        previous_end_ts = None

        while True:
            iteration += 1
            if iteration > max_iterations:
                print(f"[DEBUG] Reached maximum iterations ({max_iterations}), breaking loop to prevent infinite loop")
                break

            print(f"[DEBUG] Iteration {iteration}: Fetching data from {pd.to_datetime(start_ts, unit='ms')} to {pd.to_datetime(end_ts, unit='ms')}")
            try:
                print(f"[DEBUG] Making API call with symbol={self.symbol}, interval={bybit_interval}, start={start_ts}, end={end_ts}, limit={limit}")
                klines = client.get_kline(
                    category="linear",
                    symbol=self.symbol,
                    interval=bybit_interval,
                    start=start_ts,
                    end=end_ts,
                    limit=limit
                )

                if not klines or 'result' not in klines or 'list' not in klines['result']:
                    print(f"[DEBUG] No data returned from API or invalid response: {klines}")
                    break

                raw_klines = klines['result']['list']
                print(f"[DEBUG] Received {len(raw_klines)} klines in this batch")
                if not raw_klines:
                    print("[DEBUG] Empty klines list, breaking loop")
                    break

                all_data.extend(raw_klines)
                print(f"[DEBUG] Total klines collected so far: {len(all_data)}")

                # Bybit returns klines in descending order (newest to oldest)
                # Use the oldest timestamp (last in the batch) to set the next end_ts
                new_end_ts = int(raw_klines[-1][0]) - 1  # Move to just before the oldest kline
                print(f"[DEBUG] Newest kline timestamp: {raw_klines[0][0]} ({pd.to_datetime(int(raw_klines[0][0]), unit='ms')})")
                print(f"[DEBUG] Oldest kline timestamp: {raw_klines[-1][0]} ({pd.to_datetime(int(raw_klines[-1][0]), unit='ms')})")
                print(f"[DEBUG] Proposed new end_ts: {new_end_ts} ({pd.to_datetime(new_end_ts, unit='ms')})")

                # Check if end_ts is stuck
                if previous_end_ts == new_end_ts:
                    print(f"[DEBUG] end_ts has not changed (stuck at {new_end_ts}), breaking loop")
                    break
                previous_end_ts = end_ts

                # Update end_ts for the next batch
                end_ts = new_end_ts

                # Break if we've reached or passed the start_time
                if end_ts <= start_ts:
                    print("[DEBUG] Reached or passed start_time, breaking loop")
                    break

                time.sleep(0.2)
                print(f"[DEBUG] Paused for 0.2 seconds to avoid rate limiting")

            except Exception as e:
                print(f"[DEBUG] Error fetching batch: {e}")
                break

        print(f"[DEBUG] Finished fetching, total klines collected: {len(all_data)}")
        if not all_data:
            print("[DEBUG] No data collected, returning empty DataFrame")
            return pd.DataFrame()

        print("[DEBUG] Converting klines to DataFrame")
        df = pd.DataFrame(all_data, columns=[
            "datetime", "open", "high", "low", "close", "volume", "turnover"
        ])

        print("[DEBUG] Converting datetime column from milliseconds")
        df["datetime"] = pd.to_datetime(pd.to_numeric(df["datetime"]), unit="ms")
        print("[DEBUG] Selecting OHLCV columns")
        df = df[["datetime", "open", "high", "low", "close", "volume"]]

        print("[DEBUG] Converting numeric columns to float and rounding to 3 decimal places")
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].round(3)

        print("[DEBUG] Sorting by datetime ascending to ensure correct order")
        df = df.sort_values("datetime")

        print("[DEBUG] Setting datetime as index")
        df.set_index("datetime", inplace=True)

        print("[DEBUG] Dropping last record as it may be incomplete")
        df = df.iloc[:-1]

        print(f"[DEBUG] Final DataFrame has {len(df)} rows for {self.symbol.upper()} - {self.interval}")
        return df


if __name__ == "__main__":
    print("[DEBUG] Running main block")
    fetcher = BybitFetcher(symbol="BTCUSDT", interval="1m", start_time="2020-01-01")
    df = fetcher.get_klines()
    print("[DEBUG] DataFrame Shape:", df.shape)
    print("[DEBUG] DataFrame Head:")
    print(df.head())