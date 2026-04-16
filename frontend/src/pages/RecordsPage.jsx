import { useReportContext } from "../state/ReportContext";

export function RecordsPage() {
  const { history, currentSessionId, setCurrentFromHistory } = useReportContext();

  return (
    <div className="stack-page">
      <section className="workspace-card section-card">
        <div className="panel-header">
          <div>
            <p className="panel-kicker">Patient Records Archive</p>
            <h3>Session History</h3>
          </div>
        </div>

        {history.length ? (
          <div className="records-table">
            <div className="records-head">
              <span>Session ID</span>
              <span>Summary</span>
              <span>Created</span>
            </div>
            {history.map((item) => (
              <button
                key={item.sessionId}
                className="records-row"
                type="button"
                onClick={() => setCurrentFromHistory(item.sessionId)}
                aria-pressed={item.sessionId === currentSessionId}
              >
                <strong>{item.sessionId}</strong>
                <p>{item.report?.patient_summary}</p>
                <span>{new Date(item.createdAt).toLocaleString()}</span>
              </button>
            ))}
          </div>
        ) : (
          <p className="muted-copy">No records captured yet in this local session.</p>
        )}
      </section>
    </div>
  );
}
