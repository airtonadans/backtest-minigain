import io, zipfile, base64
import pandas as pd
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from backtest_engine.runner import run_backtest
from supabase_client import save_backtest_result

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

@app.post("/run_backtest")
async def run_bt(
    file: UploadFile,
    strategy_name: str = Form(...),
    atr_period: int = Form(...),
    atr_threshold: float = Form(...),
    stop_multiplier: float = Form(...),
    lot_type: str = Form(...),
    lot_value: float = Form(...),
    capital: float = Form(...),
    spread: float = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...)
):
    # 1. ler zip
    content = await file.read()
    z = zipfile.ZipFile(io.BytesIO(content))
    fname = z.namelist()[0]
    df = pd.read_csv(z.open(fname))
    # 2. rodar backtest
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
    # 3. salvar
    save_backtest_result(params, result["metrics"], result["equity_curve_image"])
    return result
