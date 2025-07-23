import pandas as pd
from strategies.strategy_pipeline.utils.postgress_handler import DatabaseManager
from backtest.backtest import Backtester

def main(strategy_name: str):
    db = DatabaseManager()

    # Fetch strategy metadata
    metadata = db.fetch_strategy_metadata(strategy_name)
    exchange, symbol, time_horizon = metadata["exchange"], metadata["symbol"], metadata["time_horizon"]

    # Load 1-minute OHLCV data
    ohlcv = db.fetch_ohlcv_data(exchange, symbol, '1m')

    # Load strategy signals
    signals = db.fetch_strategy_signals(strategy_name)

    # Ensure datetime format and sorting
    ohlcv['datetime'] = pd.to_datetime(ohlcv['datetime'])
    signals['datetime'] = pd.to_datetime(signals['datetime'])

    # Instantiate backtester
    backtester = Backtester(ohlcv_df=ohlcv, signals_df=signals)

    # Run backtest
    result = backtester.run()

    # Display final balance and summary
    if not result.empty:
        result[['price', 'pnl_percent', 'pnl_sum', 'balance']] = result[[
            'price', 'pnl_percent', 'pnl_sum', 'balance'
        ]].round(2)
        print(f"\n Final Balance: {result.iloc[-1]['balance']:.2f}")
        print(f"Total Trades: {len(result[result['action'].isin(['tp', 'sl'])])}")
        print(result.tail(10))
                
        db.save_backtest_results(result, strategy_name)
    else:
        print("No trades were executed.")

if __name__ == "__main__":
    main("strategy_v1_1")  
