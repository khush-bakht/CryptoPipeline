#optimization/optimizer.py
import configparser
import logging
import json
import datetime
import optuna
import pandas as pd
import os
from data.downloader.data_downloader import DataDownloader
from indicator.indicator_calculator import IndicatorCalculator
from signals.technical_indicator_signal.signal_generator import SignalGenerator
from strategies.strategy_pipeline.signal_processor import SignalProcessor
from strategies.strategy_pipeline.generator import StrategyGenerator
from backtest.backtest import Backtester
from strategies.strategy_pipeline.utils.postgress_handler import DatabaseManager
from strategies.strategy_pipeline.utils.indicator_utils import INDICATORS


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Optimizer:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.exchange = self.config['DATA']['exchange']
        self.symbol_list = self.config['DATA']['symbol_list'].split(',')
        self.time_horizons = self.config['DATA']['time_horizons'].split(',')
        self.start_date = self.config['dates']['start_date']
        self.end_date = self.config['dates']['end_date'] if self.config['dates']['end_date'] != 'now' else datetime.datetime.now().strftime('%Y-%m-%d')
        self.n_trials = int(self.config['optimization']['n_trials'])
        self.num_strategies = int(self.config['optimization']['num_strategies'])
        self.pnl_threshold = float(self.config['optimization']['pnl_threshold'])
        self.strategy_generator = StrategyGenerator({
            'base_filename': self.config['general']['base_filename'],
            'prefix': self.config['general']['prefix'],
            'exchange': self.exchange,
            'symbol_list': self.symbol_list,
            'time_horizons': self.time_horizons
        })
        self.downloader = DataDownloader()
        os.makedirs('optimization_results', exist_ok=True)

    def objective(self, trial, strategy):
        # Define hyperparameter search space for enabled indicators with windows
        params = {}
        if isinstance(strategy.get('sma'), int):
            params['sma'] = {'window': trial.suggest_int('sma_window', 5, 50)}
        if isinstance(strategy.get('ema'), int):
            params['ema'] = {'window': trial.suggest_int('ema_window', 5, 50)}
        if isinstance(strategy.get('wma'), int):
            params['wma'] = {'window': trial.suggest_int('wma_window', 5, 50)}
        if isinstance(strategy.get('dema'), int):
            params['dema'] = {'window': trial.suggest_int('dema_window', 5, 50)}
        if isinstance(strategy.get('tema'), int):
            params['tema'] = {'window': trial.suggest_int('tema_window', 5, 50)}
        if isinstance(strategy.get('trima'), int):
            params['trima'] = {'window': trial.suggest_int('trima_window', 5, 50)}
        if isinstance(strategy.get('kama'), int):
            params['kama'] = {'window': trial.suggest_int('kama_window', 5, 50)}
        if isinstance(strategy.get('t3'), int):
            params['t3'] = {'window': trial.suggest_int('t3_window', 5, 20)}
        if isinstance(strategy.get('midpoint'), int):
            params['midpoint'] = {'window': trial.suggest_int('midpoint_window', 5, 20)}
        if isinstance(strategy.get('bbands'), int):
            params['bbands'] = {'window': trial.suggest_int('bbands_window', 5, 50)}
        if isinstance(strategy.get('adx'), int):
            params['adx'] = {'window': trial.suggest_int('adx_window', 5, 30)}
        if isinstance(strategy.get('adxr'), int):
            params['adxr'] = {'window': trial.suggest_int('adxr_window', 5, 30)}
        if isinstance(strategy.get('aroon'), int):
            params['aroon'] = {'window': trial.suggest_int('aroon_window', 5, 25)}
        if isinstance(strategy.get('aroonosc'), int):
            params['aroonosc'] = {'window': trial.suggest_int('aroonosc_window', 5, 25)}
        if isinstance(strategy.get('cci'), int):
            params['cci'] = {'window': trial.suggest_int('cci_window', 5, 30)}
        if isinstance(strategy.get('cmo'), int):
            params['cmo'] = {'window': trial.suggest_int('cmo_window', 5, 30)}
        if isinstance(strategy.get('dx'), int):
            params['dx'] = {'window': trial.suggest_int('dx_window', 5, 30)}
        if isinstance(strategy.get('mfi'), int):
            params['mfi'] = {'window': trial.suggest_int('mfi_window', 5, 30)}
        if isinstance(strategy.get('minus_di'), int):
            params['minus_di'] = {'window': trial.suggest_int('minus_di_window', 5, 30)}
        if isinstance(strategy.get('minus_dm'), int):
            params['minus_dm'] = {'window': trial.suggest_int('minus_dm_window', 5, 30)}
        if isinstance(strategy.get('plus_di'), int):
            params['plus_di'] = {'window': trial.suggest_int('plus_di_window', 5, 30)}
        if isinstance(strategy.get('plus_dm'), int):
            params['plus_dm'] = {'window': trial.suggest_int('plus_dm_window', 5, 30)}
        if isinstance(strategy.get('rsi'), int):
            params['rsi'] = {'window': trial.suggest_int('rsi_window', 5, 30)}
        if isinstance(strategy.get('trix'), int):
            params['trix'] = {'window': trial.suggest_int('trix_window', 5, 30)}
        if isinstance(strategy.get('willr'), int):
            params['willr'] = {'window': trial.suggest_int('willr_window', 5, 30)}
        if isinstance(strategy.get('atr'), int):
            params['atr'] = {'window': trial.suggest_int('atr_window', 5, 30)}
        if isinstance(strategy.get('natr'), int):
            params['natr'] = {'window': trial.suggest_int('natr_window', 5, 30)}
        if isinstance(strategy.get('trange'), int):
            params['trange'] = {'window': trial.suggest_int('trange_window', 5, 30)}
        tp = trial.suggest_float('tp', 0.01, 0.10)
        sl = trial.suggest_float('sl', 0.01, 0.05)

        # Log trial parameters
        param_log = {k: v['window'] for k, v in params.items() if 'window' in v}
        param_log.update({'tp': tp, 'sl': sl})
        logging.info(f"Trial {trial.number} for {strategy['name']}: {strategy['symbol']}, {strategy['time_horizon']}, params {param_log}")

        # Download data
        symbol = strategy['symbol']
        time_horizon = strategy['time_horizon']
        df_1m = self.downloader.download(self.exchange, symbol, "1m", self.start_date, self.end_date)
        if df_1m is None or df_1m.empty:
            logging.warning(f"No data for {symbol} at 1m")
            return 0.0

        # Resample data
        df = df_1m if time_horizon == "1m" else self.downloader.resample(df_1m, time_horizon)
        if df is None or df.empty:
            logging.warning(f"No resampled data for {symbol} at {time_horizon}")
            return 0.0

        # Ensure datetime column
        if 'datetime' not in df.columns:
            df = df.reset_index()
            if 'index' in df.columns and 'datetime' not in df.columns:
                df = df.rename(columns={'index': 'datetime'})

        # Prepare enabled indicators with fixed windows from strategy
        enabled_indicators = {
            k: v for k, v in strategy.items()
            if k not in ['name', 'exchange', 'symbol', 'time_horizon'] and (isinstance(v, bool) and v or isinstance(v, int))
        }
        calculator = IndicatorCalculator(df)
        df_with_indicators = calculator.apply_indicators(indicators=enabled_indicators, params=params)
        
        df_with_indicators.to_csv("indicators.csv", index=False)
        print("_______Indicators_______")


        if df_with_indicators is None or df_with_indicators.empty:
            logging.warning(f"No indicators calculated for {symbol}")
            return 0.0

        # Map indicators to signal names
        indicator_map = {
            'sma': f'sma_{params.get("sma", {"window": strategy.get("sma", 20)})["window"]}',
            'ema': f'ema_{params.get("ema", {"window": strategy.get("ema", 20)})["window"]}',
            'wma': f'wma_{params.get("wma", {"window": strategy.get("wma", 20)})["window"]}',
            'dema': f'dema_{params.get("dema", {"window": strategy.get("dema", 20)})["window"]}',
            'tema': f'tema_{params.get("tema", {"window": strategy.get("tema", 20)})["window"]}',
            'trima': f'trima_{params.get("trima", {"window": strategy.get("trima", 30)})["window"]}',
            'kama': f'kama_{params.get("kama", {"window": strategy.get("kama", 30)})["window"]}',
            't3': f't3_{params.get("t3", {"window": strategy.get("t3", 5)})["window"]}',
            'midpoint': f'midpoint_{params.get("midpoint", {"window": strategy.get("midpoint", 14)})["window"]}',
            'bbands': ['bb_upper', 'bb_middle', 'bb_lower'],
            'adx': 'adx',
            'adxr': 'adxr',
            'aroon': ['aroon_up', 'aroon_down'],
            'aroonosc': 'aroonosc',
            'cci': 'cci',
            'cmo': 'cmo',
            'dx': 'dx',
            'mfi': 'mfi',
            'minus_di': 'minus_di',
            'minus_dm': 'minus_dm',
            'plus_di': 'plus_di',
            'plus_dm': 'plus_dm',
            'rsi': 'rsi',
            'trix': 'trix',
            'willr': 'williams_r',
            'atr': 'atr',
            'natr': 'natr',
            'trange': 'true_range',
            'mama': ['mama', 'fama'],
            'mavp': 'mavp',
            'midprice': 'midprice',
            'sar': 'sar',
            'sarext': 'sarext',
            'macd': ['macd', 'macd_signal', 'macd_hist'],
            'macdext': ['macdext', 'macdext_signal', 'macdext_hist'],
            'macdfix': ['macdfix', 'macdfix_signal', 'macdfix_hist'],
            'bop': 'bop',
            'stoch': ['stoch_k', 'stoch_d'],
            'stochf': ['stochf_k', 'stochf_d'],
            'stochrsi': ['stochrsi_k', 'stochrsi_d'],
            'ad': 'ad',
            'adosc': 'adosc',
            'obv': 'obv',
            'avgprice': 'avgprice',
            'medprice': 'medprice',
            'typprice': 'typprice',
            'wclprice': 'wclprice',
            'ht_dcperiod': 'ht_dcperiod',
            'ht_dcphase': 'ht_dcphase',
            'ht_phasor': ['ht_phasor_inphase', 'ht_phasor_quadrature'],
            'ht_sine': ['ht_sine', 'ht_leadsine'],
            'ht_trendmode': 'ht_trendmode'
        }
        for ind in enabled_indicators:
            if ind.startswith('cdl'):
                indicator_map[ind] = ind

        indicators_in_df = []
        for k in enabled_indicators:
            mapped = indicator_map.get(k)
            if isinstance(mapped, list):
                indicators_in_df.extend([col for col in mapped if col in df_with_indicators.columns])
            elif mapped in df_with_indicators.columns:
                indicators_in_df.append(mapped)

        # Generate signals

        sg = SignalGenerator(df_with_indicators, indicator_names=indicators_in_df)
        signal_df = sg.generate_signals()
        if signal_df is None or signal_df.empty:
            logging.warning(f"No signals generated for {symbol}")
            return 0.0, None, None
        signal_df.to_csv("signals.csv", index=False)
        print("_______Signals_______")

        # Process signals with voting
        processor = SignalProcessor()
        final_signal_df = processor.process_signals(signal_df, strategy['name'])
        if final_signal_df is None or final_signal_df.empty:
            logging.warning(f"No final signals for {strategy['name']}")
            return 0.0, None, None

        # Run backtest
        backtester = Backtester(df_with_indicators, final_signal_df, tp=tp, sl=sl)
        results = backtester.run()
        if results.empty:
            logging.warning(f"No backtest results for {symbol}")
            return 0.0, None, None

        pnl_sum = results['pnl_sum'].iloc[-1] if 'pnl_sum' in results.columns else 0.0
        logging.info(f"Trial {trial.number} pnl_sum: {pnl_sum}")

        # Return pnl_sum and data for best trial
        return pnl_sum, final_signal_df, results

    def run(self):
        db = DatabaseManager()
        max_index = db.fetch_strategies()
        for i in range(self.num_strategies):
            new_index = max_index + i + 1
            strategy = self.strategy_generator.generate_strategy(new_index)
            logging.info(f"Optimizing strategy {strategy['name']}: {strategy['symbol']}, {strategy['time_horizon']}, indicators {strategy}")
            study = optuna.create_study(direction='maximize')
            best_pnl = float('-inf')
            best_signal_df = None
            best_results = None
            best_params = None
            best_trial_number = None

            def objective_wrapper(trial):
                nonlocal best_pnl, best_signal_df, best_results, best_params, best_trial_number
                pnl, signals, results = self.objective(trial, strategy)
                if pnl > best_pnl:
                    best_pnl = pnl
                    best_signal_df = signals
                    best_results = results
                    best_params = trial.params
                    best_trial_number = trial.number
                return pnl

            study.optimize(objective_wrapper, n_trials=self.n_trials)
            logging.info(f"Best trial for {strategy['name']}: trial {best_trial_number}, pnl_sum {best_pnl}, params {best_params}")

            # Save best trial data
            if best_signal_df is not None and best_results is not None:
                if best_signal_df is not None and not best_signal_df.empty:
                    db.save_signals(best_signal_df, strategy['name'])
                    print(f"Saved final signals for {strategy['name']}")

                # Display final balance and summary
                if not best_results.empty:
                    best_results[['buy_price', 'sell_price', 'pnl_percent', 'pnl_sum', 'balance']] = best_results[[
                        'buy_price', 'sell_price', 'pnl_percent', 'pnl_sum', 'balance'
                    ]].round(2)
                    print(f"\n Final Balance: {best_results.iloc[-1]['balance']:.2f}")
                    print(f"Total Trades: {len(best_results[best_results['action'].isin(['tp', 'sl'])])}")
                    print(best_results.tail(10))
                    db.save_backtest_results(best_results, strategy['name'])
                else:
                    print("No trades were executed.")

                # Append strategy to strategies_config table with indicator windows
                strategy_config = {
                    'name': strategy['name'],
                    'exchange': strategy['exchange'],
                    'symbol': strategy['symbol'],
                    'time_horizon': strategy['time_horizon'],
                    'tp': round(best_params.get('tp', 0.0), 2), 
                    'sl': round(best_params.get('sl', 0.0), 4),
                }
                # Add indicator enable/disable flags
                strategy_config.update({ind: strategy.get(ind, False) for ind in INDICATORS})
                # Add indicator window sizes
                window_indicators = [
                    'sma', 'ema', 'wma', 'dema', 'tema', 'trima', 'kama', 't3', 'midpoint', 'bbands',
                    'adx', 'adxr', 'aroon', 'aroonosc', 'cci', 'cmo', 'dx', 'mfi', 'minus_di', 'minus_dm',
                    'plus_di', 'plus_dm', 'rsi', 'trix', 'willr', 'atr', 'natr', 'trange'
                ]
                for ind in window_indicators:
                    window_key = f"{ind}_window"
                    if strategy.get(ind, False) and best_params and window_key in best_params:
                        strategy_config[window_key] = best_params[window_key]
                    else:
                        strategy_config[window_key] = 0

                db.save_strategies([strategy_config])
                print(f"Appended strategy {strategy['name']} to strategies_config table")

                metadata_file = f"optimization_results/{strategy['name']}_metadata.json"
                metadata = {
                    'strategy_name': strategy['name'],
                    'trial_number': best_trial_number,
                    'symbol': strategy['symbol'],
                    'time_horizon': strategy['time_horizon'],
                    'pnl_sum': best_pnl,
                    'optimized_params': best_params
                }
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=4)

            

if __name__ == "__main__":
    logging.info(f"Running optimizer.py at {datetime.datetime.now()}")
    optimizer = Optimizer("E:\\Neurog\\New\\cryptoPipeline\\optimization\\optuna_config.ini")
    optimizer.run()