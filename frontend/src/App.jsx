import { Activity, Archive, FileSearch, FlaskConical, Home, Route as RouteIcon } from "lucide-react";
import { NavLink, Navigate, Route, Routes, useLocation, useNavigate } from "react-router-dom";

import { EvidencePage } from "./pages/EvidencePage";
import { HomePage } from "./pages/HomePage";
import { LabReportPage } from "./pages/LabReportPage";
import { RecordsPage } from "./pages/RecordsPage";
import { ResultsPage } from "./pages/ResultsPage";
import { StatusPage } from "./pages/StatusPage";
import { TracePage } from "./pages/TracePage";

const NAV_LINKS = [
  { to: "/", label: "Analysis", icon: Home },
  { to: "/results", label: "Results", icon: FileSearch },
  { to: "/evidence", label: "Evidence", icon: FlaskConical },
  { to: "/lab-report", label: "Lab Report", icon: Archive },
  { to: "/trace", label: "Trace", icon: RouteIcon },
  { to: "/status", label: "Status", icon: Activity },
  { to: "/records", label: "Records", icon: Archive },
];

const PAGE_TITLES = {
  "/": "New Clinical Analysis",
  "/results": "Clinical Results",
  "/evidence": "Knowledge Context",
  "/lab-report": "Lab Data Lens",
  "/trace": "Agent Trace",
  "/status": "System Status",
  "/records": "Session Records",
};

function AppShell() {
  const location = useLocation();
  const navigate = useNavigate();
  const title = PAGE_TITLES[location.pathname] || "MediAgent";

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="sidebar-brand-mark">M</div>
          <div>
            <p className="sidebar-kicker">MediAgent</p>
            <h1>Clinical Workspace</h1>
          </div>
        </div>

        <nav className="sidebar-nav">
          {NAV_LINKS.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              end={to === "/"}
              className={({ isActive }) => `sidebar-link${isActive ? " active" : ""}`}
            >
              <Icon size={15} />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          <button className="sidebar-cta" type="button" onClick={() => navigate("/")}>New Analysis</button>
          <p>Local runtime mode</p>
        </div>
      </aside>

      <div className="main-region">
        <header className="topbar">
          <div>
            <p className="eyebrow">MediAgent</p>
            <h2>{title}</h2>
          </div>
          <div className="topbar-meta">
            <span className="status-chip">Frontend: Online</span>
            <span className="status-chip online">Interactive Mode</span>
          </div>
        </header>

        <main className="page-shell">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/results" element={<ResultsPage />} />
            <Route path="/status" element={<StatusPage />} />
            <Route path="/records" element={<RecordsPage />} />
            <Route path="/trace" element={<TracePage />} />
            <Route path="/evidence" element={<EvidencePage />} />
            <Route path="/lab-report" element={<LabReportPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return <AppShell />;
}
