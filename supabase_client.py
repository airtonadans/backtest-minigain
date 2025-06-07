from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_backtest_result(params: dict, metrics: dict, equity_img: str):
    data = {
        "params": params,
        "metrics": metrics,
        "equity_curve": equity_img,
        "strategy_name": params.get("strategy_name", "")
    }
    supabase.table("backtests").insert(data).execute()


