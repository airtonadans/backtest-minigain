import numpy as np
import pandas as pd

def calculate_atr(df, period):
    high = df["high"]; low = df["low"]; close = df["close"]
    prev = close.shift(1)
    tr = pd.concat([
        high-low,
        (high-prev).abs(),
        (low-prev).abs()
    ], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def calculate_stop_atr(df, atr_series, multiplier):
    return df["low"] - atr_series*multiplier, df["high"] + atr_series*multiplier
