import { Download, FileCode2, FileText, FileType2 } from "lucide-react";

import { exportReport } from "../api/client";

export function ExportBar({ sessionId }) {
  if (!sessionId) return null;

  async function handleExport(format) {
    const blob = await exportReport(sessionId, format);
    const url = URL.createObjectURL(blob);
    window.open(url, "_blank", "noopener,noreferrer");
    setTimeout(() => URL.revokeObjectURL(url), 30000);
  }

  return (
    <div className="export-bar">
      <span className="export-label">Export Report</span>
      <button onClick={() => handleExport("pdf")}>
        <FileType2 size={15} />
        PDF
      </button>
      <button onClick={() => handleExport("markdown")}>
        <FileText size={15} />
        Markdown
      </button>
      <button onClick={() => handleExport("json")}>
        <FileCode2 size={15} />
        JSON
      </button>
      <div className="export-hint">
        <Download size={15} />
        Stored in-memory for the current session
      </div>
    </div>
  );
}
