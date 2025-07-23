import pandas as pd
from pybit.unified_trading import HTTP
from datetime import datetime
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_SECRET_KEY = os.getenv("BYBIT_SECRET_KEY")

class BybitFetcher:
    def __init__(self, symbol, timeframe, start_time, end_time):
        """
        Initialize BybitFetcher for fetching futures kline data from Bybit using API keys.
        
        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT' for futures).
            timeframe (str): Kline interval (e.g., '1' for 1 minute).
            start_time (str): Start date in 'YYYY-MM-DD' format.
            end_time (str): End date in 'YYYY-MM-DD' format or 'now'.
        """
        symbol = symbol.upper()
        if not symbol.endswith('USDT'):
            symbol += 'USDT'
        self.symbol = symbol
        self.timeframe = timeframe
        self.start_time = start_time
        self.end_time = end_time
        self.client = HTTP(
            api_key=BYBIT_API_KEY,
            api_secret=BYBIT_SECRET_KEY
        )  # Initialize pybit HTTP client with API keys
        print(f"[DEBUG] Initialized BybitFetcher for {self.symbol}, timeframe: {self.timeframe}, "
              f"start: {self.start_time}, end: {self.end_time}")
        
    def _parse_datetime(self, date_str):
        """
        Convert date string to timestamp in milliseconds.
        
        Args:
            date_str (str): Date string in 'YYYY-MM-DD' format or 'now'.
        
        Returns:
            int: Timestamp in milliseconds.
        """
        if date_str.lower() == "now":
            ts = int(time.time() * 1000)
            print(f"[DEBUG] Parsed 'now' to timestamp: {ts}")
            return ts
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            ts = int(dt.timestamp() * 1000)
            print(f"[DEBUG] Parsed date '{date_str}' to timestamp: {ts}")
            return ts
        except ValueError as e:
            print(f"[DEBUG] Error parsing date '{date_str}': {e}")
            raise ValueError(f"Invalid date format: {date_str}. Use 'YYYY-MM-DD' or 'now'.") from e

    def get_klines(self):
        """
        Fetch futures kline data from Bybit for the specified symbol and timeframe.
        
        Returns:
            pandas.DataFrame: DataFrame containing kline data with columns:
                              ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        """
        try:
            # Convert start and end times to milliseconds
            start_ts = self._parse_datetime(self.start_time)
            end_ts = self._parse_datetime(self.end_time)
            print(f"[DEBUG] Fetching klines for {self.symbol}, timeframe: {self.timeframe}, "
                  f"start_ts: {start_ts}, end_ts: {end_ts}")

            # Bybit API parameters for futures (linear perpetual)
            params = {
                "category": "linear",  # Futures (linear perpetual contracts)
                "symbol": self.symbol,
                "interval": self.timeframe,
                "start": start_ts,
                "end": end_ts,
                "limit": 1000  # Max limit per request
            }

            # Fetch kline data
            data = []
            iteration = 0
            while start_ts < end_ts:
                iteration += 1
                print(f"[DEBUG] API call {iteration}: Fetching klines from {start_ts}")
                response = self.client.get_kline(**params)
                if response.get("retCode") != 0:
                    print(f"[DEBUG] Bybit API error: {response.get('retMsg')}")
                    raise Exception(f"Bybit API error: {response.get('retMsg')}")

                klines = response["result"]["list"]
                if not klines:
                    print(f"[DEBUG] No more klines returned for {self.symbol}")
                    break

                print(f"[DEBUG] Retrieved {len(klines)} klines in iteration {iteration}")
                data.extend(klines)
                
                # Update start_ts to the timestamp of the last kline + 1ms
                start_ts = int(klines[0][0]) + 1
                params["start"] = start_ts

                # Avoid hitting rate limits
                time.sleep(0.1)

            if not data:
                print(f"[DEBUG] No data fetched for {self.symbol}")
                return pd.DataFrame()

            print(f"[DEBUG] Total klines fetched: {len(data)}")
            
            # Convert to DataFrame
            df = pd.DataFrame(
                data,
                columns=["timestamp", "open", "high", "low", "close", "volume", "turnover"]
            )
            print(f"[DEBUG] Created DataFrame with columns: {df.columns.tolist()}")
            
            # Convert timestamp to datetime and adjust data types
            df["timestamp"] = pd.to_datetime(df["timestamp"].astype(float), unit="ms")
            df[["open", "high", "low", "close", "volume"]] = df[
                ["open", "high", "low", "close", "volume"]
            ].astype(float)
            print(f"[DEBUG] Converted timestamp to datetime and cast columns to float")
            
            # Drop turnover column as it's not needed
            df = df.drop(columns=["turnover"])
            print(f"[DEBUG] Dropped 'turnover' column")
            
            # Sort by timestamp ascending
            df = df.sort_values(by="timestamp").reset_index(drop=True)
            print(f"[DEBUG] Sorted DataFrame by timestamp, final row count: {len(df)}")
            
            return df

        except Exception as e:
            print(f"[DEBUG] Error fetching Bybit futures data: {e}")
            return pd.DataFrame()

    def __del__(self):
        """
        Close the Bybit client session when the object is destroyed.
        """
        try:
            self.client.session.close()
            print("[DEBUG] Closed Bybit client session")
        except Exception as e:
            print(f"[DEBUG] Error closing Bybit client session: {e}")