import pandas as pd
import time
import datetime
from pybit.unified_trading import HTTP
import os
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(
    filename='Execution/Bybit/trade_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables
load_dotenv()
API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_SECRET_KEY")

# Initialize Bybit client
client = HTTP(
    demo=True,
    api_key=API_KEY,
    api_secret=API_SECRET
)

class BybitFetcher:
    def __init__(self, symbol, interval, start_time, end_time="now"):
        symbol = symbol.upper()
        if not symbol.endswith('USDT'):
            symbol += 'USDT'
        self.symbol = symbol
        self.interval = interval
        self.start_time = start_time
        self.end_time = end_time

    def get_klines(self):
        all_data = []
        limit = 1000
        start_ts = int(pd.to_datetime(self.start_time).timestamp() * 1000)
        end_ts = int(pd.Timestamp.utcnow().timestamp() * 1000) if self.end_time == "now" else int(pd.to_datetime(self.end_time).timestamp() * 1000)

        interval_map = {
            '1m': '1',
            '5m': '5',
            '15m': '15',
            '30m': '30',
            '1h': '60',
            '4h': '240',
            '1d': 'D'
        }
        bybit_interval = interval_map.get(self.interval, '1')

        iteration = 0
        max_iterations = 10000
        previous_end_ts = None

        while True:
            iteration += 1
            if iteration > max_iterations:
                break

            try:
                klines = client.get_kline(
                    category="linear",
                    symbol=self.symbol,
                    interval=bybit_interval,
                    start=start_ts,
                    end=end_ts,
                    limit=limit
                )

                if not klines or 'result' not in klines or 'list' not in klines['result']:
                    break

                raw_klines = klines['result']['list']
                if not raw_klines:
                    break

                all_data.extend(raw_klines)
                new_end_ts = int(raw_klines[-1][0]) - 1

                if previous_end_ts == new_end_ts:
                    break
                previous_end_ts = end_ts

                end_ts = new_end_ts
                if end_ts <= start_ts:
                    break

                time.sleep(0.2)

            except Exception as e:
                break

        if not all_data:
            return pd.DataFrame()

        df = pd.DataFrame(all_data, columns=["datetime", "open", "high", "low", "close", "volume", "turnover"])
        df["datetime"] = pd.to_datetime(pd.to_numeric(df["datetime"]), unit="ms", utc=True)
        df = df[["datetime", "open", "high", "low", "close", "volume"]]
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float).round(3)
        df = df.sort_values("datetime")
        df.set_index("datetime", inplace=True)
        df = df.iloc[:-1]
        return df

def fetch_fees(symbol="BTCUSDT"):
    try:
        # Try the fee rate endpoint (may not work with demo accounts)
        fee_data = client.get_fee_rates(category="linear", symbol=symbol)
        
        if 'result' in fee_data and fee_data['result']['list']:
            taker_fee = float(fee_data['result']['list'][0]['takerFeeRate'])
            logging.info(f"Fetched taker fee for {symbol}: {taker_fee}")
            return taker_fee
            
    except Exception as e:
        logging.info(f"Fee endpoint not accessible (common with demo accounts): {e}")
    
    # Use standard Bybit linear futures taker fee
    default_fee = 0.0006  # 0.06% - standard Bybit taker fee
    logging.info(f"Using standard Bybit taker fee: {default_fee}")
    return default_fee

def fetch_current_price(symbol="BTCUSDT"):
    try:
        ticker = client.get_tickers(category="linear", symbol=symbol)
        price = float(ticker['result']['list'][0]['lastPrice'])
        logging.info(f"Fetched current price for {symbol}: {price}")
        return price
    except Exception as e:
        logging.error(f"Error fetching price: {e}")
        return None

def fetch_balance():
    try:
        balance_data = client.get_wallet_balance(accountType="UNIFIED")
        
        if 'result' not in balance_data or not balance_data['result']['list']:
            logging.error("No balance data found in response")
            return 50000
        
        account_data = balance_data['result']['list'][0]
        
        # Use total available balance - this is your actual trading balance
        if 'totalAvailableBalance' in account_data and account_data['totalAvailableBalance']:
            total_balance = float(account_data['totalAvailableBalance'])
            logging.info(f"Fetched total available balance: {total_balance} USDT")
            return total_balance
        
        # Fallback to total wallet balance
        if 'totalWalletBalance' in account_data and account_data['totalWalletBalance']:
            wallet_balance = float(account_data['totalWalletBalance'])
            logging.info(f"Fetched total wallet balance: {wallet_balance} USDT")
            return wallet_balance
        
        logging.error("Could not find valid balance")
        return 50000
        
    except Exception as e:
        logging.error(f"Error fetching balance: {e}")
        return 50000

