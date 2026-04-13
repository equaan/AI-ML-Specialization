import { AlertTriangle, ClipboardList, ShieldAlert } from "lucide-react";

export function ResultsPanel({ report }) {
  if (!report) {
    return (
      <section className="panel card empty-state">
        <ClipboardList size={26} />
        <h2>No Report Yet</h2>
        <p>Run an analysis from the home page to populate the result view.</p>
      </section>
    );
  }

  return (
    <section className="panel stack">
      {report.red_flags?.length ? (
        <div className="alert-banner">
          <ShieldAlert size={18} />
          <div>
            <h3>Red Flags Detected</h3>
            {report.red_flags.map((flag) => (
              <p key={flag}>{flag}</p>
            ))}
          </div>
        </div>
      ) : null}

      <article className="card">
        <h2>Clinical Summary</h2>
        <p>{report.patient_summary}</p>
      </article>

      <article className="card">
        <h2>Differential Diagnosis</h2>
        <div className="diagnosis-grid">
          {report.differential_diagnosis?.map((item) => (
            <div key={`${item.rank}-${item.condition}`} className="diagnosis-card">
              <div className="rank-pill">#{item.rank}</div>
              <h3>{item.condition}</h3>
              <p className="icd-pill">{item.icd_10_code}</p>
              <p>Confidence: {(item.confidence_score * 100).toFixed(0)}%</p>
              <p>{item.clinical_rationale}</p>
            </div>
          ))}
        </div>
      </article>

      <article className="card">
        <h2>Next Steps</h2>
        <ul className="simple-list">
          {report.recommended_next_steps?.map((step) => (
            <li key={step}>
              <AlertTriangle size={16} />
              <span>{step}</span>
            </li>
          ))}
        </ul>
      </article>
    </section>
  );
}
