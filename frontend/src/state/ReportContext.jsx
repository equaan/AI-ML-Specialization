import { createContext, useContext, useMemo, useState } from "react";

const ReportContext = createContext(null);

export function ReportProvider({ children }) {
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const [currentReport, setCurrentReport] = useState(null);
  const [currentLabReport, setCurrentLabReport] = useState(null);
  const [currentInputs, setCurrentInputs] = useState({
    symptoms: "",
    transcript: "",
    imageName: "",
    pdfName: "",
  });
  const [history, setHistory] = useState([]);

  function updateAnalysis(payload) {
    const { sessionId, report, labReport, inputs } = payload;
    setCurrentSessionId(sessionId);
    setCurrentReport(report);
    setCurrentLabReport(labReport || null);
    setCurrentInputs(inputs);
    setHistory((previous) => [
      {
        sessionId,
        report,
        labReport: labReport || null,
        inputs,
        createdAt: new Date().toISOString(),
      },
      ...previous.filter((item) => item.sessionId !== sessionId).slice(0, 9),
    ]);
  }

  const value = useMemo(
    () => ({
      currentSessionId,
      currentReport,
      currentLabReport,
      currentInputs,
      history,
      updateAnalysis,
    }),
    [currentSessionId, currentReport, currentLabReport, currentInputs, history]
  );

  return <ReportContext.Provider value={value}>{children}</ReportContext.Provider>;
}

export function useReportContext() {
  const context = useContext(ReportContext);
  if (!context) {
    throw new Error("useReportContext must be used within ReportProvider");
  }
  return context;
}
