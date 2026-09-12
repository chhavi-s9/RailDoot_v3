import { useEffect, useState } from "react";
import { NavLink, Route, Routes, useLocation } from "react-router-dom";
import {
  Activity, AlertTriangle, BarChart3, CalendarDays, ChevronRight, CircleHelp,
  Cpu, Gauge, LayoutDashboard, Map, Menu, Settings, TrainFront, Wrench, X
} from "lucide-react";
import { Dashboard } from "./pages/Dashboard";
import { Planner } from "./pages/Planner";
import { Corridor } from "./pages/Corridor";
import { Conflicts } from "./pages/Conflicts";
import { Requests } from "./pages/Requests";
import { Assets } from "./pages/Assets";
import { Analytics } from "./pages/Analytics";

const nav = [
  { to: "/", label: "Operations", icon: LayoutDashboard, end: true },
  { to: "/planner", label: "AI Block Planner", icon: Cpu },
  { to: "/corridor", label: "Corridor View", icon: Map },
  { to: "/conflicts", label: "Conflicts", icon: AlertTriangle },
  { to: "/requests", label: "Maintenance Requests", icon: Wrench },
  { to: "/assets", label: "Assets", icon: Gauge },
  { to: "/analytics", label: "Performance", icon: BarChart3 },
];

export default function App() {
  const [open, setOpen] = useState(true);
  const location = useLocation();

  useEffect(() => {
    if (window.innerWidth < 900) setOpen(false);
  }, [location.pathname]);

  const current = nav.find(n => n.end ? location.pathname === n.to : location.pathname.startsWith(n.to));

  return (
    <div className="app">
      <aside className={`sidebar ${open ? "open" : "closed"}`}>
        <div className="brand">
          <div className="brand-mark">R</div>
          {open && <div><div className="brand-name">RailDoot</div><div className="brand-sub">Automatic Block Planning</div></div>}
        </div>

        <div className="nav-section">{open && <span>OPERATIONS</span>}</div>
        <nav>
          {nav.map(({ to, label, icon: Icon, end }) => (
            <NavLink key={to} to={to} end={end} className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}>
              <Icon size={18} />
              {open && <span>{label}</span>}
              {open && label === "Conflicts" && <span className="nav-count">6</span>}
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <NavLink to="/settings" className="nav-item"><Settings size={18}/>{open && <span>System Settings</span>}</NavLink>
          <div className="system-state">
            <span className="state-dot" />
            {open && <div><strong>System operational</strong><small>All services connected</small></div>}
          </div>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <button className="icon-button" onClick={() => setOpen(v => !v)} aria-label="Toggle navigation">
            {open ? <X size={19}/> : <Menu size={19}/>}
          </button>
          <div className="crumb">
            <span>Centralized Block Planning</span><ChevronRight size={14}/><strong>{current?.label ?? "Operations"}</strong>
          </div>
          <div className="topbar-right">
            <div className="corridor-chip"><TrainFront size={16}/> Jaipur ↔ Delhi</div>
            <div className="officer">
              <div className="avatar">CO</div>
              <div><strong>Control Officer</strong><small>Operations</small></div>
            </div>
          </div>
        </header>

        <div className="content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/planner" element={<Planner />} />
            <Route path="/corridor" element={<Corridor />} />
            <Route path="/conflicts" element={<Conflicts />} />
            <Route path="/requests" element={<Requests />} />
            <Route path="/assets" element={<Assets />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Routes>
        </div>
      </main>
    </div>
  );
}

function SettingsPage() {
  return <div className="page"><div className="page-title"><div><span className="eyebrow">SYSTEM</span><h1>System Settings</h1><p>Backend connection, planning preferences and operational configuration.</p></div></div><div className="empty-state"><Settings size={32}/><h3>Configuration is managed by the backend</h3><p>Connect the FastAPI service on port 8000 to load live configuration.</p></div></div>;
}
