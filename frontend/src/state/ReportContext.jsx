import { createContext, useContext, useEffect, useMemo, useState } from "react";

import { getRecentReports } from "../api/client";

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

function defaultInputs() {
  return {
    symptoms: "",
    transcript: "",
    imageName: "",
    pdfName: "",
  };
}

function normalizeHistoryItem(item) {
  return {
    sessionId: item.sessionId || item.session_id,
    report: item.report || null,
    labReport: item.labReport || item.lab_report || null,
    inputs: item.inputs || defaultInputs(),
    createdAt: item.createdAt || item.created_at || new Date().toISOString(),
  };
}

function mergeHistory(primary, secondary) {
  const map = new Map();
  [...primary, ...secondary].forEach((entry) => {
    const normalized = normalizeHistoryItem(entry);
    if (normalized.sessionId) {
      map.set(normalized.sessionId, normalized);
    }
  });
  return Array.from(map.values())
    .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
    .slice(0, 25);
}

export function ReportProvider({ children }) {
  const persisted = loadInitialState();

  const [currentSessionId, setCurrentSessionId] = useState(persisted?.currentSessionId || null);
  const [currentReport, setCurrentReport] = useState(persisted?.currentReport || null);
  const [currentLabReport, setCurrentLabReport] = useState(persisted?.currentLabReport || null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [currentInputs, setCurrentInputs] = useState(
    persisted?.currentInputs || defaultInputs()
  );
  const [history, setHistory] = useState(persisted?.history || []);

  useEffect(() => {
    let active = true;

    async function hydrateFromBackend() {
      try {
        const serverItems = await getRecentReports(25);
        if (!active || !serverItems.length) {
          return;
        }

        const normalizedServer = serverItems.map(normalizeHistoryItem);
        setHistory((prev) => mergeHistory(normalizedServer, prev));

        if (!currentSessionId) {
          const latest = normalizedServer[0];
          if (latest) {
            setCurrentSessionId(latest.sessionId);
            setCurrentReport(latest.report || null);
            setCurrentLabReport(latest.labReport || null);
            setCurrentInputs(latest.inputs || defaultInputs());
          }
        }
      } catch {
        // Non-blocking: app still works with local state if backend history fetch fails.
      }
    }

    hydrateFromBackend();
    return () => {
      active = false;
    };
  }, [currentSessionId]);

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
    const { sessionId, report, labReport, inputs, createdAt } = payload;
    const nowIso = createdAt || new Date().toISOString();
    setCurrentSessionId(sessionId);
    setCurrentReport(report);
    setCurrentLabReport(labReport || null);
    setCurrentInputs(inputs);
    setHistory((previous) =>
      mergeHistory(
        [
          {
            sessionId,
            report,
            labReport: labReport || null,
            inputs,
            createdAt: nowIso,
          },
        ],
        previous
      )
    );
  }

  function setCurrentFromHistory(sessionId) {
    const selected = history.find((item) => item.sessionId === sessionId);
    if (!selected) {
      return;
    }
    setCurrentSessionId(selected.sessionId);
    setCurrentReport(selected.report || null);
    setCurrentLabReport(selected.labReport || null);
    setCurrentInputs(selected.inputs || defaultInputs());
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
      setCurrentFromHistory,
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
