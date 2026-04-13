import { FileText, Image as ImageIcon, Mic } from "lucide-react";

import { ExportBar } from "../components/ExportBar";
import { InputPanel } from "../components/InputPanel";
import { LoadingCard } from "../components/LoadingCard";
import { ResultsPanel } from "../components/ResultsPanel";
import { StatusBar } from "../components/StatusBar";
import { useReportContext } from "../state/ReportContext";

export function HomePage() {
  const { currentInputs, currentReport, currentSessionId, history, analysisLoading } = useReportContext();

  return (
    <div className="home-grid">
      <div className="left-column">
        <StatusBar />
        <InputPanel />
      </div>

      <div className="right-column">
        <section className="workspace-card preview-card">
          <div className="panel-header">
            <div>
              <p className="panel-kicker">Live Preview</p>
              <h3>Submitted Inputs</h3>
            </div>
          </div>

          <div className="preview-stack">
            <PreviewTile icon={ImageIcon} title="Image Input" value={currentInputs.imageName || "No image attached"} />
            <PreviewTile icon={FileText} title="PDF Input" value={currentInputs.pdfName || "No PDF attached"} />
            <PreviewTile
              icon={Mic}
              title="Symptom / Voice Context"
              value={currentInputs.transcript || currentInputs.symptoms || "No symptom text yet"}
              tall
            />
          </div>
        </section>

        {analysisLoading ? <LoadingCard title="Agents are assembling the clinical report..." /> : <ResultsPanel report={currentReport} compact />}
        <ExportBar sessionId={currentSessionId} />

        <section className="workspace-card recent-card">
          <div className="panel-header">
            <div>
              <p className="panel-kicker">Recent Clinical Cycles</p>
              <h3>Session Archive</h3>
            </div>
          </div>
          <div className="recent-list">
            {history.length ? (
              history.map((entry) => (
                <div key={entry.sessionId} className="recent-item">
                  <div>
                    <strong>{entry.sessionId}</strong>
                    <p>{entry.report?.patient_summary || "No summary captured"}</p>
                  </div>
                  <span>{new Date(entry.createdAt).toLocaleTimeString()}</span>
                </div>
              ))
            ) : (
              <p className="muted-copy">No previous analyses in this session yet.</p>
            )}
          </div>
        </section>
      </div>
    </div>
  );
}

function PreviewTile({ icon: Icon, title, value, tall = false }) {
  return (
    <div className={`preview-tile ${tall ? "tall" : ""}`}>
      <div className="preview-icon">
        <Icon size={16} />
      </div>
      <div>
        <strong>{title}</strong>
        <p>{value}</p>
      </div>
    </div>
  );
}
