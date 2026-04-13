import { ExportBar } from "../components/ExportBar";
import { InputPanel } from "../components/InputPanel";
import { ResultsPanel } from "../components/ResultsPanel";
import { StatusBar } from "../components/StatusBar";
import { useReportContext } from "../state/ReportContext";

export function HomePage() {
  const { currentReport, currentSessionId } = useReportContext();

  return (
    <div className="two-column-layout">
      <div className="stack">
        <StatusBar />
        <InputPanel />
      </div>
      <div className="stack">
        <ResultsPanel report={currentReport} />
        <ExportBar sessionId={currentSessionId} />
      </div>
    </div>
  );
}
