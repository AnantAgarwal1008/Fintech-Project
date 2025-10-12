from prefect import flow, task
from utils.db import get_conn
import requests, os, datetime as dt

ML_URL = f"http://{os.getenv('ML_SERVICE_HOST','ml_service_py')}:{os.getenv('ML_SERVICE_PORT','8000')}/predict"

@task
def call_model(symbol: str, horizon="1d"):
    resp = requests.post(ML_URL, json={"symbol": symbol, "horizon": horizon}, timeout=15)
    resp.raise_for_status()
    return resp.json()

@task
def write_prediction(pred):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
        INSERT INTO predictions(symbol, asof_date, horizon, p_up, p_down, p_neu, model_version)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (symbol, asof_date, horizon, model_version) DO NOTHING
        """, (pred["symbol"], dt.date.today(), pred["horizon"], pred["p_up"], pred["p_down"], pred["p_neu"], pred["model_version"]))

@flow
def batch_predict_flow(symbols: list[str] = ["RELIANCE.NS","TCS.NS"], horizon="1d"):
    for s in symbols:
        pred = call_model(s, horizon)
        write_prediction(pred)

if __name__ == "__main__":
    batch_predict_flow()
