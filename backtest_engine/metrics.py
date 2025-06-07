import numpy as np
import pandas as pd

def calculate_all_metrics(trades_df, equity_curve, params):
    net = trades_df["gain"].sum()
    wins=trades_df[trades_df["gain"]>0]["gain"]
    losses=trades_df[trades_df["gain"]<0]["gain"]
    pf = wins.sum()/(-losses.sum()) if not losses.empty else np.inf
    max_dd = np.max(np.maximum.accumulate(equity_curve)-equity_curve)
    # outros KPIs...
    return {"net_profit":net,"profit_factor":pf,"max_drawdown":max_dd}
