import { useEffect, useState } from "react";
import { AlertTriangle, ArrowRight, BrainCircuit, CalendarClock, CheckCircle2, CircleAlert, Clock3, TrainFront, Wrench } from "lucide-react";
import { Link } from "react-router-dom";
import { getConflicts, getDashboard, getRequests } from "../api";
import type { Conflict, DashboardSummary, RequestItem } from "../types";

const fallback: DashboardSummary = {
  total_requests: 485, critical_requests: 24, overdue_requests: 67, active_conflicts: 6,
  planned_blocks: 18, high_risk_assets: 31, asset_availability_pct: 94.2, block_utilization_pct: 81
};

export function Dashboard() {
  const [summary, setSummary] = useState(fallback);
  const [requests, setRequests] = useState<RequestItem[]>([]);
  const [conflicts, setConflicts] = useState<Conflict[]>([]);

  useEffect(() => {
    Promise.allSettled([getDashboard(), getRequests(), getConflicts()]).then(([s, r, c]) => {
      if (s.status === "fulfilled") setSummary(s.value);
      if (r.status === "fulfilled") setRequests(r.value);
      if (c.status === "fulfilled") setConflicts(c.value);
    });
  }, []);

  const topRequests = requests.slice(0, 5);
  const openConflicts = conflicts.filter(c => c.status === "OPEN").slice(0, 4);

  return (
    <div className="page">
      <section className="page-title dashboard-title">
        <div>
          <span className="eyebrow">OPERATIONS CONTROL</span>
          <h1>Today's Operations</h1>
          <p>One operational view across Engineering, S&T, TRD and the Control Office.</p>
        </div>
        <div className="date-box"><CalendarClock size={17}/><div><strong>{new Date().toLocaleDateString("en-IN",{day:"2-digit",month:"short",year:"numeric"})}</strong><small>Planning day</small></div></div>
      </section>

      <section className="stat-grid">
        <Stat label="Maintenance requests" value={summary.total_requests} sub="Across 3 departments" icon={<Wrench/>}/>
        <Stat label="Critical requests" value={summary.critical_requests} sub="Need priority attention" icon={<CircleAlert/>} tone="orange"/>
        <Stat label="Overdue requests" value={summary.overdue_requests} sub="Past scheduled date" icon={<Clock3/>} tone="red"/>
        <Stat label="Open conflicts" value={summary.active_conflicts} sub="Require resolution" icon={<AlertTriangle/>} tone="red"/>
        <Stat label="Asset availability" value={`${summary.asset_availability_pct}%`} sub="Current network status" icon={<CheckCircle2/>} tone="green"/>
      </section>

      <section className="attention-grid">
        <div className="panel">
          <div className="panel-head">
            <div><span className="eyebrow">ATTENTION QUEUE</span><h2>Maintenance requests</h2></div>
            <Link to="/requests" className="text-link">View all <ArrowRight size={15}/></Link>
          </div>
          <div className="request-list">
            {(topRequests.length ? topRequests : [
              {req_uid:"TMS/SUR/1001",dept:"Engineering",asset_id:"TRK-041",activity_desc:"Track geometry inspection",dept_priority_code:"P1",days_overdue:4},
              {req_uid:"SMMS/SUR/2001",dept:"S&T",asset_id:"SIG-014",activity_desc:"Signalling cable rectification",dept_priority_code:"B2",days_overdue:0},
              {req_uid:"TDMS/SUR/3007",dept:"TRD",asset_id:"OHE-022",activity_desc:"OHE insulator replacement",dept_priority_code:"A",days_overdue:7},
              {req_uid:"TMS/SUR/1024",dept:"Engineering",asset_id:"TRK-117",activity_desc:"Rail renewal",dept_priority_code:"P2",days_overdue:12},
              {req_uid:"SMMS/SUR/2042",dept:"S&T",asset_id:"SIG-031",activity_desc:"Point machine maintenance",dept_priority_code:"A1",days_overdue:2}
            ] as RequestItem[]).map((r, i) => (
              <div className="request-row" key={r.req_uid}>
                <div className={`dept-dot ${String(r.dept).toLowerCase().replace("&","")}`}>{String(r.dept).slice(0,2)}</div>
                <div className="row-main"><strong>{r.activity_desc}</strong><span>{r.req_uid} · {r.asset_id}</span></div>
                <span className={`priority ${i < 2 ? "critical" : "high"}`}>{r.dept_priority_code || "HIGH"}</span>
                <div className="overdue">{Number(r.days_overdue) > 0 ? `${r.days_overdue}d overdue` : "Due window open"}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <div className="panel-head">
            <div><span className="eyebrow">CONFLICT MANAGEMENT</span><h2>Open conflicts</h2></div>
            <Link to="/conflicts" className="text-link">Resolve <ArrowRight size={15}/></Link>
          </div>
          <div className="conflict-list">
            {(openConflicts.length ? openConflicts : [
              {id:"C-104",type:"TRAIN CONFLICT",severity:"HIGH",task:"Track renewal",section:"JP-AII",detail:"Passenger movement intersects proposed block",status:"OPEN"},
              {id:"C-101",type:"RESOURCE CONFLICT",severity:"HIGH",task:"Tower wagon allocation",section:"AII-REW",detail:"TRD and S&T requests overlap resource",status:"OPEN"},
              {id:"C-099",type:"SECTION CONFLICT",severity:"MEDIUM",task:"Joint maintenance window",section:"REW-GGC",detail:"Incompatible activities proposed together",status:"OPEN"},
            ] as Conflict[]).map(c => (
              <div className="conflict-row" key={c.id}>
                <div className={`severity ${c.severity.toLowerCase()}`}><AlertTriangle size={15}/></div>
                <div className="row-main"><strong>{c.type}</strong><span>{c.task} · {c.section}</span><small>{c.detail}</small></div>
                <span className={`severity-label ${c.severity.toLowerCase()}`}>{c.severity}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="ai-strip">
        <div className="ai-icon"><BrainCircuit size={23}/></div>
        <div className="ai-copy"><span className="eyebrow">RAILDOOT OPTIMIZATION ENGINE</span><h2>Generate a coordinated block plan</h2><p>AI/ML prioritizes maintenance demand, then CP-SAT searches for a feasible schedule across trains, resources and corridor windows.</p></div>
        <Link to="/planner" className="primary-button">Open AI Block Planner <ArrowRight size={17}/></Link>
      </section>

      <section className="mini-metrics">
        <Metric label="Planned blocks" value={summary.planned_blocks} detail={`${summary.block_utilization_pct}% block capacity used`}/>
        <Metric label="High-risk assets" value={summary.high_risk_assets} detail="Priority maintenance candidates"/>
        <Metric label="Network state" value="NORMAL" detail="No system-wide restriction"/>
        <Metric label="Departments" value="3" detail="Engineering · S&T · TRD"/>
      </section>
    </div>
  );
}

function Stat({label,value,sub,icon,tone=""}:{label:string,value:string|number,sub:string,icon:React.ReactNode,tone?:string}) {
  return <div className={`stat-card ${tone}`}><div className="stat-icon">{icon}</div><div><span>{label}</span><strong>{value}</strong><small>{sub}</small></div></div>;
}
function Metric({label,value,detail}:{label:string,value:string|number,detail:string}) {
  return <div className="metric-card"><span>{label}</span><strong>{value}</strong><small>{detail}</small></div>;
}
