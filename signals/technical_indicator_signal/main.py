import configparser
from data.downloader.data_downloader import DataDownloader
from indicator.indicator_calculator import IndicatorCalculator
from data.utils.data_saver import DataSaver
from signals.technical_indicator_signal.signal_generator import SignalGenerator


def load_config(path="E:\\Neurog\\New\\cryptoPipeline\\signals\\technical_indicator_signal\\signals_config.ini"):
    config = configparser.ConfigParser()
    config.read(path)
    return config

def main():
    # Load configuration
    cfg = load_config()
    
    # Extract DATA section
    data_config = cfg["DATA"]
    exchange = data_config["exchange"]
    symbol = data_config["symbol"]
    time_horizon = data_config["time_horizon"]


    # Load from SQLite
    downloader = DataDownloader()
    df_1m = downloader.download(exchange, symbol, base_interval="1m")

    # Resample to desired interval
    df = downloader.resample(df_1m, custom_interval=time_horizon)

    # Dictionary for enabled indicators from all sections
    enabled_indicators = {}
    for section in cfg.sections():
        if section != "DATA":  # Skip DATA section
            indicators = cfg[section]
            for indicator, value in indicators.items():
                if value.lower() == "true":
                    enabled_indicators[indicator] = True

    # Applying only enabled indicators
    calculator = IndicatorCalculator(df)
    df_indicators = calculator.apply_indicators(indicators=enabled_indicators)

    # Generate signals
    signal_gen = SignalGenerator(df_indicators)
    df_signals = signal_gen.generate_signals()
    print(df_signals.head())

    # Final Signal File
    output_path = f"{exchange}_{symbol}_{time_horizon}_signals.csv"
    DataSaver.save_to_csv(df_signals, output_path)
    

if __name__ == "__main__":
    main()


#Run from main directory     