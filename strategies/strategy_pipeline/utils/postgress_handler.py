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




    def close(self):
        """Close database connections and dispose of the engine."""
        self.cursor.close()
        self.conn.close()
        self.engine.dispose()



