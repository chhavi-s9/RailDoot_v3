import { useEffect, useState } from "react";
import { AlertTriangle, BrainCircuit, CheckCircle2, ChevronRight, Clock3, ShieldAlert } from "lucide-react";
import { getConflicts, resolveConflict } from "../api";
import type { Conflict } from "../types";

const demo: Conflict[] = [
 {id:"C-104",type:"TRAIN CONFLICT",severity:"HIGH",task:"Track renewal",section:"JP-AII",detail:"Proposed maintenance window overlaps a protected passenger movement.",status:"OPEN"},
 {id:"C-101",type:"RESOURCE CONFLICT",severity:"HIGH",task:"Tower wagon allocation",section:"AII-REW",detail:"TRD and S&T requests require the same scarce tower wagon.",status:"OPEN"},
 {id:"C-099",type:"SECTION CONFLICT",severity:"MEDIUM",task:"Joint maintenance window",section:"REW-GGC",detail:"Two incompatible activities were proposed for the same section.",status:"OPEN"},
];

export function Conflicts() {
 const [items,setItems]=useState(demo);
 const [working,setWorking]=useState<string|null>(null);
 useEffect(()=>{getConflicts().then(setItems).catch(()=>{});},[]);
 const ask=async(id:string)=>{setWorking(id);try{await resolveConflict(id)}catch{}setTimeout(()=>setWorking(null),600)};
 return <div className="page">
  <section className="page-title"><div><span className="eyebrow">DECISION SUPPORT</span><h1>Conflict Management</h1><p>Review operational conflicts and ask RailDoot to find a feasible alternative.</p></div><div className="conflict-summary"><ShieldAlert size={18}/><strong>{items.filter(x=>x.status==="OPEN").length}</strong><span>open conflicts</span></div></section>
  <div className="conflict-page-grid">
   <section className="panel"><div className="panel-head"><div><span className="eyebrow">OPEN ISSUES</span><h2>Requires attention</h2></div></div>
    {items.map(c=><div className="conflict-card" key={c.id}><div className={`conflict-severity ${c.severity.toLowerCase()}`}><AlertTriangle size={18}/></div><div className="conflict-body"><div className="conflict-top"><span className={`severity-label ${c.severity.toLowerCase()}`}>{c.severity}</span><span>{c.id}</span></div><h3>{c.type}</h3><strong>{c.task} · {c.section}</strong><p>{c.detail}</p><div className="conflict-meta"><span><Clock3 size={14}/> Needs alternate window</span><span><CheckCircle2 size={14}/> Safety constraints protected</span></div></div><button className="ai-button" onClick={()=>ask(c.id)} disabled={working===c.id}>{working===c.id ? "Analyzing..." : <><BrainCircuit size={16}/> Ask AI to Resolve</>}</button></div>)}
   </section>
   <aside className="panel ai-explain"><div className="ai-icon"><BrainCircuit size={22}/></div><span className="eyebrow">HOW RESOLUTION WORKS</span><h2>AI recommendation, officer approval</h2><p>RailDoot checks feasible windows, train movements, resources and department compatibility before suggesting an alternative.</p><div className="explain-step"><b>01</b><span>Detect conflict</span></div><div className="explain-step"><b>02</b><span>Generate feasible alternatives</span></div><div className="explain-step"><b>03</b><span>Score alternatives with ML + CP-SAT</span></div><div className="explain-step"><b>04</b><span>Officer applies or rejects</span></div></aside>
  </div>
 </div>
}
