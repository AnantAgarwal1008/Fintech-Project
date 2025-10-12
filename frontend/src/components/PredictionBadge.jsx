export default function PredictionBadge({p}) {
  const conf = (p.p_up * 100).toFixed(1);
  return (
    <div style={{padding:"6px 10px", border:"1px solid #ddd", borderRadius:8}}>
      <b>{p.symbol}</b> {p.horizon} —
      &nbsp;P(up): <b>{conf}%</b> · model: {p.model_version}
    </div>
  );
}
