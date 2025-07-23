#data/downloader
import pandas as pd
import configparser
import datetime
from data.utils.data_saver import DataSaver
from data.utils.postgress_connection import PostgresConnection
from data.fetch.binance.binance_fetch import BinanceFetcher
from data.fetch.bybit.bybit_fetch import BybitFetcher
from data.utils.postgress_dataSave import DatabaseManager
from data.validate.data_validator import DataValidator
from data.utils.interval_mapper import map_to_pandas_freq

def load_config(config_path="E:\\Neurog\\New\\cryptoPipeline\\data\\config.ini"):
    config = configparser.ConfigParser()
    config.read(config_path)

    exchange = config["DEFAULT"]["exchange"]
    symbol = config["DEFAULT"]["symbols"]
    time_horizon = config["DEFAULT"]["time_horizons"]
    start_date = config["DEFAULT"]["start_date"]
    end_date = config["DEFAULT"]["end_date"]

    return exchange.lower(), symbol.upper(), time_horizon, start_date, end_date

class DataDownloader:
    def __init__(self):
        # Initialize PostgresConnection
        self.pg_conn = PostgresConnection()
        self.engine = self.pg_conn.get_engine()

    def _format_table_name(self, exchange, symbol, interval):
        return f"{exchange.lower()}_data.{symbol.lower()}_{interval}"

    def download(self, exchange, symbol, base_interval="1m", start_date="2020-01-01", end_date=None):
        if end_date is None:
            end_date = datetime.datetime.now().strftime("%Y-%m-%d")
        table_name = self._format_table_name(exchange, symbol, base_interval)
        print(f"Downloading data from table: {table_name}")

        try:
            df = pd.read_sql(f"SELECT * FROM {table_name}", self.engine, parse_dates=["datetime"])
            df.set_index("datetime", inplace=True)
        except Exception as e:
            print(f"Error reading table '{table_name}': {e}")
            df = pd.DataFrame()
        finally:
            self.engine.dispose()
        if not df.empty:
            return df

        if df.empty and start_date and end_date:
            print(f"No data found in {table_name}. Attempting to fetch...")
            # Fetch data based on exchange
            if exchange == "binance":
                fetcher = BinanceFetcher(symbol, base_interval, start_date, end_date)
                df = fetcher.get_klines()
            elif exchange == "bybit":
                fetcher = BybitFetcher(symbol, base_interval, start_time=start_date, end_time=end_date)
                df = fetcher.get_klines()
            else:
                print(f"Exchange '{exchange}' not supported for fetching.")
                return pd.DataFrame()

            if not df.empty:
                validator = DataValidator(df, "1m")
                clean_df = validator.clean()
                # Save fetched data to PostgreSQL
                db = DatabaseManager()
                db.save_dataframe(clean_df, exchange, symbol, base_interval)
                db.close()
                return clean_df
                
            else:
                print("Fetching failed. No data available.")
                return df
    
        

    def resample(self, df, custom_interval):
        print(f"Resampling data to: {custom_interval}")
        pandas_freq = map_to_pandas_freq(custom_interval)
        df_resampled = df.resample(pandas_freq).agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        })

      
        df_resampled = df_resampled.round(3)
        df_resampled.reset_index(inplace=True)
        df_resampled.dropna(inplace=True)

        return df_resampled


if __name__ == "__main__":
    exchange, symbol, time_horizon, start_date, end_date = load_config()
    downloader = DataDownloader()
    df_1m = downloader.download(exchange, symbol, "1m", start_date, end_date)

    if time_horizon != "1m":
        df_custom = downloader.resample(df_1m, time_horizon)
    else:
        df_custom = df_1m

    # Final Output as CSV
    DataSaver.save_to_csv(df_custom, f"{exchange}_{symbol}_{time_horizon}.csv")
    print(df_custom.head())

    print("DataFrame Shape:", df_custom.shape)
    print("DataFrame Head:")
    print(df_custom.head())