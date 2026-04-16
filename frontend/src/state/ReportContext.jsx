import { createContext, useContext, useEffect, useMemo, useState } from "react";

const ReportContext = createContext(null);
const STORAGE_KEY = "mediagent.report_state.v1";

function loadInitialState() {
  if (typeof window === "undefined") {
    return null;
  }

  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return null;
    }
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function ReportProvider({ children }) {
  const persisted = loadInitialState();

  const [currentSessionId, setCurrentSessionId] = useState(persisted?.currentSessionId || null);
  const [currentReport, setCurrentReport] = useState(persisted?.currentReport || null);
  const [currentLabReport, setCurrentLabReport] = useState(persisted?.currentLabReport || null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [currentInputs, setCurrentInputs] = useState(
    persisted?.currentInputs || {
      symptoms: "",
      transcript: "",
      imageName: "",
      pdfName: "",
    }
  );
  const [history, setHistory] = useState(persisted?.history || []);

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }

    const snapshot = {
      currentSessionId,
      currentReport,
      currentLabReport,
      currentInputs,
      history,
    };

    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot));
  }, [currentSessionId, currentReport, currentLabReport, currentInputs, history]);

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
      analysisLoading,
      setAnalysisLoading,
      currentInputs,
      history,
      updateAnalysis,
    }),
    [currentSessionId, currentReport, currentLabReport, analysisLoading, currentInputs, history]
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
