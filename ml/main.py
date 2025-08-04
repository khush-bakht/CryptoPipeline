import configparser
import os
import optuna
import pandas as pd
from typing import Dict, Any
import sqlite3
import numpy as np
import json

from data.downloader.data_downloader import DataDownloader
from ml.learner import (
    LinearRegressionLearner, RidgeRegressionLearner, LassoRegressionLearner,
    DecisionTreeLearner, RandomForestLearner,
    SVRLearner, KNNRegressionLearner, MLPRegressorLearner
)
from backtest.backtest import Backtester


def load_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read('E:\\Neurog\\New\\cryptoPipeline\\ml\\ml_config.ini')
    return config


def initialize_learners() -> Dict[str, Any]:
    return {
        'linear_regression': LinearRegressionLearner,
        'ridge': RidgeRegressionLearner,
        'lasso': LassoRegressionLearner,
        'decision_tree': DecisionTreeLearner,
        'random_forest': RandomForestLearner,
        'svr': SVRLearner,
        'knn': KNNRegressionLearner,
        'mlp': MLPRegressorLearner
    }


def run_pipeline():
    config = load_config()
    downloader = DataDownloader()

    symbols = [s.strip() for s in config['DATA']['symbol_list'].split(',')]
    time_horizons = [t.strip() for t in config['DATA']['time_horizons'].split(',')]
    models_to_train = [m.strip() for m in config['train']['models'].split(',')]

    start_date = config['dates']['start_date']
    end_date = config['dates']['end_date']
    n_trials = int(config['optimization']['n_trials'])

    model_classes = initialize_learners()

    for symbol in symbols:
        for time_horizon in time_horizons:
            print(f"\n=== Training models for {symbol} - {time_horizon} ===")

            try:
                df_1m = downloader.download(config['DATA']['exchange'], symbol, '1m', start_date, end_date)
                df_resampled = df_1m if time_horizon == '1m' else downloader.resample(df_1m, time_horizon)

                df_resampled['target'] = df_resampled['close'].shift(-1)
                df_resampled = df_resampled.dropna().reset_index(drop=True)

                X = df_resampled[['open', 'high', 'low', 'close', 'volume']]
                y = df_resampled['target']

                for model_name in models_to_train:
                    if model_name not in model_classes:
                        print(f"Model '{model_name}' not found")
                        continue

                    print(f"\nTraining {model_name}...")
                    model_path = f"E:/Neurog/New/cryptoPipeline/ml/trainer/{symbol}/{time_horizon}/{model_name}"
                    os.makedirs(model_path, exist_ok=True)

                    learner = model_classes[model_name](symbol, time_horizon, model_name)
                    best_trial_data = {"trial": None, "params": None, "pnl_sum": float('-inf'), "preds": None}

                    def objective(trial):
                        params = learner.get_search_space(trial)
                        model = learner.train_model(X, y, params)
                        learner.best_model = model
                        preds = learner.predict(X)

                        df_pred = df_resampled.copy()
                        df_pred['predicted'] = preds
                        df_pred['datetime'] = pd.to_datetime(df_pred['datetime'])
                        df_pred = df_pred[['datetime', 'predicted']]

                        df_merged = pd.merge_asof(
                            df_1m.sort_values('datetime'),
                            df_pred.sort_values('datetime'),
                            on='datetime',
                            direction='backward'
                        ).dropna()

                        result = run_backtest(df_merged, df_merged['predicted'].values, trial, model_name, save=False)
                        pnl_sum = result['pnl_sum'].iloc[-1] if not result.empty else 0.0

                        if pnl_sum > best_trial_data['pnl_sum']:
                            best_trial_data.update({
                                "trial": trial,
                                "params": params,
                                "pnl_sum": pnl_sum,
                                "preds": df_merged['predicted'].values,
                                "ohlcv_df": df_merged
                            })

                        db_folder = os.path.join(model_path, "db")
                        os.makedirs(db_folder, exist_ok=True)
                        db_path = os.path.join(db_folder, "results.db")

                        with sqlite3.connect(db_path) as conn:
                            cursor = conn.cursor()
                            cursor.execute("""
                                CREATE TABLE IF NOT EXISTS trial_results (
                                    trial_number INTEGER,
                                    params TEXT,
                                    pnl_sum REAL
                                )
                            """)
                            cursor.execute("""
                                INSERT INTO trial_results (trial_number, params, pnl_sum)
                                VALUES (?, ?, ?)
                            """, (trial.number, json.dumps(params), pnl_sum))
                            conn.commit()

                        return pnl_sum

                    study = optuna.create_study(direction='maximize')
                    study.optimize(objective, n_trials=n_trials)

                    if best_trial_data["trial"] is not None:
                        final_result = run_backtest(
                            best_trial_data["ohlcv_df"],
                            best_trial_data["preds"],
                            best_trial_data["trial"],
                            model_name,
                            save=True
                        )
                        os.makedirs("Signals_results", exist_ok=True)
                        final_result.to_csv(
                            os.path.join("Signals_results", f"backtest_{model_name}_best_trial_{best_trial_data['trial'].number}.csv"),
                            index=False
                        )

            except Exception as e:
                print(f"Error with {symbol} {time_horizon}: {e}")


def run_backtest(ohlcv_df, predictions, trial, model_name, save=False):
    df = ohlcv_df.copy()
    df['predicted'] = predictions

    df['signal'] = np.where(
        df['predicted'] > df['close'], 1,
        np.where(df['predicted'] < df['close'], -1, 0)
    )

    signal_df = df[['datetime', 'signal']].copy()
    signal_df.rename(columns={'signal': 'final_signal'}, inplace=True)

    if save:
        os.makedirs("Signals_results", exist_ok=True)
        signal_file = f"signals_{model_name}_best_trial_{trial.number}.csv"
        signal_df.to_csv(os.path.join("Signals_results", signal_file), index=False)

    backtester = Backtester(ohlcv_df, signal_df)
    result = backtester.run()
    return result


if __name__ == "__main__":
    run_pipeline()
