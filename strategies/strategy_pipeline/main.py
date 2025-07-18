import configparser
import pandas as pd
from strategies.strategy_pipeline.generator import StrategyGenerator
from data.downloader.data_downloader import DataDownloader
from indicator.indicator_calculator import IndicatorCalculator
from signals.technical_indicator_signal.signal_generator import SignalGenerator
from strategies.strategy_pipeline.signal_processor import SignalProcessor
from strategies.strategy_pipeline.utils.postgress_handler import DatabaseManager
from strategies.strategy_pipeline.utils.indicator_utils import INDICATORS

def load_config(config_path="strategies/strategy_pipeline/strategy_config.ini"):
    config = configparser.ConfigParser()
    config.read(config_path)
    return {
        'exchange': config['DATA']['exchange'],
        'symbol_list': config['DATA']['symbol_list'].split(', '),
        'time_horizons': config['DATA']['time_horizons'].split(', '),
        'max_strategy_files': int(config['limits']['max_strategy_files']),
        'base_filename': config['general']['base_filename'],
        'prefix': config['general']['prefix'],
        'start_date': config['dates']['start_date'],
        'end_date': config['dates']['end_date']
    }

if __name__ == "__main__":
    config = load_config()
    generator = StrategyGenerator(config)
    downloader = DataDownloader()
    db = DatabaseManager()  

    # Generate and process strategies
    #Get Max Index
    max_index = db.fetch_strategies()  

    for i in range(config['max_strategy_files']):
        new_index = max_index + i + 1
        strategy = generator.generate_strategy(new_index)

        # Download and resample data

        downloader = DataDownloader()
        df_1m = downloader.download(strategy['exchange'], strategy['symbol'], "1m", config['start_date'], config['end_date'])
        print(df_1m.shape)
        if strategy['time_horizon'] != "1m":
            df_custom = downloader.resample(df_1m, strategy['time_horizon'])
        else:
            df_custom = df_1m

        # Calculate indicators
        true_indicators = {ind: val for ind, val in strategy.items() if ind in INDICATORS and val}
        calc = IndicatorCalculator(df_custom)
        df_indicators = calc.apply_indicators(true_indicators)

        # Generate signals
        signal_gen = SignalGenerator(df_indicators)
        df_signals = signal_gen.generate_signals()
        print(df_signals.head())
        


        # Process signals and save
        signal_proc = SignalProcessor()
        df_final = signal_proc.process_signals(df_signals, strategy['name'])
        if df_final is not None and not df_final.empty:
            db.save_signals(df_final, strategy['name'])
            print(f"Saved final signals for {strategy['name']}")

        # Append strategy to strategies_config table
        strategy_config = {
            'name': strategy['name'],
            'exchange': strategy['exchange'],
            'symbol': strategy['symbol'],
            'time_horizon': strategy['time_horizon']
        }
        strategy_config.update({ind: strategy.get(ind, False) for ind in INDICATORS})
        db.save_strategies([strategy_config])
        print(f"Appended strategy {strategy['name']} to strategies_config table")    

    db.close()