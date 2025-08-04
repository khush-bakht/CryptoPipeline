import pandas as pd
from strategies.strategy_pipeline.utils.postgress_handler import DatabaseManager


def main(strategy_name: str):
    db = DatabaseManager()

    # Fetch strategy metadata
    metadata = db.fetch_strategy_metadata(strategy_name)
    exchange, symbol, time_horizon = metadata["exchange"], metadata["symbol"], metadata["time_horizon"]
    #exchange, symbol = "bybit" , "btc"





if __name__ == "__main__":
    main("strategy_opt_1")  
