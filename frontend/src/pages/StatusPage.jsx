import { StatusBar } from "../components/StatusBar";
import { useReportContext } from "../state/ReportContext";

export function StatusPage() {
  const { history } = useReportContext();

  return (
    <div className="stack">
      <StatusBar />
      <section className="card panel">
        <h2>Recent Analyses</h2>
        {history.length === 0 ? (
          <p>No local session history yet.</p>
        ) : (
          <ul className="history-list">
            {history.map((entry) => (
              <li key={entry.sessionId}>
                <strong>{entry.sessionId}</strong>
                <span>{new Date(entry.createdAt).toLocaleString()}</span>
                <p>{entry.report?.patient_summary}</p>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
