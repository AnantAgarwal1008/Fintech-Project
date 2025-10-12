from fastapi import FastAPI
from pydantic import BaseModel
import os
import psycopg
from datetime import date

app = FastAPI(title="ML Model Service")

DB_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@" \
         f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

class PredictRequest(BaseModel):
    symbol: str
    horizon: str = "1d"
    asof_date: date | None = None

class PredictResponse(BaseModel):
    symbol: str
    horizon: str
    p_up: float
    p_down: float
    p_neu: float
    model_version: str

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    # Placeholder: a deterministic stub you will replace with real model call.
    # Optionally fetch latest features from DB here.
    p_up, p_down, p_neu = 0.40, 0.35, 0.25
    return PredictResponse(
        symbol=req.symbol, horizon=req.horizon,
        p_up=p_up, p_down=p_down, p_neu=p_neu,
        model_version="stub-0.0.1"
    )
