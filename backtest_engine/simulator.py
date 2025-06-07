import pandas as pd
import numpy as np
from .indicators import calculate_atr, calculate_stop_atr
from .utils import to_ohlcv
from .metrics import calculate_all_metrics
from .chart import generate_equity_curve_image

class TradeSimulator:
    def __init__(self, raw_df, params):
        self.params = params
        # preparar o DF: ticks → ohlcv
        self.df = to_ohlcv(raw_df, params["start_date"], params["end_date"])
        self.trades = []
        self.capital = params["capital"]
        self.equity = [self.capital]

    def run(self):
        # calcular indicadores
        atr = calculate_atr(self.df, self.params["atr_period"])
        stop_buy, stop_sell = calculate_stop_atr(self.df, atr, self.params["atr_multiplier"])
        self.df["ATR"] = atr; self.df["StopBuy"]=stop_buy; self.df["StopSell"]=stop_sell

        in_pos=False
        for i in range(1,len(self.df)):
            row=self.df.iloc[i]; prev=self.df.iloc[i-1]
            if not in_pos and row["ATR"]>self.params["atr_threshold"]:
                if prev["close"]<prev["StopBuy"] and row["close"]>row["StopBuy"]:
                    in_pos=True; side="buy"; entry=row["close"]
                elif prev["close"]>prev["StopSell"] and row["close"]<row["StopSell"]:
                    in_pos=True; side="sell"; entry=row["close"]
                if in_pos: entry_idx=i; entry_px=entry
            elif in_pos:
                if side=="buy" and row["low"]<=row["StopSell"]:
                    exit_px=row["StopSell"]; self._record_trade(entry_idx,i,entry_px,exit_px,side); in_pos=False
                if side=="sell" and row["high"]>=row["StopBuy"]:
                    exit_px=row["StopBuy"]; self._record_trade(entry_idx,i,entry_px,exit_px,side); in_pos=False

        df_trades=pd.DataFrame(self.trades)
        metrics=calculate_all_metrics(df_trades,self.equity,self.params)
        return df_trades, metrics

    def _record_trade(self, ei, xi, ep, xp, side):
        pips = (xp-ep)/0.01 if side=="buy" else (ep-xp)/0.01
        lot = self.params["lot_value"] if self.params["lot_type"]=="fixed" else (self.capital*self.params["lot_value"]/100)/ (abs(pips)*0.01)
        gain = pips*lot*0.01
        self.capital+=gain; self.equity.append(self.capital)
        self.trades.append({"entry_index":ei,"exit_index":xi,"side":side,"pips":pips,"lot":lot,"gain":gain})
