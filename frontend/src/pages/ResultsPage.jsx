import { ExportBar } from "../components/ExportBar";
import { ResultsPanel } from "../components/ResultsPanel";
import { useReportContext } from "../state/ReportContext";

export function ResultsPage() {
  const { currentReport, currentSessionId } = useReportContext();

  return (
    <div className="stack">
      <ResultsPanel report={currentReport} />
      <ExportBar sessionId={currentSessionId} />
    </div>
  );
}