def calculate_position_quantity(position_size_usdt, entry_price):
    """Calculate BTC quantity for given USDT position size"""
    quantity = position_size_usdt / entry_price
    quantity = round(quantity, 3)  # Round to Bybit's precision
    
    # Check minimum order size
    if quantity < 0.001:
        logging.warning(f"Calculated quantity {quantity} BTC is below minimum, using 0.001 BTC")
        quantity = 0.001
    
    actual_usdt_value = quantity * entry_price
    logging.info(f"Position: {quantity} BTC = ${actual_usdt_value:.2f} USDT at ${entry_price}")
    
    return quantity

def place_order(symbol, side, quantity, price, tp_price, sl_price):
    try:
        # Round quantity to 3 decimal places (Bybit's qtyStep for BTCUSDT is 0.001)
        quantity = round(quantity, 3)
        
        # Ensure minimum order size (usually 0.001 BTC for BTCUSDT)
        if quantity < 0.001:
            logging.error(f"Quantity {quantity} is below minimum order size")
            return None, None
        
        logging.info(f"Placing {side} order: {quantity} BTC at ${price}, TP: ${tp_price}, SL: ${sl_price}")
        
        order = client.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=str(quantity),  # Convert to string
            takeProfit=str(round(tp_price, 2)),
            stopLoss=str(round(sl_price, 2))
        )
        order_id = order['result']['orderId']
        logging.info(f"Order placed successfully, order_id: {order_id}")
        return order_id, price
    except Exception as e:
        logging.error(f"Error placing order: {e}")
        return None, None

def close_position(symbol, quantity, side="Sell"):
    try:
        quantity = round(quantity, 3)
        
        order = client.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=str(quantity),
            reduceOnly=True
        )
        order_id = order['result']['orderId']
        
        # Get executed price
        time.sleep(1)  # Wait for order to execute
        order_details = client.get_order_history(category="linear", symbol=symbol, orderId=order_id)
        executed_price = float(order_details['result']['list'][0]['avgPrice'])
        
        logging.info(f"Closed position for {symbol}, qty: {quantity}, executed_price: {executed_price}, order_id: {order_id}")
        return order_id, executed_price
    except Exception as e:
        logging.error(f"Error closing position: {e}")
        return None, None

def get_position(symbol="BTCUSDT"):
    try:
        positions = client.get_positions(category="linear", symbol=symbol)
        position_list = positions['result']['list']
        if position_list and float(position_list[0]['size']) > 0:
            return {
                'size': float(position_list[0]['size']),
                'side': position_list[0]['side'],
                'entry_price': float(position_list[0]['avgPrice'])
            }
        return None
    except Exception as e:
        logging.error(f"Error checking position: {e}")
        return None

