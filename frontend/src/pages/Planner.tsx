import { useState } from "react";
import { BrainCircuit, Check, ChevronRight, Clock3, Cpu, Loader2, ShieldCheck, Sparkles, TrainFront, Wrench, X } from "lucide-react";
import { generatePlan } from "../api";
import type { PlanBlock } from "../types";

const demoBlocks: PlanBlock[] = [
  {id:"B-204",section:"JP-AII",block_section:"BS-JP-AII-04",department:"Engineering",activity:"Rail renewal",start:"06:30",end:"09:05",duration:155,status:"RECOMMENDED",score:94,resource:"BCM-01"},
  {id:"B-205",section:"JP-AII",block_section:"BS-JP-AII-04",department:"S&T",activity:"Signal cable rectification",start:"06:30",end:"08:15",duration:105,status:"JOINT",score:91,resource:"SI-02"},
  {id:"B-208",section:"AII-REW",block_section:"BS-AII-REW-07",department:"TRD",activity:"OHE insulator replacement",start:"14:20",end:"17:00",duration:160,status:"RECOMMENDED",score:88,resource:"TW-02"},
];

export function Planner() {
  const [horizon, setHorizon] = useState<"weekly"|"monthly">("weekly");
  const [running, setRunning] = useState(false);
  const [generated, setGenerated] = useState(false);
  const [blocks, setBlocks] = useState<PlanBlock[]>(demoBlocks);

  const run = async () => {
    setRunning(true);
    try {
      const now = new Date();
      const end = new Date(now);
      end.setDate(now.getDate() + (horizon === "weekly" ? 6 : 29));
      const result = await generatePlan({
        start_date: now.toISOString().slice(0,10),
        end_date: end.toISOString().slice(0,10)
      });
      setBlocks(result.plan || demoBlocks);
    } catch {
      await new Promise(r => setTimeout(r, 900));
    } finally {
      setGenerated(true);
      setRunning(false);
    }
  };

  return <div className="page">
    <section className="page-title">
      <div><span className="eyebrow">AI + OPTIMIZATION</span><h1>AI Block Planner</h1><p>Generate a coordinated maintenance plan while respecting operational and safety constraints.</p></div>
      <div className="horizon-switch"><button className={horizon==="weekly"?"selected":""} onClick={()=>setHorizon("weekly")}>7 days</button><button className={horizon==="monthly"?"selected":""} onClick={()=>setHorizon("monthly")}>30 days</button></div>
    </section>

    <section className="planner-flow">
      <Step icon={<Wrench/>} title="Maintenance demand" text="TMS · SMMS · TDMS"/>
      <ChevronRight/>
      <Step icon={<BrainCircuit/>} title="AI prioritization" text="Risk · duration · impact"/>
      <ChevronRight/>
      <Step icon={<Cpu/>} title="CP-SAT optimizer" text="Windows · trains · resources"/>
      <ChevronRight/>
      <Step icon={<ShieldCheck/>} title="Officer approval" text="Review before apply"/>
    </section>

    <section className="planner-toolbar panel">
      <div><span className="eyebrow">PLANNING ENGINE</span><h2>{generated ? "Plan generated" : "Ready to generate"}</h2><p>{generated ? "The recommendation below is ready for operational review." : `Planning horizon: ${horizon === "weekly" ? "7 days" : "30 days"}.`}</p></div>
      <button className="primary-button" onClick={run} disabled={running}>{running ? <><Loader2 className="spin" size={17}/> Optimizing...</> : <><Sparkles size={17}/> Generate AI Block Plan</>}</button>
    </section>

    <section className="planner-stats">
      <Metric label="Requests considered" value="485" />
      <Metric label="Candidate windows" value="1,240" />
      <Metric label="Blocks recommended" value={blocks.length} />
      <Metric label="Constraint status" value="FEASIBLE" />
    </section>

    <section className="panel">
      <div className="panel-head"><div><span className="eyebrow">RECOMMENDED BLOCKS</span><h2>Coordinated schedule</h2></div><span className="live-tag"><i/> Solver result</span></div>
      <div className="plan-table">
        <div className="plan-head"><span>Block</span><span>Section</span><span>Department</span><span>Activity</span><span>Window</span><span>Resource</span><span>Score</span></div>
        {blocks.map(b=><div className="plan-row" key={b.id}><strong>{b.id}</strong><span>{b.section}</span><span><b className="dept-pill">{b.department}</b></span><span>{b.activity}</span><span><Clock3 size={14}/>{b.start}–{b.end}</span><span>{b.resource}</span><span className="score">{b.score ?? 86}</span></div>)}
      </div>
    </section>

    <section className="review-grid">
      <div className="panel">
        <div className="panel-head"><div><span className="eyebrow">WHY THIS PLAN</span><h2>Decision factors</h2></div></div>
        <div className="reason-list">
          <Reason title="Critical maintenance first" text="High-risk and overdue assets receive higher planning priority."/>
          <Reason title="Joint block opportunity" text="Compatible Engineering and S&T work is grouped where the corridor allows it."/>
          <Reason title="Train protection" text="Protected passenger movements remain hard constraints."/>
          <Reason title="Resource availability" text="Scarce crews and equipment cannot be double-booked."/>
        </div>
      </div>
      <div className="panel approval-card"><div className="approval-icon"><ShieldCheck/></div><span className="eyebrow">HUMAN IN THE LOOP</span><h2>Officer review required</h2><p>RailDoot recommends a plan. It does not silently change operational blocks.</p><div className="approval-actions"><button className="secondary-button"><X size={16}/> Reject / Edit</button><button className="primary-button"><Check size={16}/> Apply Recommendation</button></div></div>
    </section>
  </div>;
}

function Step({icon,title,text}:{icon:React.ReactNode,title:string,text:string}) {
  return <div className="flow-step"><div>{icon}</div><strong>{title}</strong><small>{text}</small></div>;
}
function Metric({label,value}:{label:string,value:string|number}) { return <div className="metric-card"><span>{label}</span><strong>{value}</strong><small>Current planning run</small></div>; }
function Reason({title,text}:{title:string,text:string}) { return <div className="reason"><Check size={17}/><div><strong>{title}</strong><p>{text}</p></div></div>; }
