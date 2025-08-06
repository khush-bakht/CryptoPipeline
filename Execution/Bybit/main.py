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
        fee_data = client.get_fee_rates(category="linear", symbol=symbol)
        
        if 'result' in fee_data and fee_data['result']['list']:
            taker_fee = float(fee_data['result']['list'][0]['takerFeeRate'])
            logging.info(f"Fetched taker fee for {symbol}: {taker_fee}")
            return taker_fee
            
    except Exception as e:
        logging.info(f"Fee endpoint not accessible (common with demo accounts): {e}")
    
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
        
        if 'totalAvailableBalance' in account_data and account_data['totalAvailableBalance']:
            total_balance = float(account_data['totalAvailableBalance'])
            logging.info(f"Fetched total available balance: {total_balance} USDT")
            return total_balance
        
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
    quantity = round(quantity, 3)
    
    if quantity < 0.001:
        logging.warning(f"Calculated quantity {quantity} BTC is below minimum, using 0.001 BTC")
        quantity = 0.001
    
    actual_usdt_value = quantity * entry_price
    logging.info(f"Position: {quantity} BTC = ${actual_usdt_value:.2f} USDT at ${entry_price}")
    
    return quantity

def place_order(symbol, side, quantity, price, tp_price, sl_price):
    try:
        quantity = round(quantity, 3)
        
        if quantity < 0.001:
            logging.error(f"Quantity {quantity} is below minimum order size")
            return None, None
        
        logging.info(f"Placing {side} order: {quantity} BTC at ${price}, TP: ${tp_price}, SL: ${sl_price}")
        
        order = client.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=str(quantity),
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
        
        time.sleep(1)
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

def load_existing_ledger(ledger_file="Execution/Bybit/trade_ledger.csv"):
    """Load existing ledger or create new one"""
    try:
        if os.path.exists(ledger_file):
            ledger_df = pd.read_csv(ledger_file)
            logging.info(f"Loaded existing ledger with {len(ledger_df)} records")
            return ledger_df.to_dict('records')
        else:
            logging.info("No existing ledger found, starting fresh")
            return []
    except Exception as e:
        logging.error(f"Error loading ledger: {e}")
        return []

