from supabase import create_client
import os

# Variáveis protegidas via .env ou Hugging Face Secrets
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_backtest_result(params, metrics, image_base64):
    data = {
        "strategy_name": params["strategy_name"],
        "atr_period": params["atr_period"],
        "atr_threshold": params["atr_threshold"],
        "atr_multiplier": params["atr_multiplier"],
        "lot_type": params["lot_type"],
        "lot_value": params["lot_value"],
        "capital": params["capital"],
        "spread": params["spread"],
        "start_date": params["start_date"],
        "end_date": params["end_date"],
        "metrics": metrics,
        "equity_curve_image": image_base64
    }
    supabase.table("backtest_results").insert(data).execute()
