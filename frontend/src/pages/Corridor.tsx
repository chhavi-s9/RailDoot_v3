import { ArrowRight, Circle, Flag, Gauge, MapPin, PauseCircle, TrainFront, Wrench } from "lucide-react";

const stations = ["Jaipur","Gandhinagar","Dausa","Bandikui","Alwar","Rewari","Delhi"];
const trains = [
  {n:"12956", name:"Jaipur–Mumbai SF", pos:18, status:"RUNNING", delay:"On time"},
  {n:"12413", name:"Ajmer–Delhi Intercity", pos:48, status:"RUNNING", delay:"+4 min"},
  {n:"12915", name:"Ashram Express", pos:73, status:"BLOCK AHEAD", delay:"Regulated"},
];
const blocks = [
  {start:11,end:22,label:"B-204",type:"Engineering",time:"06:30–09:05"},
  {start:31,end:43,label:"B-205",type:"S&T + Engg.",time:"06:30–08:15"},
  {start:62,end:76,label:"B-208",type:"TRD",time:"14:20–17:00"},
];

export function Corridor() {
  return <div className="page">
    <section className="page-title">
      <div><span className="eyebrow">NETWORK CONTROL</span><h1>Jaipur ↔ Delhi Corridor</h1><p>Corridor-level view of maintenance blocks and running trains.</p></div>
      <div className="corridor-status"><i/> Normal operations</div>
    </section>

    <section className="corridor-summary">
      <div><span>Sections</span><strong>6</strong><small>Planning sections</small></div>
      <div><span>Stations</span><strong>41</strong><small>Network master</small></div>
      <div><span>Active blocks</span><strong>3</strong><small>Current schedule</small></div>
      <div><span>Trains tracked</span><strong>18</strong><small>Passenger + goods</small></div>
    </section>

    <section className="panel corridor-panel">
      <div className="panel-head"><div><span className="eyebrow">CORRIDOR SCHEMATIC</span><h2>Train movement and maintenance blocks</h2></div><div className="legend"><span><i className="train-dot"/> Train</span><span><i className="block-dot"/> Maintenance block</span><span><i className="conflict-dot"/> Conflict / restriction</span></div></div>
      <div className="corridor-map">
        <div className="track-line"/>
        <div className="station-row">{stations.map((s,i)=><div className="station" key={s} style={{left:`${i*16.66}%`}}><span className="station-marker"><MapPin size={14}/></span><strong>{s}</strong><small>{i === 0 ? "JPR" : i === stations.length-1 ? "DLI" : `S-${String(i).padStart(2,"0")}`}</small></div>)}</div>
        <div className="block-lane"><span className="lane-label">BLOCKS</span>{blocks.map(b=><div className="block-marker" key={b.label} style={{left:`${b.start}%`,width:`${b.end-b.start}%`}}><b>{b.label}</b><small>{b.time}</small></div>)}</div>
        <div className="train-lane">{trains.map(t=><div className="train-marker" key={t.n} style={{left:`${t.pos}%`}}><TrainFront size={18}/><div><strong>{t.n}</strong><small>{t.status}</small></div></div>)}</div>
      </div>
    </section>

    <section className="corridor-lower">
      <div className="panel"><div className="panel-head"><div><span className="eyebrow">RUNNING TRAINS</span><h2>Live movement</h2></div></div>{trains.map(t=><div className="train-row" key={t.n}><div className="train-icon"><TrainFront size={17}/></div><div><strong>{t.n} · {t.name}</strong><small>{t.status} · {t.delay}</small></div><span className={`train-state ${t.status === "BLOCK AHEAD" ? "warning":""}`}>{t.status}</span></div>)}</div>
      <div className="panel"><div className="panel-head"><div><span className="eyebrow">MAINTENANCE BLOCKS</span><h2>Scheduled on corridor</h2></div></div>{blocks.map(b=><div className="block-row" key={b.label}><div className="block-icon"><Wrench size={16}/></div><div><strong>{b.label} · {b.type}</strong><small>{b.time}</small></div><span>{b.end-b.start}% capacity</span></div>)}</div>
    </section>
  </div>;
}