def save_single_trade(trade_entry, ledger_file="Execution/Bybit/trade_ledger.csv"):
    """Save a single trade entry immediately to CSV"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(ledger_file), exist_ok=True)
        
        # Convert single entry to DataFrame
        trade_df = pd.DataFrame([trade_entry])
        
        # Append to existing file or create new one
        if os.path.exists(ledger_file):
            trade_df.to_csv(ledger_file, mode='a', header=False, index=False)
        else:
            trade_df.to_csv(ledger_file, index=False)
        
        logging.info(f"SAVED TRADE: {trade_entry['action']} - PnL: {trade_entry['pnl_percent']:.2f}% - Balance: ${trade_entry['balance']:.2f}")
        
    except Exception as e:
        logging.error(f"ERROR saving trade: {e}")

def calculate_pnl_sum(existing_ledger):
    """Calculate cumulative PnL from existing ledger"""
    if not existing_ledger:
        return 0.0
    
    return sum([record.get('pnl_percent', 0) for record in existing_ledger])

def calculate_current_balance(existing_ledger, initial_balance):
    """Calculate current balance from existing ledger"""
    if not existing_ledger:
        return initial_balance
    
    # Get the last recorded balance
    last_entry = existing_ledger[-1]
    return last_entry.get('balance', initial_balance)

def handle_direction_change(symbol, current_position, new_signal, current_price, taker_fee, position_size_usdt, current_pnl_sum, current_balance):
    """Handle direction change similar to backtest logic with immediate saving"""
    
    # Close existing position first
    close_side = "Sell" if current_position['side'] == "Buy" else "Buy"
    order_id, exit_price = close_position(symbol, current_position['size'], close_side)
    
    if not order_id:
        logging.error("Failed to close position for direction change")
        return None, current_pnl_sum, current_balance
    
    # Calculate PnL for closed position
    entry_price = current_position['entry_price']
    if current_position['side'] == "Buy":
        gross_pnl_percent = (exit_price - entry_price) / entry_price
    else:
        gross_pnl_percent = (entry_price - exit_price) / entry_price
    
    net_pnl_percent = gross_pnl_percent - taker_fee  # Exit fee
    current_balance += position_size_usdt * net_pnl_percent
    current_pnl_sum += net_pnl_percent * 100
    
    # Record and IMMEDIATELY save the close
    close_entry = {
        'datetime': pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%d %H:%M:%S.%f'),
        'action': 'direction_change',
        'buy_price': entry_price if current_position['side'] == "Buy" else exit_price,
        'sell_price': exit_price if current_position['side'] == "Buy" else entry_price,
        'quantity': current_position['size'],
        'pnl_percent': net_pnl_percent * 100,
        'pnl_sum': current_pnl_sum,
        'balance': current_balance
    }
    
    save_single_trade(close_entry) 
    
    logging.info(f"Direction change: Closed {current_position['side']} position at ${exit_price}, PnL: {net_pnl_percent*100:.2f}%")
    
    # Now open new position in opposite direction
    quantity = calculate_position_quantity(position_size_usdt, current_price)
    
    if new_signal == 1:  # Buy
        side = "Buy"
        tp_price = current_price * (1 + 0.0009)  # Your TP
        sl_price = current_price * (1 - 0.001)   # Your SL
    else:  # Sell
        side = "Sell"
        tp_price = current_price * (1 - 0.0009)
        sl_price = current_price * (1 + 0.001)
    
    order_id, executed_price = place_order(symbol, side, quantity, current_price, tp_price, sl_price)
    
    if order_id:
        # Update balance and PnL for entry fee
        current_balance -= position_size_usdt * taker_fee
        current_pnl_sum += (-taker_fee * 100)
        
        # Record and IMMEDIATELY save the new entry
        entry_entry = {
            'datetime': pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%d %H:%M:%S.%f'),
            'action': side.lower(),
            'buy_price': executed_price if side == "Buy" else 0.0,
            'sell_price': executed_price if side == "Sell" else 0.0,
            'quantity': quantity,
            'pnl_percent': -taker_fee * 100,
            'pnl_sum': current_pnl_sum,
            'balance': current_balance
        }
        
        save_single_trade(entry_entry)  
        
        logging.info(f"Direction change: Opened new {side} position at ${executed_price}")
        return {'side': side, 'size': quantity, 'entry_price': executed_price}, current_pnl_sum, current_balance
    
    return None, current_pnl_sum, current_balance

def detect_manual_position_change(symbol, tracked_position, current_pnl_sum, current_balance, position_size_usdt, taker_fee):
    """Detect if position was closed (manually or by TP/SL) and record it appropriately"""
    live_position = get_position(symbol)

    if tracked_position and not live_position:
        logging.info("🔍 POSITION CLOSED DETECTED (TP/SL/Manual)")

        current_price = fetch_current_price(symbol)
        if not current_price:
            logging.error("Cannot get price for position close detection")
            return tracked_position, current_pnl_sum, current_balance

        try:
            # Get the most recent orders (both active and history)
            orders = client.get_order_history(
                category="linear",
                symbol=symbol,
                limit=5
            )
            
            if not orders or 'result' not in orders or not orders['result']['list']:
                raise Exception("No order history available")

            # Check each order to find the closing one
            for order in orders['result']['list']:
                if order['orderStatus'] == 'Filled' and order['reduceOnly'] == True:
                    close_price = float(order.get('avgPrice', current_price))
                    
                    # Determine close type
                    if 'stopLoss' in order.get('orderLinkId', '').lower():
                        action_type = 'sl_close'
                        logging.info("Position closed via STOP LOSS")
                    elif 'takeProfit' in order.get('orderLinkId', '').lower():
                        action_type = 'tp_close'
                        logging.info("Position closed via TAKE PROFIT")
                    else:
                        action_type = 'manual_close'
                        logging.info("Position closed MANUALLY")
                    break
            else:
                raise Exception("No closing order found")

        except Exception as e:
            logging.warning(f"Could not determine close type. Assuming manual: {str(e)}")
            action_type = 'manual_close'
            close_price = current_price

        # Calculate PnL
        entry_price = tracked_position['entry_price']
        if tracked_position['side'] == "Buy":
            gross_pnl_percent = (close_price - entry_price) / entry_price
        else:
            gross_pnl_percent = (entry_price - close_price) / entry_price

        net_pnl_percent = gross_pnl_percent - taker_fee
        current_balance += position_size_usdt * net_pnl_percent
        current_pnl_sum += net_pnl_percent * 100

        close_entry = {
            'datetime': pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%d %H:%M:%S.%f'),
            'action': action_type,
            'buy_price': entry_price if tracked_position['side'] == "Buy" else close_price,
            'sell_price': close_price if tracked_position['side'] == "Buy" else entry_price,
            'quantity': tracked_position['size'],
            'pnl_percent': net_pnl_percent * 100,
            'pnl_sum': current_pnl_sum,
            'balance': current_balance
        }

        save_single_trade(close_entry)
        logging.info(f"Closed: {action_type.upper()} - PnL: {net_pnl_percent*100:.2f}% - Bal: ${current_balance:.2f}")

        return None, current_pnl_sum, current_balance

    return tracked_position, current_pnl_sum, current_balance

def main():
    logging.info("=== Starting Bybit Trading Bot ===")
    
    symbol = "BTCUSDT"
    tp = 0.009  # Take profit
    sl = 0.001     # Stop loss
    position_size_usdt = 1000
    
    # Load existing ledger
    existing_ledger = load_existing_ledger()
    current_pnl_sum = calculate_pnl_sum(existing_ledger)
    
    # Initialize
    initial_balance = fetch_balance()
    current_balance = calculate_current_balance(existing_ledger, initial_balance)
    taker_fee = fetch_fees(symbol)
    
    logging.info(f"Initial balance: ${initial_balance}, Current balance: ${current_balance:.2f}, Current PnL Sum: {current_pnl_sum:.2f}%, Fee rate: {taker_fee*100}%")

    # Dynamic signals for testing
    current_time = pd.Timestamp.now(tz='UTC')
    signals_df = pd.DataFrame({
        'datetime': [
            current_time - pd.Timedelta(minutes=5),
            current_time + pd.Timedelta(minutes=10)
        ],
        'signal': [1, -1]  # Buy now, Sell later
    })
    
    # Check for current signal
    current_signal = signals_df[signals_df['datetime'] <= current_time].tail(1)
    
    if current_signal.empty or current_signal['signal'].iloc[0] not in [1, -1]:
        logging.info("No valid signal at current time, exiting")
        return

    signal = current_signal['signal'].iloc[0]
    signal_time = current_signal['datetime'].iloc[0]
    
    logging.info(f"Found signal: {signal} ({'Buy' if signal == 1 else 'Sell'}) at {signal_time}")

    # Get current price and position
    entry_price = fetch_current_price(symbol)
    if not entry_price:
        logging.error("Failed to fetch current price, exiting")
        return

    current_position = get_position(symbol)
    
    # Handle different scenarios
    if not current_position:
        # No existing position - open new one
        quantity = calculate_position_quantity(position_size_usdt, entry_price)
        
        if signal == 1:  # Buy
            side = "Buy"
            tp_price = entry_price * (1 + tp)
            sl_price = entry_price * (1 - sl)
        else:  # Sell
            side = "Sell"
            tp_price = entry_price * (1 - tp)
            sl_price = entry_price * (1 + sl)

        order_id, executed_price = place_order(symbol, side, quantity, entry_price, tp_price, sl_price)
        if not order_id:
            logging.error("Failed to place order, exiting")
            return

        # Record entry and IMMEDIATELY save
        fee_cost = position_size_usdt * taker_fee
        current_balance -= fee_cost
        current_pnl_sum += (-taker_fee * 100)
        
        entry_trade = {
            'datetime': pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%d %H:%M:%S.%f'),
            'action': side.lower(),
            'buy_price': executed_price if side == "Buy" else 0.0,
            'sell_price': executed_price if side == "Sell" else 0.0,
            'quantity': quantity,
            'pnl_percent': -taker_fee * 100,
            'pnl_sum': current_pnl_sum,
            'balance': current_balance
        }
        
        save_single_trade(entry_trade)  
        
        current_position = {'side': side, 'size': quantity, 'entry_price': executed_price, 'open_time': pd.Timestamp.now(tz='UTC')}
        
        logging.info(f"New position opened: {side} {quantity} BTC at ${executed_price}")
        
    else:
        # Existing position - check for direction change
        position_signal = 1 if current_position['side'] == "Buy" else -1
        
        if signal != position_signal:
            # Direction change required
            logging.info(f"Direction change detected: Current={position_signal}, New={signal}")
            
            new_position, current_pnl_sum, current_balance = handle_direction_change(
                symbol, current_position, signal, entry_price, taker_fee, position_size_usdt, current_pnl_sum, current_balance
            )
            
            if new_position:
                current_position = new_position
                current_position['open_time'] = pd.Timestamp.now(tz='UTC')
                
                # Set new TP/SL levels
                if signal == 1:
                    tp_price = current_position['entry_price'] * (1 + tp)
                    sl_price = current_position['entry_price'] * (1 - sl)
                else:
                    tp_price = current_position['entry_price'] * (1 - tp)
                    sl_price = current_position['entry_price'] * (1 + sl)
            else:
                logging.error("Failed to handle direction change")
                return
        else:
            # Same direction - continue with existing position
            logging.info(f"Continuing with existing {current_position['side']} position")
            if signal == 1:
                tp_price = current_position['entry_price'] * (1 + tp)
                sl_price = current_position['entry_price'] * (1 - sl)
            else:
                tp_price = current_position['entry_price'] * (1 - tp)
                sl_price = current_position['entry_price'] * (1 + sl)
            # Ensure open_time is tracked
            if 'open_time' not in current_position:
                current_position['open_time'] = pd.Timestamp.now(tz='UTC')

    # Monitor position for TP/SL with manual detection
    monitoring_end = signal_time + pd.Timedelta(minutes=10)
    logging.info(f"Monitoring position until {monitoring_end}")
    
    while pd.Timestamp.now(tz='UTC') < monitoring_end:
        try:
            # Check for manual position changes FIRST
            current_position, current_pnl_sum, current_balance = detect_manual_position_change(
                symbol, current_position, current_pnl_sum, current_balance, position_size_usdt, taker_fee
            )
            
            if not current_position:
                logging.info("Position manually closed, ending monitoring")
                break
            
            # Get price data since position was opened
            fetcher = BybitFetcher(
                symbol=symbol,
                interval="1m",
                start_time=current_position['open_time'].strftime('%Y-%m-%d %H:%M:%S')
            )
            price_df = fetcher.get_klines()
            
            if price_df.empty:
                time.sleep(30)
                continue

            # Check if position still exists (could be closed by TP/SL)
            live_position = get_position(symbol)
            if not live_position and current_position:
                logging.info("Position closed by TP/SL or other means")
                
                # Determine if TP or SL was hit using historical data
                entry_price = current_position['entry_price']
                max_high = price_df['high'].max()
                min_low = price_df['low'].min()
                
                if current_position['side'] == "Buy":
                    if max_high >= tp_price:
                        action = "tp"
                        exit_price = tp_price  # Assume TP was hit at TP price
                    elif min_low <= sl_price:
                        action = "sl"
                        exit_price = sl_price  # Assume SL was hit at SL price
                    else:
                        action = "auto_close"
                        exit_price = price_df['close'].iloc[-1]  # Use latest close price
                    gross_pnl_percent = (exit_price - entry_price) / entry_price
                else:  # Sell position
                    if min_low <= tp_price:
                        action = "tp"
                        exit_price = tp_price
                    elif max_high >= sl_price:
                        action = "sl"
                        exit_price = sl_price
                    else:
                        action = "auto_close"
                        exit_price = price_df['close'].iloc[-1]
                    gross_pnl_percent = (entry_price - exit_price) / entry_price
                
                net_pnl_percent = gross_pnl_percent - taker_fee  # Exit fee
                current_balance += position_size_usdt * net_pnl_percent
                current_pnl_sum += net_pnl_percent * 100
                
                # Record exit and IMMEDIATELY save
                exit_trade = {
                    'datetime': pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%d %H:%M:%S.%f'),
                    'action': action,
                    'buy_price': entry_price if current_position['side'] == "Buy" else exit_price,
                    'sell_price': exit_price if current_position['side'] == "Buy" else entry_price,
                    'quantity': current_position['size'],
                    'pnl_percent': net_pnl_percent * 100,
                    'pnl_sum': current_pnl_sum,
                    'balance': current_balance
                }
                
                save_single_trade(exit_trade) 
                
                logging.info(f"Position closed by {action.upper()}: PnL = {net_pnl_percent*100:.2f}%, Total PnL = {current_pnl_sum:.2f}%, Balance = ${current_balance:.2f}")
                break
            
            # Log current status
            current_price = price_df['close'].iloc[-1]
            if current_position:
                if current_position['side'] == "Buy":
                    unrealized_pnl = ((current_price - current_position['entry_price']) / current_position['entry_price']) * 100
                else:
                    unrealized_pnl = ((current_position['entry_price'] - current_price) / current_position['entry_price']) * 100
                    
                logging.info(f"Current price: ${current_price}, Unrealized PnL: {unrealized_pnl:.2f}%")
            
            time.sleep(30)
            
        except Exception as e:
            logging.error(f"Error in monitoring loop: {e}")
            time.sleep(30)

    logging.info("=== Trading session completed ===")
if __name__ == "__main__":
    main()