import sqlite3
import pandas as pd
import os

class DatabaseManager:
    def __init__(self, db_path="../db/sqlite_data.db"):  #This path when run from data folder
        self.db_path = db_path  
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def _format_table_name(self, exchange, symbol, interval):
        return f"{exchange.lower()}_{symbol.lower()}_{interval}"

    def save_dataframe(self, df, exchange, symbol, interval):
        table_name = self._format_table_name(exchange, symbol, interval)
        print(f"Saving data to table: {table_name}")

        # Ensure index is a column
        df_to_save = df.copy()
        df_to_save.reset_index(inplace=True)
        df_to_save.rename(columns={"index": "datetime"}, inplace=True)

        # Save to SQLite
        df_to_save.to_sql(table_name, self.conn, if_exists="replace", index=False)

        print(f"Data saved to table '{table_name}' successfully.")

    def read_dataframe(self, exchange, symbol, interval):
        table_name = self._format_table_name(exchange, symbol, interval)
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, self.conn, parse_dates=["datetime"])
        df.set_index("datetime", inplace=True)
        return df

    def close(self):
        self.conn.close()
