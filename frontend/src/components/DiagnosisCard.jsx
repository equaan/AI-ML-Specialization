import { useState } from "react";
import { ChevronDown, CircleX, ShieldCheck } from "lucide-react";

export function DiagnosisCard({ item, defaultOpen = false }) {
  const [open, setOpen] = useState(defaultOpen);
  const confidencePercent = Math.round((item.confidence_score || 0) * 100);

  return (
    <div className="diagnosis-card">
      <button type="button" className="diagnosis-header" onClick={() => setOpen((value) => !value)}>
        <div className="diagnosis-left">
          <div className="rank-ring">
            <span>{String(item.rank).padStart(2, "0")}</span>
          </div>
          <div>
            <h4>{item.condition}</h4>
            <p className="diagnosis-meta">
              <span className="icd-pill">{item.icd_10_code}</span>
              <span>{confidencePercent}% confidence</span>
            </p>
          </div>
        </div>
        <ChevronDown className={open ? "open" : ""} size={18} />
      </button>

      {open ? (
        <div className="diagnosis-body">
          <div className="diagnosis-detail-block">
            <h5>Supporting Findings</h5>
            <ul className="detail-list positive">
              {(item.supporting_findings || []).map((finding) => (
                <li key={finding}>
                  <ShieldCheck size={15} />
                  <span>{finding}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="diagnosis-detail-block">
            <h5>Against Findings</h5>
            <ul className="detail-list negative">
              {(item.against_findings || []).length ? (
                item.against_findings.map((finding) => (
                  <li key={finding}>
                    <CircleX size={15} />
                    <span>{finding}</span>
                  </li>
                ))
              ) : (
                <li>
                  <CircleX size={15} />
                  <span>No strong contradictory findings captured.</span>
                </li>
              )}
            </ul>
          </div>

          <p className="clinical-rationale">{item.clinical_rationale}</p>
        </div>
      ) : null}
    </div>
  );
}
