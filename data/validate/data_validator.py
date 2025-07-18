import pandas as pd
from data.utils.interval_mapper import map_to_pandas_freq

class DataValidator:


    def __init__(self, df, interval):
        self.df = df.copy()
        self.interval = interval

    def clean(self):
        print("Cleaning and validating data...")

        # Remove duplicate timestamps
        self.df = self.df[~self.df.index.duplicated(keep="first")]

        # Convert Binance interval to Pandas frequency string

        freq = map_to_pandas_freq(self.interval)
        if not freq:
            raise ValueError(f"Interval '{self.interval}' not supported for cleaning.")
        
        # Generate a complete time index from start to end
        full_index = pd.date_range(start=self.df.index[0], end=self.df.index[-1], freq=freq)

        # Reindex the DataFrame with the full time range (adds NaNs for missing)
        self.df = self.df.reindex(full_index)

        # Interpolate numeric columns linearly to fill missing values
        self.df[["open", "high", "low", "close", "volume"]] = self.df[["open", "high", "low", "close", "volume"]].interpolate(method="linear")

        # Missing (should be 0 if interpolation worked)
        missing_count = self.df.isnull().sum().sum()
        print(f"Interpolation completed. Remaining missing values: {missing_count}")

        return self.df
