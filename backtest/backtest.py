# backtest/backtester.py
import pandas as pd

class Backtester:
    def __init__(self, ohlcv_df, signals_df, tp=0.05, sl=0.03, initial_balance=1000, fee_percent=0.0005):
        self.ohlcv = ohlcv_df.copy()
        self.signals = signals_df.copy()
        self.tp = tp
        self.sl = sl
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.fee_percent = fee_percent

    def merge_data(self):
        df = self.ohlcv.copy()
        df = df.reset_index()
        signals = self.signals.reset_index()

        df['datetime'] = pd.to_datetime(df['datetime']).dt.floor('min')
        signals['datetime'] = pd.to_datetime(signals['datetime']).dt.floor('min')

        df = df.merge(signals, how='left', on='datetime')
        df['final_signal'] = df['final_signal'].fillna(0)
        df = df.rename(columns={'final_signal': 'signal'})
        df = df.set_index('datetime')

        return df

    def run(self):
        df = self.merge_data()
        in_position = False
        position_type = None
        entry_price = 0.0
        results = []
        pnl_sum = 0.0

        for current_time, row in df.iterrows():
            signal = row['signal']
            price = row['close']

            # Entry
            if not in_position and signal in [1, -1]:
                in_position = True
                position_type = 'long' if signal == 1 else 'short'
                entry_price = price
                entry_time = current_time
                fee = self.fee_percent * self.balance
                self.balance -= fee  # Entry fee
                results.append({
                    'datetime': current_time,
                    'action': 'buy' if signal == 1 else 'sell',
                    'price': price,
                    'pnl_percent': 0.0,
                    'pnl_sum': pnl_sum,
                    'balance': self.balance
                })
                continue

            # Exit
            if in_position:
                if position_type == 'long':
                    tp_price = entry_price * (1 + self.tp)
                    sl_price = entry_price * (1 - self.sl)
                    if price >= tp_price or price <= sl_price:
                        pnl_percent = (price - entry_price) / entry_price
                        in_position = False
                else:
                    tp_price = entry_price * (1 - self.tp)
                    sl_price = entry_price * (1 + self.sl)
                    if price <= tp_price or price >= sl_price:
                        pnl_percent = (entry_price - price) / entry_price
                        in_position = False

                if not in_position:
                    fee = self.fee_percent * self.balance
                    self.balance += self.balance * pnl_percent
                    self.balance -= fee  # Exit fee
                    pnl_sum += self.balance - self.initial_balance - pnl_sum

                    results.append({
                        'datetime': current_time,
                        'action': 'tp' if pnl_percent > 0 else 'sl',
                        'price': price,
                        'pnl_percent': pnl_percent * 100,
                        'pnl_sum': pnl_sum,
                        'balance': self.balance
                    })

        return pd.DataFrame(results)
