import configparser
from data.fetch.binance.binance_fetch import BinanceFetcher
from data.fetch.bybit.bybit_fetch import BybitFetcher
from data.validate.data_validator import DataValidator
from data.utils.postgress_dataSave import DatabaseManager
from datetime import datetime
import pandas as pd

file = open(r'E:\Neurog\New\cryptoPipeline\data\task.txt','a')
file.write(f'{datetime.now()} - The script ran \n')

def load_config(config_path="E:\\Neurog\\New\\cryptoPipeline\\data\\config.ini"):
    config = configparser.ConfigParser()
    config.read(config_path)

    exchange = config["DEFAULT"]["exchange"]
    symbols = config["DEFAULT"]["symbols"]
    time_horizon = config["DEFAULT"]["time_horizons"]
    start_date = config["DEFAULT"]["start_date"]
    end_date = config["DEFAULT"]["end_date"]

    # Parse comma-separated exchanges and symbols
    exchanges = [e.strip().lower() for e in exchange.split(",")]
    symbols = [s.strip().upper() for s in symbols.split(",")]
    

    return exchanges, symbols, time_horizon, start_date, end_date

def main():
    exchanges, symbols, time_horizon, start_date, end_date = load_config()

    # Initialize DatabaseManager once to reuse connection
    db = DatabaseManager()

    for exchange in exchanges:
        for symbol in symbols:
            print(f"\nProcessing {exchange} - {symbol}")

            # Check if table exists and is up-to-date
            is_up_to_date, latest_timestamp = db.check_table_up_to_date(exchange, symbol, "1m")

            if is_up_to_date:
                print(f"Data for {symbol} on {exchange} is up-to-date (latest: {latest_timestamp})")
                continue

            # If table exists but isn't up-to-date, adjust start_date to fetch new data
            if latest_timestamp:
                start_date = latest_timestamp.strftime("%Y-%m-%d %H:%M:%S")

            # Fetch Data
            fetcher = None
            if exchange == "binance":
                fetcher = BinanceFetcher(symbol, time_horizon, start_date, end_date)
            elif exchange == "bybit":
                fetcher = BybitFetcher(symbol, "1", start_time=start_date, end_time=end_date)
            else:
                print(f"Exchange '{exchange}' not supported.")
                continue

            df = fetcher.get_klines()
            if df.empty:
                print(f"No data fetched for {symbol} on {exchange}.")
                continue

            print(f"Fetched {len(df)} rows for {symbol} - {time_horizon} on {exchange}")

            # Validate Data
            validator = DataValidator(df, "1m")
            clean_df = validator.clean()

            # Save to PostgreSQL DB
            db.save_dataframe(clean_df, exchange, symbol, "1m")

    # Close database connection after all operations
    db.close()

if __name__ == "__main__":
    main()