from prefect import flow, task
from utils.db import get_conn
import datetime as dt

@task
def fetch_prices(symbol: str):
    # TODO: call data provider; here mock yesterday close
    return [{"date": dt.date.today(), "open":100,"high":101,"low":99,"close":100.5,"adj_close":100.5,"volume":123456}]

@task
def upsert_prices(symbol: str, rows):
    with get_conn() as conn, conn.cursor() as cur:
        for r in rows:
            cur.execute("""
              INSERT INTO prices(symbol,date,open,high,low,close,adj_close,volume)
              VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
              ON CONFLICT (symbol,date)
              DO UPDATE SET open=EXCLUDED.open, high=EXCLUDED.high, low=EXCLUDED.low,
                close=EXCLUDED.close, adj_close=EXCLUDED.adj_close, volume=EXCLUDED.volume
            """, (symbol, r["date"], r["open"], r["high"], r["low"], r["close"], r["adj_close"], r["volume"]))
    return True

@flow
def ingest_prices_flow(symbols: list[str] = ["RELIANCE.NS","TCS.NS"]):
    for s in symbols:
        rows = fetch_prices(s)
        upsert_prices(s, rows)

if __name__ == "__main__":
    ingest_prices_flow()
