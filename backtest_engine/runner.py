from .indicators import calculate_atr, calculate_stop_atr
from .simulator import TradeSimulator

def run_backtest(raw_df, params):
    # Pré-processar - converter ticks para OHLCV aqui se necessário
    # raw_df já deve ter timestamp and bid columns
    sim = TradeSimulator(raw_df, params)
    trades_df, metrics = sim.run()
    # gerar equity image
    equity_img = sim.generate_equity_image()  # dentro de TradeSimulator
    return {"metrics": metrics, "equity_curve_image": equity_img}
