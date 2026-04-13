import { AlertTriangle, ArrowRight, ClipboardList } from "lucide-react";

import { DiagnosisCard } from "./DiagnosisCard";
import { RedFlagBanner } from "./RedFlagBanner";
import { SourceChip } from "./SourceChip";
import { TraceViewer } from "./TraceViewer";

export function ResultsPanel({ report, compact = false }) {
  if (!report) {
    return (
      <section className="workspace-card empty-state">
        <ClipboardList size={28} />
        <h3>No Clinical Report Yet</h3>
        <p>Run an analysis from the workspace to render the report, evidence, and agent trace.</p>
      </section>
    );
  }

  return (
    <section className="results-stack">
      <RedFlagBanner redFlags={report.red_flags || []} />

      <article className="workspace-card section-card">
        <div className="panel-header">
          <div>
            <p className="panel-kicker">Clinical Summary</p>
            <h3>Topline Interpretation</h3>
          </div>
          <span className={`urgency-chip ${report.estimated_urgency || "semi_urgent"}`}>
            {(report.estimated_urgency || "semi_urgent").replace("_", " ")}
          </span>
        </div>
        <p className="summary-copy">{report.patient_summary}</p>
      </article>

      <article className="workspace-card section-card">
        <div className="panel-header">
          <div>
            <p className="panel-kicker">Differential Diagnosis</p>
            <h3>Ranked Conditions</h3>
          </div>
        </div>
        <div className="diagnosis-list">
          {(report.differential_diagnosis || []).map((item, index) => (
            <DiagnosisCard key={`${item.rank}-${item.condition}`} item={item} defaultOpen={index === 0} />
          ))}
        </div>
      </article>

      {!compact ? (
        <div className="results-two-up">
          <article className="workspace-card section-card">
            <div className="panel-header">
              <div>
                <p className="panel-kicker">Recommended Actions</p>
                <h3>Next Steps</h3>
              </div>
            </div>
            <div className="action-list">
              {(report.recommended_next_steps || []).map((step) => (
                <div key={step} className="action-card">
                  <span className="action-badge">Action</span>
                  <p>{step}</p>
                  <ArrowRight size={16} />
                </div>
              ))}
            </div>
          </article>

          <article className="workspace-card section-card">
            <div className="panel-header">
              <div>
                <p className="panel-kicker">Additional History</p>
                <h3>Improve Accuracy</h3>
              </div>
            </div>
            <ul className="detail-list">
              {(report.additional_history_needed || []).map((item) => (
                <li key={item}>
                  <AlertTriangle size={15} />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </article>
        </div>
      ) : null}

      <article className="workspace-card section-card">
        <div className="panel-header">
          <div>
            <p className="panel-kicker">Evidence</p>
            <h3>Supporting Medical Sources</h3>
          </div>
        </div>
        <div className="source-grid">
          {(report.sources || []).length ? (
            report.sources.map((source, index) => <SourceChip key={`${source.title}-${index}`} source={source} />)
          ) : (
            <p className="muted-copy">No structured sources returned yet.</p>
          )}
        </div>
      </article>

      <TraceViewer report={report} />
    </section>
  );
}
