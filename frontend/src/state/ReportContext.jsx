import { createContext, useContext, useState } from "react";

const ReportContext = createContext(null);

export function ReportProvider({ children }) {
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const [currentReport, setCurrentReport] = useState(null);
  const [history, setHistory] = useState([]);

  function updateReport(sessionId, report) {
    setCurrentSessionId(sessionId);
    setCurrentReport(report);
    setHistory((previous) => [
      {
        sessionId,
        report,
        createdAt: new Date().toISOString(),
      },
      ...previous.slice(0, 4),
    ]);
  }

  return (
    <ReportContext.Provider
      value={{
        currentSessionId,
        currentReport,
        history,
        updateReport,
      }}
    >
      {children}
    </ReportContext.Provider>
  );
}

export function useReportContext() {
  const context = useContext(ReportContext);
  if (!context) {
    throw new Error("useReportContext must be used within ReportProvider");
  }
  return context;
}
