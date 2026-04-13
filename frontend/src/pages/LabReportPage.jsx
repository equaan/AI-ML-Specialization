import { useReportContext } from "../state/ReportContext";

export function LabReportPage() {
  const { currentLabReport } = useReportContext();

  return (
    <div className="lab-layout">
      <section className="workspace-card section-card">
        <div className="panel-header">
          <div>
            <p className="panel-kicker">Lab Data Lens</p>
            <h3>Parsed Lab Report</h3>
          </div>
        </div>

        {currentLabReport ? (
          <>
            <div className="lab-summary-grid">
              <div className="lab-summary-card">
                <span>Report Type</span>
                <strong>{currentLabReport.report_type}</strong>
              </div>
              <div className="lab-summary-card">
                <span>Patient Name</span>
                <strong>{currentLabReport.patient_info?.name || "Unknown"}</strong>
              </div>
              <div className="lab-summary-card">
                <span>Date</span>
                <strong>{currentLabReport.patient_info?.date || "Unknown"}</strong>
              </div>
            </div>

            <div className="lab-table">
              <div className="lab-head">
                <span>Analyte</span>
                <span>Value</span>
                <span>Reference Range</span>
                <span>Flag</span>
              </div>
              {(currentLabReport.test_results || []).map((result) => (
                <div key={`${result.test_name}-${result.value}`} className="lab-row">
                  <strong>{result.test_name}</strong>
                  <span>{result.value}</span>
                  <span>{result.reference_range || "N/A"}</span>
                  <span className={`lab-flag ${String(result.flag || "normal").toLowerCase()}`}>{result.flag || "NORMAL"}</span>
                </div>
              ))}
            </div>
          </>
        ) : (
          <p className="muted-copy">Upload a lab-report PDF during analysis to populate this page.</p>
        )}
      </section>
    </div>
  );
}
