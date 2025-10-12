import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const fake = Array.from({length: 60}).map((_,i)=>({
  t: i, close: 100 + Math.sin(i/7)*2 + i*0.05
}));

export default function PriceChart() {
  return (
    <div style={{width:"100%", height:320}}>
      <ResponsiveContainer>
        <LineChart data={fake}>
          <XAxis dataKey="t" />
          <YAxis domain={["dataMin - 2", "dataMax + 2"]}/>
          <Tooltip />
          <Line type="monotone" dataKey="close" dot={false}/>
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
