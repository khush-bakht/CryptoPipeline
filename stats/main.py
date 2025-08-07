from strategies.strategy_pipeline.utils.postgress_connection import PostgresConnection
from stats.generate_stats import generate_stats_from_backtest
import pandas as pd

def create_stats_schema_and_table(cursor):
    """Create stats schema and table if they don't exist"""
    try:
        cursor.execute("CREATE SCHEMA IF NOT EXISTS stats")
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS stats.strategy_stats (
            strategy_name VARCHAR(255),
            total_return DECIMAL(10,4),
            daily_return DECIMAL(10,4),
            weekly_return DECIMAL(10,4),
            monthly_return DECIMAL(10,4),
            cagr DECIMAL(10,4),
            sharpe_ratio DECIMAL(10,4),
            sortino_ratio DECIMAL(10,4),
            calmar_ratio DECIMAL(10,4),
            alpha DECIMAL(10,4),
            beta DECIMAL(10,4),
            r_squared DECIMAL(10,4),
            information_ratio DECIMAL(10,4),
            treynor_ratio DECIMAL(10,4),
            profit_factor DECIMAL(10,4),
            omega_ratio DECIMAL(10,4),
            gain_to_pain_ratio DECIMAL(10,4),
            payoff_ratio DECIMAL(10,4),
            cpc_ratio DECIMAL(10,4),
            risk_return_ratio DECIMAL(10,4),
            common_sense_ratio DECIMAL(10,4),
            max_drawdown DECIMAL(10,4),
            max_drawdown_days INTEGER,
            avg_drawdown DECIMAL(10,4),
            avg_drawdown_days DECIMAL(10,4),
            current_drawdown DECIMAL(10,4),
            current_drawdown_days INTEGER,
            drawdown_duration INTEGER,
            conditional_drawdown_at_risk DECIMAL(10,4),
            ulcer_index DECIMAL(10,4),
            risk_of_ruin DECIMAL(10,4),
            var_95 DECIMAL(10,4),
            cvar_99 DECIMAL(10,4),
            downside_deviation DECIMAL(10,4),
            volatility DECIMAL(10,4),
            annualized_volatility DECIMAL(10,4),
            skewness DECIMAL(10,4),
            kurtosis DECIMAL(10,4),
            winning_weeks INTEGER,
            losing_weeks INTEGER,
            winning_months INTEGER,
            losing_months INTEGER,
            winning_months_percent DECIMAL(10,4),
            negative_months_percent DECIMAL(10,4),
            total_profit DECIMAL(10,4),
            net_profit DECIMAL(10,4),
            avg_profit_per_trade DECIMAL(10,4),
            avg_loss_per_trade DECIMAL(10,4),
            profit_loss_ratio DECIMAL(10,4),
            number_of_trades INTEGER,
            win_rate DECIMAL(10,4),
            loss_rate DECIMAL(10,4),
            average_win DECIMAL(10,4),
            average_loss DECIMAL(10,4),
            average_trade_duration DECIMAL(10,4),
            largest_win DECIMAL(10,4),
            largest_loss DECIMAL(10,4),
            consecutive_wins INTEGER,
            consecutive_losses INTEGER,
            avg_trade_return DECIMAL(10,4),
            profitability_per_trade DECIMAL(10,4),
            recovery_factor DECIMAL(10,4),
            total_long_return DECIMAL(10,4),
            avg_long_return_per_trade DECIMAL(10,4),
            num_long_trades INTEGER,
            win_rate_long_trades DECIMAL(10,4),
            avg_long_trade_duration DECIMAL(10,4),
            max_long_trade_return DECIMAL(10,4),
            min_long_trade_return DECIMAL(10,4),
            long_trades_percent DECIMAL(10,4),
            total_short_return DECIMAL(10,4),
            avg_short_return_per_trade DECIMAL(10,4),
            num_short_trades INTEGER,
            win_rate_short_trades DECIMAL(10,4),
            avg_short_trade_duration DECIMAL(10,4),
            max_short_trade_return DECIMAL(10,4),
            min_short_trade_return DECIMAL(10,4),
            short_trades_percent DECIMAL(10,4),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_sql)
        print("Stats schema and table created successfully")
    except Exception as e:
        print(f"Error creating schema/table: {e}")

def main():
    pg = PostgresConnection()
    engine = pg.get_engine()
    cursor = pg.get_cursor()
    
    try:
        create_stats_schema_and_table(cursor)
        cursor.execute("SELECT name FROM public.strategies_config")
        strategy_names = [row[0] for row in cursor.fetchall()]
        print(f"Found {len(strategy_names)} strategies to process")
        cursor.execute("DELETE FROM stats.strategy_stats")
        print("Cleared existing stats")
        
        for i, strategy in enumerate(strategy_names, 1):
            try:
                print(f"Processing strategy {i}/{len(strategy_names)}: {strategy}")
                df = pd.read_sql(f'SELECT * FROM backtest."{strategy}"', engine)
                
                if df.empty:
                    print(f"No data found for strategy: {strategy}")
                    continue
                
                stats_df = generate_stats_from_backtest(df)
                
                if stats_df.empty:
                    print(f"No stats generated for strategy: {strategy}")
                    continue
                
                stats_df["strategy_name"] = strategy
                stats_df.to_sql("strategy_stats", engine, schema="stats", if_exists="append", index=False)
                print(f"Successfully processed strategy: {strategy}")
            except Exception as e:
                print(f"Failed for {strategy}: {e}")
                continue
        
        print("Stats generation completed!")
    except Exception as e:
        print(f"Error in main execution: {e}")
    finally:
        pg.close()

if __name__ == "__main__":
    main()