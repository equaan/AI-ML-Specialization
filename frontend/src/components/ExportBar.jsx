import { exportReport } from "../api/client";

export function ExportBar({ sessionId }) {
  if (!sessionId) return null;

  async function handleExport(format) {
    const data = await exportReport(sessionId, format);
    if (format === "pdf") {
      const url = URL.createObjectURL(data);
      window.open(url, "_blank", "noopener,noreferrer");
      return;
    }
    const blob = new Blob([data], { type: format === "json" ? "application/json" : "text/markdown" });
    const url = URL.createObjectURL(blob);
    window.open(url, "_blank", "noopener,noreferrer");
  }

  return (
    <div className="export-bar card">
      <span>Export report</span>
      <button onClick={() => handleExport("json")}>JSON</button>
      <button onClick={() => handleExport("markdown")}>Markdown</button>
      <button onClick={() => handleExport("pdf")}>PDF</button>
    </div>
  );
}
