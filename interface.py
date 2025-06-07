import gradio as gr
import os

from supabase_client import save_backtest_result
from app import run_bt

def run_interface(file, strategy_name, atr_period, atr_threshold,
                  stop_multiplier, lot_type, lot_value, capital,
                  spread, start_date, end_date):
    res = run_bt(
        file, strategy_name, atr_period, atr_threshold,
        stop_multiplier, lot_type, lot_value, capital,
        spread, start_date, end_date
    )
    metrics = res["metrics"]
    img = res["equity_curve_image"]
    return metrics, img

with gr.Blocks() as demo:
    gr.Markdown("## ATR Dinâmico v1 – Backtest App")
    with gr.Row():
        file = gr.File(label="Upload .zip de ticks")
        strategy_name = gr.Textbox(value="ATR Dinâmico v1", label="Nome da Estratégia")
    with gr.Row():
        atr_period = gr.Number(value=20, label="Período ATR")
        atr_threshold = gr.Number(value=50, label="Filtro ATR >")
        stop_multiplier = gr.Number(value=1.5, label="Multiplicador ATR")
    with gr.Row():
        lot_type = gr.Radio(["fixed","percent"], value="percent", label="Tipo de Lote")
        lot_value = gr.Number(value=5, label="Lote (% ou fixo)")
    with gr.Row():
        capital = gr.Number(value=100, label="Capital Inicial")
        spread = gr.Number(value=1.0, label="Spread (pips)")
    with gr.Row():
        start_date = gr.Textbox(value="2025-05-01", label="Data Início (YYYY-MM-DD)")
        end_date = gr.Textbox(value="2025-05-07", label="Data Fim (YYYY-MM-DD)")
    run_btn = gr.Button("Rodar Backtest")
    metrics_out = gr.JSON(label="Métricas")
    eq_img = gr.Image(label="Equity Curve")
    run_btn.click(fn=run_interface, inputs=[
        file, strategy_name, atr_period, atr_threshold,
        stop_multiplier, lot_type, lot_value, capital,
        spread, start_date, end_date
    ], outputs=[metrics_out, eq_img])
    # Botão de solicitar melhorias
    msg = gr.Textbox(placeholder="Sugestões de melhorias...", label="📩 Feedback")
    feedback_btn = gr.Button("Enviar Feedback")
    feedback_btn.click(lambda text: gr.update(value="Obrigado! Recebido"), inputs=[msg], outputs=[msg])

demo.launch()
