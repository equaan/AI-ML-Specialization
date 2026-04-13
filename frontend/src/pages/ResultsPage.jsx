import { ExportBar } from "../components/ExportBar";
import { LoadingCard } from "../components/LoadingCard";
import { ResultsPanel } from "../components/ResultsPanel";
import { useReportContext } from "../state/ReportContext";

export function ResultsPage() {
  const { currentReport, currentSessionId, analysisLoading } = useReportContext();

  return (
    <div className="stack-page">
      {analysisLoading ? <LoadingCard title="Preparing the full result view..." /> : <ResultsPanel report={currentReport} />}
      <ExportBar sessionId={currentSessionId} />
    </div>
  );
}
