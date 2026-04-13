import { NavLink, Route, Routes } from "react-router-dom";

import { HomePage } from "./pages/HomePage";
import { ResultsPage } from "./pages/ResultsPage";
import { StatusPage } from "./pages/StatusPage";

export default function App() {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Multimodal Clinical Intelligence</p>
          <h1>MediAgent</h1>
        </div>
        <nav className="nav">
          <NavLink to="/">Home</NavLink>
          <NavLink to="/results">Results</NavLink>
          <NavLink to="/status">Status</NavLink>
        </nav>
      </header>

      <main className="page-shell">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/results" element={<ResultsPage />} />
          <Route path="/status" element={<StatusPage />} />
        </Routes>
      </main>
    </div>
  );
}
