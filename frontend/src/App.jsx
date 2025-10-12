import {useEffect, useState} from "react";
import {fetchPrediction} from "./api";
import PriceChart from "./components/PriceChart";
import PredictionBadge from "./components/PredictionBadge";

export default function App() {
  const [symbol, setSymbol] = useState("RELIANCE.NS");
  const [pred, setPred] = useState(null);
  const [err, setErr] = useState("");

  useEffect(() => {
    fetchPrediction(symbol, "1d").then(setPred).catch(e => setErr(e.message));
  }, [symbol]);

  const latest = Array.isArray(pred) && pred.length ? pred[0] : null;

  return (
    <div style={{padding: 24, fontFamily: "Inter, system-ui, sans-serif"}}>
      <h2>Stock Prediction Dashboard</h2>
      <div style={{display:"flex", gap:12, alignItems:"center"}}>
        <input value={symbol} onChange={e=>setSymbol(e.target.value)} placeholder="Symbol e.g. RELIANCE.NS" />
        {latest && <PredictionBadge p={latest} />}
      </div>
      <div style={{marginTop: 20}}>
        <PriceChart symbol={symbol} />
      </div>
      {err && <p style={{color:"crimson"}}>{err}</p>}
    </div>
  );
}
