
def map_to_pandas_freq(interval):
    # Handle minute-based intervals
    if interval.endswith("m"):
        return interval.replace("m", "min")
    
    # Handle hour, day, week — just uppercase them
    elif interval.endswith(("h", "d", "w")):
        return interval.upper()

    # Optionally: support seconds too
    elif interval.endswith("s"):
        return interval.replace("s", "S")

    else:
        raise ValueError(f"Interval '{interval}' is not a valid pandas frequency.")
