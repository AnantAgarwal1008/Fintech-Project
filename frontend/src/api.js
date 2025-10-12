const BASE = import.meta.env.VITE_API_BASE || "http://localhost:8080";
export async function fetchPrediction(symbol, horizon="1d") {
  const url = `${BASE}/predictions?symbol=${encodeURIComponent(symbol)}&horizon=${horizon}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("API error");
  return res.json();
}
