#strategies/strategy_pipeline/utils/postgress_handler.py
import pandas as pd
from sqlalchemy import create_engine, text
from strategies.strategy_pipeline.utils.indicator_utils import INDICATORS
from strategies.strategy_pipeline.utils.postgress_connection import PostgresConnection

class DatabaseManager:
    def __init__(self):
        # Initialize PostgresConnection
        self.pg_conn = PostgresConnection()
        self.engine = self.pg_conn.get_engine()
        self.cursor = self.pg_conn.get_cursor()
        self.conn = self.pg_conn.get_connection()

    
    def create_strategies_table(self):
        with self.engine.connect() as conn:
            create_table_query = f"""
                CREATE TABLE IF NOT EXISTS public.strategies_config (
                    name VARCHAR(50) PRIMARY KEY,
                    exchange VARCHAR(50),
                    symbol VARCHAR(50),
                    time_horizon VARCHAR(10),
                    {', '.join([f"{ind} BOOLEAN" for ind in INDICATORS])}
                )
            """
            conn.execute(text(create_table_query))
            conn.commit()
        print("Strategies_config table exists in public schema.")

    
    def save_strategies(self, strategies):
        self.create_strategies_table()
        df = pd.DataFrame(strategies)
        df.to_sql(
            'strategies_config',
            self.engine,
            schema='public',
            if_exists='append',
            index=False,
            method='multi'
        )
        
    def fetch_strategies(self):
            """Return the total number of strategies in the strategies_config table. Return 0 if table doesn't exist."""
            try:
                with self.engine.connect() as conn:
                    result = conn.execute(text("SELECT COUNT(*) FROM public.strategies_config"))
                    count = result.scalar()  # gets the single value from the result
                    return count
            except Exception as e:
                return 0
            
    def save_signals(self, df_signals, strategy_name):
        """Save the signal DataFrame to the strategy_signal schema with the strategy_name as the table name."""
        # Create strategy_signal schema if it doesn't exist
        with self.engine.connect() as conn:
            self.cursor.execute(
                "SELECT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'strategy_signal')"
            )
            schema_exists = self.cursor.fetchone()[0]
            if not schema_exists:
                print("Creating schema: strategy_signal")
                self.cursor.execute("CREATE SCHEMA strategy_signal")
                conn.commit()

        # Ensure datetime is a column
        if df_signals.index.name == 'datetime':
            df_signals = df_signals.reset_index()

        # Verify required columns
        required_cols = ['datetime', 'final_signal']
        if not all(col in df_signals.columns for col in required_cols):
            print(f"Error: DataFrame for {strategy_name} missing required columns {required_cols}")
            return

        # Save to database
        table_name = strategy_name
        print(f"Saving signals to table: strategy_signal.{table_name}")
        df_signals.to_sql(
            table_name,
            self.engine,
            schema='strategy_signal',
            if_exists='replace',  # Replace existing table; use 'append' if you want to add data
            index=False,
            method='multi'
        )
        print(f"Signals saved to strategy_signal.{table_name} successfully.")
    
    def fetch_ohlcv_data(self, exchange: str, symbol: str, time_horizon: str) -> pd.DataFrame:
        """
        Fetch OHLCV data from schema 'binance_data' or other exchange-based schema.
        Always fetch data at '1m' resolution regardless of the strategy time horizon.
        """
        table_name = f"{symbol.lower()}_1m"  # Always 1-minute table
        schema_name = f"{exchange.lower()}_data"

        query = f"""
            SELECT datetime, open, high, low, close, volume
            FROM {schema_name}.{table_name}
            ORDER BY datetime
        """
        print(f"Downloading data from table: {schema_name}.{table_name}")
        df = pd.read_sql(query, self.engine, parse_dates=["datetime"])
        return df


    def fetch_strategy_signals(self, strategy_name: str) -> pd.DataFrame:
        """
        Fetch signals from strategy_signal.<strategy_name> table.
        """
        table = f"strategy_signal.{strategy_name}"

        query = f"""
            SELECT datetime, final_signal
            FROM {table}
            ORDER BY datetime
        """
        print(f"Fetching signals from table: {table}")
        df = pd.read_sql(query, self.engine, parse_dates=["datetime"])
        return df


    def fetch_strategy_metadata(self, strategy_name):
        """Fetch metadata (exchange, symbol, time_horizon) for a given strategy name from strategies_config."""
        with self.engine.connect() as conn:
            result = conn.execute(
                text("SELECT exchange, symbol, time_horizon FROM public.strategies_config WHERE name = :name"),
                {"name": strategy_name}
            ).mappings().first()  # Use mappings() to access columns by name

            if result:
                return {
                    "exchange": result["exchange"],
                    "symbol": result["symbol"],
                    "time_horizon": result["time_horizon"]
                }
            else:
                raise ValueError(f"Strategy '{strategy_name}' not found in strategies_config.")

            
    def save_backtest_results(self, df_results, strategy_name):
        """
        Save the backtest results DataFrame to the 'backtest' schema with the strategy_name as the table name.
        """
        # Create backtest schema if it doesn't exist
        with self.engine.connect() as conn:
            self.cursor.execute(
                "SELECT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'backtest')"
            )
            schema_exists = self.cursor.fetchone()[0]
            if not schema_exists:
                print("Creating schema: backtest")
                self.cursor.execute("CREATE SCHEMA backtest")
                conn.commit()

        # Ensure datetime is a column
        if df_results.index.name == 'datetime':
            df_results = df_results.reset_index()

        # Required columns for validation (adjust as needed)
        required_cols = ['datetime', 'action', 'price', 'pnl_percent', 'pnl_sum', 'balance']
        if not all(col in df_results.columns for col in required_cols):
            print(f"Error: DataFrame for {strategy_name} missing required columns: {required_cols}")
            return

        # Save to database
        table_name = strategy_name
        print(f"Saving backtest results to table: backtest.{table_name}")
        df_results.to_sql(
            table_name,
            self.engine,
            schema='backtest',
            if_exists='replace',  
            index=False,
            method='multi'
        )
        print(f"Backtest results saved to backtest.{table_name} successfully.")



    def close(self):
        """Close database connections and dispose of the engine."""
        self.cursor.close()
        self.conn.close()
        self.engine.dispose()



