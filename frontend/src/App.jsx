import { NavLink, Route, Routes } from "react-router-dom";
import {
  Activity,
  Database,
  FileSearch,
  FlaskConical,
  FolderArchive,
  ShieldCheck,
} from "lucide-react";

import { EvidencePage } from "./pages/EvidencePage";
import { HomePage } from "./pages/HomePage";
import { LabReportPage } from "./pages/LabReportPage";
import { RecordsPage } from "./pages/RecordsPage";
import { ResultsPage } from "./pages/ResultsPage";
import { StatusPage } from "./pages/StatusPage";
import { TracePage } from "./pages/TracePage";

const navItems = [
  { to: "/", label: "Analysis", icon: Activity },
  { to: "/results", label: "Results", icon: ShieldCheck },
  { to: "/status", label: "Status", icon: Database },
  { to: "/records", label: "Records", icon: FolderArchive },
  { to: "/trace", label: "Trace", icon: FileSearch },
  { to: "/evidence", label: "Evidence", icon: FlaskConical },
  { to: "/lab-report", label: "Lab Lens", icon: FileSearch },
];

export default function App() {
  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="sidebar-brand-mark">M</div>
          <div>
            <p className="sidebar-kicker">Precision Sentinel</p>
            <h1>MediAgent</h1>
          </div>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink key={item.to} to={item.to} className="sidebar-link">
                <Icon size={16} />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          <button className="sidebar-cta">New Analysis</button>
          <p>Clinical Node 04</p>
        </div>
      </aside>

      <div className="main-region">
        <header className="topbar">
          <div>
            <p className="eyebrow">Multimodal Clinical Intelligence</p>
            <h2>Operational Workspace</h2>
          </div>
          <div className="topbar-meta">
            <span className="status-chip online">System Ready</span>
            <span className="status-chip">Local-first stack</span>
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
          </Routes>
        </main>
      </div>
    </div>
  );
}
