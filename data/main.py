import configparser
from data.fetch.binance.binance_fetch import BinanceFetcher
from data.fetch.bybit.bybit_fetch import BybitFetcher
from data.validate.data_validator import DataValidator
# from utils.db_handler import DatabaseManager
from data.utils.postgress_dataSave import DatabaseManager
# from downloader.data_downloader import DataDownloader
# from utils.data_saver import DataSaver


def load_config(config_path="config.ini"):
    config = configparser.ConfigParser()
    config.read(config_path)

    exchange = config["DEFAULT"]["exchange"]
    symbol = config["DEFAULT"]["symbols"]
    time_horizon = config["DEFAULT"]["time_horizons"]
    start_date = config["DEFAULT"]["start_date"]
    end_date = config["DEFAULT"]["end_date"]

    return exchange.lower(), symbol.upper(), time_horizon, start_date, end_date


def main():
    exchange, symbol, time_horizon, start_date, end_date = load_config()

    
    fetcher = None

    # Fetch Data
    if exchange == "binance":
        fetcher = BinanceFetcher(symbol, time_horizon, start_date, end_date)
    elif exchange == "bybit":
        fetcher = BybitFetcher(symbol, "1", start_time=start_date, end_time=end_date)
    else:
        print(f"Exchange '{exchange}' not supported.")
        return

    df = fetcher.get_klines()
    if df.empty:
        print("No data fetched.")
        return

    print(f"\nFetched {len(df)} rows for {symbol} - {time_horizon}")

    # Validate Data 
    validator = DataValidator(df, "1m")
    clean_df = validator.clean()

    # # Save to SQLite DB
    # db = DatabaseManager()
    # db.save_dataframe(clean_df, exchange, symbol, "1m")
    # db.close()

    db = DatabaseManager()
    db.save_dataframe(clean_df, exchange, symbol, "1m")
    db.close()

    # # Download + Resample 
    # downloader = DataDownloader()
    # df_1m = downloader.download(exchange, symbol, "1m")

    # if time_horizon != "1m":
    #     df_custom = downloader.resample(df_1m, time_horizon)
    # else:
    #     df_custom = df_1m

    # # Final Output as CSV
    # DataSaver.save_to_csv(df_custom, f"{exchange}_{symbol}_{time_horizon}.csv")
    # print(df_custom.head())


if __name__ == "__main__":
    main()
