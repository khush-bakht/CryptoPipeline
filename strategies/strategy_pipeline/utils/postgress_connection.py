#strategies/strategy_pipeline/utils/postgress_connection.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import psycopg2

load_dotenv()

class PostgresConnection:
    def __init__(self):
        # Load PostgreSQL credentials from .env
        self.db_name = os.getenv("PG_DATABASE")
        self.user = os.getenv("PG_USER")
        self.password = os.getenv("PG_PASSWORD")
        self.host = os.getenv("PG_HOST")
        self.port = os.getenv("PG_PORT")
        
        if not all([self.db_name, self.user, self.password, self.host, self.port]):
            raise ValueError("Missing PostgreSQL credentials in .env file")
        
        # Create SQLAlchemy engine
        self.engine = create_engine(f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}")
        
        # Create psycopg2 connection for schema operations
        self.conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def get_engine(self):
        return self.engine

    def get_connection(self):
        return self.conn

    def get_cursor(self):
        return self.cursor

    def close(self):
        self.cursor.close()
        self.conn.close()
        self.engine.dispose()