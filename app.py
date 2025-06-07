import gradio as gr
import pandas as pd
import io, zipfile
from backtest_engine.runner import run_backtest
from supabase_client import save_backtest_result

def process_file(file, strategy_name, atr_period, atr_threshold,
                 stop_multiplier, lot_type, lot_value, capital,
                 spread, start_date, end_date):

    content = file.read()
    z = zipfile.ZipFile(io.BytesIO(content))
    fname = z.namelist()[0]
    df = pd.read_csv(z.open(fname))

    params = {
        "strategy_name": strategy_name,
        "atr_period": atr_period,
        "atr_threshold": atr_threshold,
        "atr_multiplier": stop_multiplier,
        "lot_type": lot_type,
        "lot_value": lot_value,
        "capital": capital,
        "spread": spread,
        "start_date": start_date,
        "end_date": end_date
    }

    result = run_backtest(df, params)
    save_backtest_result(params, result["metrics"], result["equity_curve_image"])
    return result["metrics"], result["equity_curve_image"]

iface = gr.Interface(
    fn=process_file,
    inputs=[
        gr.File(label="Upload ZIP com dados"),
        gr.Textbox(label="Nome da Estratégia", value="ATR Dinâmico v1"),
        gr.Number(label="Período ATR", value=20),
        gr.Number(label="Limiar ATR", value=50),
        gr.Number(label="Multiplicador Stop", value=1.5),
        gr.Radio(choices=["fixo", "percentual"], label="Tipo de Lote", value="percentual"),
        gr.Number(label="Valor do Lote", value=0.05),
        gr.Number(label="Capital Inicial", value=100),
        gr.Number(label="Spread Médio", value=1.0),
        gr.Textbox(label="Data Início (AAAA-MM-DD)", value="2025-05-01"),
        gr.Textbox(label="Data Fim (AAAA-MM-DD)", value="2025-05-07"),
    ],
    outputs=[
        gr.JSON(label="Métricas"),
        gr.Image(label="Equity Curve")
    ],
    title="MiniGain - Backtest App",
    description="Faça upload de um arquivo ZIP com dados M1 e rode o backtest completo com visualização da curva de capital."
)

if __name__ == "__main__":
    iface.launch()
