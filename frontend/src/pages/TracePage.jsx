import { useReportContext } from "../state/ReportContext";
import { TraceViewer } from "../components/TraceViewer";

export function TracePage() {
  const { currentReport } = useReportContext();

  return (
    <div className="stack-page">
      <TraceViewer report={currentReport} />
    </div>
  );
}