def main():
    logging.info("=== Starting Bybit Trading Bot ===")
    
    symbol = "BTCUSDT"
    tp = 0.0009  # 1% take profit
    sl = 0.001  # 3% stop loss
    time_horizon = "1h"
    position_size_usdt = 1000  # $1000 per trade

    # Dynamic signals that work anytime you run the bot
    current_time = pd.Timestamp.now(tz='UTC')
    signals_df = pd.DataFrame({
        'datetime': [
            current_time - pd.Timedelta(minutes=5),  # 5 minutes ago
            current_time + pd.Timedelta(minutes=10)     # 1 hour from now
        ],
        'signal': [1, -1]  # Current: Buy, Next: Sell
    })
    

    # Initialize
    initial_balance = fetch_balance()
    ledger = []
    taker_fee = fetch_fees(symbol)
    
    logging.info(f"Initial balance: ${initial_balance}, Fee rate: {taker_fee*100}%")

    # Check for current signal
    current_time = pd.Timestamp.now(tz='UTC')
    current_signal = signals_df[signals_df['datetime'] <= current_time].tail(1)
    
    if current_signal.empty or current_signal['signal'].iloc[0] not in [1, -1]:
        logging.info("No valid signal at current time, exiting")
        return

    signal = current_signal['signal'].iloc[0]
    signal_time = current_signal['datetime'].iloc[0]
    
    logging.info(f"Found signal: {signal} ({'Buy' if signal == 1 else 'Sell'}) at {signal_time}")

    # Get current price and calculate position
    entry_price = fetch_current_price(symbol)
    if not entry_price:
        logging.error("Failed to fetch current price, exiting")
        return

    quantity = calculate_position_quantity(position_size_usdt, entry_price)
    position = get_position(symbol)

    # Place order if no existing position
    if not position:
        if signal == 1:  # Buy signal
            side = "Buy"
            tp_price = entry_price * (1 + tp)
            sl_price = entry_price * (1 - sl)
        elif signal == -1:  # Sell signal
            side = "Sell"
            tp_price = entry_price * (1 - tp)
            sl_price = entry_price * (1 + sl)
        else:
            return

        order_id, executed_price = place_order(symbol, side, quantity, entry_price, tp_price, sl_price)
        if not order_id:
            logging.error("Failed to place order, exiting")
            return

        # Record trade in ledger
        fee_cost = position_size_usdt * taker_fee
        current_balance = initial_balance - fee_cost
        
        ledger.append({
            'datetime': pd.Timestamp.now(tz='UTC'),
            'action': side.lower(),
            'buy_price': executed_price if side == "Buy" else 0.0,
            'sell_price': executed_price if side == "Sell" else 0.0,
            'quantity': quantity,
            'pnl_percent': -taker_fee * 100,  # Entry fee
            'pnl_sum': -taker_fee * 100,
            'balance': current_balance
        })
        
        logging.info(f"Position opened: {side} {quantity} BTC at ${executed_price}")
    else:
        logging.info(f"Existing position found: {position}")
        executed_price = position['entry_price']
        if signal == 1:
            tp_price = executed_price * (1 + tp)
            sl_price = executed_price * (1 - sl)
        else:
            tp_price = executed_price * (1 - tp)
            sl_price = executed_price * (1 + sl)

    # Monitor position for TP/SL
    monitoring_end = signal_time + pd.Timedelta(hours=1)
    logging.info(f"Monitoring position until {monitoring_end}")
    
    while pd.Timestamp.now(tz='UTC') < monitoring_end:
        try:
            # Get recent price data
            fetcher = BybitFetcher(
                symbol=symbol,
                interval="1m",
                start_time=(pd.Timestamp.utcnow() - pd.Timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S')
            )
            price_df = fetcher.get_klines()
            
            if price_df.empty:
                time.sleep(30)
                continue

            current_price_df = price_df.tail(1)
            current_price = current_price_df['close'].iloc[0]
            high_price = current_price_df['high'].iloc[0]
            low_price = current_price_df['low'].iloc[0]

            # Check if position still exists
            position = get_position(symbol)
            if not position:
                logging.info("Position closed externally or by TP/SL")
                break

            # Check TP/SL conditions
            action = None
            exit_price = None
            
            if position['side'] == "Buy":
                if high_price >= tp_price:
                    action = "tp"
                    order_id, exit_price = close_position(symbol, position['size'], "Sell")
                elif low_price <= sl_price:
                    action = "sl"
                    order_id, exit_price = close_position(symbol, position['size'], "Sell")
            else:  # Sell position
                if low_price <= tp_price:
                    action = "tp"
                    order_id, exit_price = close_position(symbol, position['size'], "Buy")
                elif high_price >= sl_price:
                    action = "sl"
                    order_id, exit_price = close_position(symbol, position['size'], "Buy")

            if action and exit_price:
                # Calculate PnL
                if position['side'] == "Buy":
                    gross_pnl_percent = (exit_price - executed_price) / executed_price
                else:
                    gross_pnl_percent = (executed_price - exit_price) / executed_price
                
                net_pnl_percent = gross_pnl_percent - taker_fee  # Subtract exit fee
                current_balance = initial_balance + (position_size_usdt * net_pnl_percent)
                
                # Record exit in ledger
                ledger.append({
                    'datetime': pd.Timestamp.now(tz='UTC'),
                    'action': action,
                    'buy_price': executed_price if position['side'] == "Buy" else exit_price,
                    'sell_price': exit_price if position['side'] == "Buy" else executed_price,
                    'quantity': position['size'],
                    'pnl_percent': net_pnl_percent * 100,
                    'pnl_sum': sum([x['pnl_percent'] for x in ledger]),
                    'balance': current_balance
                })
                
                logging.info(f"Position closed by {action.upper()}: PnL = {net_pnl_percent*100:.2f}%, Balance = ${current_balance:.2f}")
                break
            
            # Log current status
            if position['side'] == "Buy":
                unrealized_pnl = ((current_price - executed_price) / executed_price) * 100
            else:
                unrealized_pnl = ((executed_price - current_price) / executed_price) * 100
                
            logging.info(f"Current price: ${current_price}, Unrealized PnL: {unrealized_pnl:.2f}%")
            
            time.sleep(30)  # Check every 30 seconds
            
        except Exception as e:
            logging.error(f"Error in monitoring loop: {e}")
            time.sleep(30)

    # Save ledger
    if ledger:
        ledger_df = pd.DataFrame(ledger)
        ledger_df.to_csv("Execution/Bybit/trade_ledger.csv", index=False)
        logging.info("Ledger saved to trade_ledger.csv")
    
    # Wait for next signal
    next_signal_time = signal_time + pd.Timedelta(hours=1)
    logging.info(f"Waiting for next signal at {next_signal_time}")

if __name__ == "__main__":
    main()