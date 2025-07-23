import configparser
from data.downloader.data_downloader import DataDownloader
from indicator.indicator_calculator import IndicatorCalculator
from data.utils.data_saver import DataSaver


def load_config(config_path="data\\config.ini"):
    """Load configuration values from the config.ini file."""
    config = configparser.ConfigParser()
    config.read(config_path)

    exchange = config["DEFAULT"]["exchange"]
    symbol = config["DEFAULT"]["symbols"]
    time_horizon = config["DEFAULT"]["time_horizons"]

    return exchange, symbol, time_horizon



def main():
    #Load config
    exchange, symbol, time_horizon = load_config()

    #Download 1-minute data from DB
    downloader = DataDownloader()
    df_1m = downloader.download(exchange, symbol, "1m")

    #Resample if time horizon isn't "1m"
    if time_horizon != "1m":
        df_resampled = downloader.resample(df_1m, time_horizon)
    else:
        df_resampled = df_1m

    # Apply TA indicators
    indicator_calc = IndicatorCalculator(df_resampled)
    df_with_indicators = indicator_calc.apply_indicators()

    #Save to CSV
    file_path = f"{exchange}_{symbol}_{time_horizon}_indicators.csv"
    DataSaver.save_to_csv(df_with_indicators, file_path)

    print(f"Indicators added and saved to {file_path}")
    print(df_with_indicators.head())



if __name__ == "__main__":
    main()
