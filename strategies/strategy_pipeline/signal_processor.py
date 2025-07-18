import pandas as pd
import numpy as np
from collections import Counter

class SignalProcessor:
    def process_signals(self, df_signals, strategy_name):
        # Ensure datetime is a column
        if df_signals.index.name == 'datetime':
            df_signals = df_signals.reset_index()

        # Identify signal columns (those starting with 'signal_')
        signal_cols = [col for col in df_signals.columns if col.startswith('signal_')]
        if not signal_cols:
            print(f"No signal columns found in {strategy_name}. Returning empty DataFrame.")
            return pd.DataFrame(columns=['datetime', 'final_signal'])

        # Select only the signal columns and datetime
        signal_df = df_signals[['datetime'] + signal_cols].copy()

        # Drop rows with any NaN in signal columns
        signal_df = signal_df.dropna()

        if signal_df.empty:
            print(f"No valid signal data for {strategy_name}. Returning empty DataFrame.")
            return pd.DataFrame(columns=['datetime', 'final_signal'])

        # Voting mechanism: Use mode across signal columns with tie handling
        final_signals = []
        for _, row in signal_df.iterrows():
            votes = [row[col] for col in signal_cols]
            count = Counter(votes)
            most_common = count.most_common()
            if len(most_common) > 1 and most_common[0][1] == most_common[1][1]:
                final_signals.append(0)  # Tie fallback
            else:
                final_signals.append(most_common[0][0])

        final_signals = pd.Series(final_signals, index=signal_df.index)

        # Create output DataFrame with datetime and final_signal
        strategy_signals = pd.DataFrame({
            'datetime': signal_df['datetime'],
            'final_signal': final_signals
        }).set_index('datetime')

        print(f"Processed signals for {strategy_name}. Shape: {strategy_signals.shape}")
        return strategy_signals