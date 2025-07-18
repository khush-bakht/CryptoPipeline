#data/utils/postgress_dataSaver.py
import pandas as pd
from data.utils.postgress_connection import PostgresConnection 
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        # Initialize PostgresConnection
        self.pg_conn = PostgresConnection()
        self.engine = self.pg_conn.get_engine()
        self.cursor = self.pg_conn.get_cursor()
        self.conn = self.pg_conn.get_connection()

    def _format_table_name(self, symbol, interval):

        return f"{symbol.lower()}_{interval}"

    def _schema_exists(self, exchange):
        schema_name = f"{exchange.lower()}_data"
        self.cursor.execute(
            "SELECT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = %s)",
            (schema_name,)
        )
        schema_exists = self.cursor.fetchone()[0]
        if not schema_exists:
            print(f"Creating schema: {schema_name}")
            self.cursor.execute(f"CREATE SCHEMA {schema_name}")

    def save_dataframe(self, df, exchange, symbol, interval):
        table_name = self._format_table_name(symbol, interval)
        print(f"Saving data to table: {table_name} in schema: {exchange.lower()}_data")

        self._schema_exists(exchange)

        df_to_save = df.copy()
        df_to_save.reset_index(inplace=True)
        df_to_save.rename(columns={"index": "datetime"}, inplace=True)
 
        df_to_save.to_sql(
            table_name,
            self.engine,
            schema=f"{exchange.lower()}_data",
            if_exists="replace",
            index=False
        )
        
        print(f"Data ({df_to_save.shape}) saved to table '{table_name}' in schema: {exchange.lower()}_data successfully.")


    def close(self):
        self.cursor.close()
        self.conn.close()
        self.engine.dispose()