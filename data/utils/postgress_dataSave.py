#data/utils/postgress_dataSaver.py
import pandas as pd
from data.utils.postgress_connection import PostgresConnection 
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

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
    
    def table_exists(self, exchange, symbol, interval):
        schema_name = f"{exchange.lower()}_data"
        table_name = self._format_table_name(symbol, interval)

        # Check if schema exists
        self.cursor.execute(
            "SELECT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = %s)",
            (schema_name,)
        )
        schema_exists = self.cursor.fetchone()[0]

        if not schema_exists:
            print(f"Schema '{schema_name}' does not exist.")
            return False

        # Check if table exists in the schema
        self.cursor.execute(
            """
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_schema = %s AND table_name = %s
            )
            """,
            (schema_name, table_name)
        )
        table_exists = self.cursor.fetchone()[0]

        if table_exists:
            print(f"Data already exists in '{schema_name}.{table_name}'")
        else:
            print(f"Table '{schema_name}.{table_name}' does not exist yet.")

        return table_exists
    
    def check_table_up_to_date(self, exchange, symbol, interval):
        """
        Check if table exists and if its latest record is within 1 minute of current time
        Returns: (is_up_to_date: bool, latest_timestamp: datetime or None)
        """
        if not self.table_exists(exchange, symbol, interval):
            return False, None

        schema_name = f"{exchange.lower()}_data"
        table_name = self._format_table_name(symbol, interval)
        
        # Get the latest timestamp from the table
        query = f"""
            SELECT MAX(datetime)
            FROM {schema_name}.{table_name}
        """
        self.cursor.execute(query)
        latest_timestamp = self.cursor.fetchone()[0]

        if latest_timestamp is None:
            return False, None

        # Consider data up-to-date if latest record is within 1 minute of current time
        current_time = datetime.utcnow()
        time_difference = current_time - latest_timestamp
        
        # Assuming 1-minute interval data, check if latest record is within 2 minutes
        # to account for processing delays
        is_up_to_date = time_difference <= timedelta(minutes=2)
        
        return is_up_to_date, latest_timestamp


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
            if_exists="append",
            index=False
        )
        
        print(f"Data ({df_to_save.shape}) saved to table '{table_name}' in schema: {exchange.lower()}_data successfully.")


    def close(self):
        self.cursor.close()
        self.conn.close()
        self.engine.dispose()