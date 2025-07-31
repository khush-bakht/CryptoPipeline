import configparser
import pandas as pd
from strategies.strategy_pipeline.generator import StrategyGenerator
from data.downloader.data_downloader import DataDownloader
from indicator.indicator_calculator import IndicatorCalculator
from signals.technical_indicator_signal.signal_generator import SignalGenerator
from strategies.strategy_pipeline.signal_processor import SignalProcessor
from strategies.strategy_pipeline.utils.postgress_handler import DatabaseManager
from strategies.strategy_pipeline.utils.indicator_utils import INDICATORS
from data.utils.data_saver import DataSaver

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
            df = downloader.resample(df_1m, strategy['time_horizon'])
        else:
            df = df_1m
        
        if df is not None and not df.empty:
            # Ensure 'datetime' is a column, not just index
            if 'datetime' not in df.columns:
                df = df.reset_index()
                if 'index' in df.columns and 'datetime' not in df.columns:
                    df = df.rename(columns={'index': 'datetime'})
            
            enabled_indicators = {ind: val for ind, val in strategy.items() if ind in INDICATORS and val}

        # Applying only enabled indicators
            calculator = IndicatorCalculator(df)
            df_with_indicators = calculator.apply_indicators(indicators=enabled_indicators)

            # Drop rows with any missing or empty values after indicators are applied
            df_with_indicators = df_with_indicators.dropna(how='any')
            df_with_indicators = df_with_indicators[~df_with_indicators.isin([None, '', 'NaN', 'nan']).any(axis=1)]
           
            DataSaver.save_to_csv(df_with_indicators, "indicators.csv")

            indicator_map = {
                
            'sma': 'sma_20', 'ema': 'ema_20', 'wma': 'wma_20', 'dema': 'dema_20', 'tema': 'tema_20',
            'trima': 'trima_20', 'kama': 'kama_20', 'mama': 'mama_20', 't3': 't3_20',
            'midpoint': 'midpoint_20', 'midprice': 'midprice_20',
            'bb_upper': 'bb_upper', 'bb_middle': 'bb_middle', 'bb_lower': 'bb_lower',
            'parabolic_sar': 'parabolic_sar',

            # Momentum Indicators
            'rsi': 'rsi', 'macd': 'macd', 'macd_signal': 'macd_signal', 'macd_hist': 'macd_hist',
            'adx': 'adx', 'cci': 'cci', 'willr': 'williams_r', 'roc': 'roc', 'trix': 'trix',
            'stoch_k': 'stoch_k', 'stoch_d': 'stoch_d', 'ultosc': 'ultosc', 'cmo': 'cmo',
            'apo': 'apo', 'ppo': 'ppo', 'mom': 'mom',

            # Volume Indicators
            'obv': 'obv', 'mfi': 'mfi', 'ad': 'ad', 'adosc': 'adosc',

            # Volatility Indicators
            'atr': 'atr', 'natr': 'natr', 'trange': 'trange', 'chaikin_volatility': 'chaikin_volatility',

            # Price Transform
            'avgprice': 'avgprice', 'medprice': 'medprice', 'typprice': 'typprice', 'wclprice': 'wclprice',

            # Cycle Indicators
            'ht_dcperiod': 'ht_dcperiod', 'ht_dcphase': 'ht_dcphase', 'ht_phasor': 'ht_phasor',
            'ht_sine': 'ht_sine', 'ht_trendmode': 'ht_trendmode',

            # Pattern Recognition (example)
            'cdl_doji': 'cdl_doji', 'cdl_hammer': 'cdl_hammer', 'cdl_engulfing': 'cdl_engulfing',
            # ... add more as you implement rules
            }
            indicators_in_df = [indicator_map[k] for k in enabled_indicators if indicator_map.get(k) in df_with_indicators.columns]
            sg = SignalGenerator(df_with_indicators, indicator_names=indicators_in_df)

            signal_df = sg.generate_signals()
            # Add datetime and OHLCV columns for reference
            ohlcv_cols = ['datetime', 'open', 'high', 'low', 'close', 'volume']
            # Remove OHLCV columns from signal_df before concatenation
            signal_df_no_ohlcv = signal_df.drop(columns=ohlcv_cols)
            output_df = df_with_indicators[ohlcv_cols].copy()
            output_df = output_df.reset_index(drop=True)
            signal_df_no_ohlcv = signal_df_no_ohlcv.reset_index(drop=True)
            output_df = output_df.join(signal_df_no_ohlcv)
            # Round volume to 2 decimal places
            output_df['volume'] = output_df['volume'].round(2)
            # Save only datetime, ohlcv, and signal columns
            # output_filename = f"{strategy['exchange']}_{strategy['symbol']}_{strategy['time_horizon']}_signals.csv"
            output_df.to_csv("signals.csv", index=False)
            # print(f"Signal data saved to {output_filename}")
        else:
            print(f"No data available for {strategy['exchange']}")

        # # Final Signal File
        # output_path = f"{strategy['exchange']}_{strategy['symbol']}_{strategy['time_horizon']}_signals.csv"
        # DataSaver.save_to_csv(df_signals, output_path)
    

        # print(df_signals.head())
        
        # Process signals and save
        signal_proc = SignalProcessor()
        df_final = signal_proc.process_signals(output_df, strategy['name'])
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