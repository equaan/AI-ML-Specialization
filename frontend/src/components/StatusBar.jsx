import { useEffect, useState } from "react";

import { getModelsStatus } from "../api/client";

export function StatusBar() {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    getModelsStatus()
      .then((data) => {
        if (active) setStatus(data);
      })
      .catch(() => {
        if (active) setError("Status unavailable");
      });

    return () => {
      active = false;
    };
  }, []);

  if (error) {
    return <div className="status-strip card">{error}</div>;
  }

  return (
    <div className="status-strip card">
      <StatusItem label="LLaMA 3.1" active={Boolean(status?.llama3)} />
      <StatusItem label="LLaVA" active={Boolean(status?.llava)} />
      <StatusItem label="Whisper" active={Boolean(status?.whisper)} />
      <StatusItem label="ChromaDB" active={Boolean(status?.chromadb)} />
    </div>
  );
}

function StatusItem({ label, active }) {
  return (
    <div className={`status-item ${active ? "active" : "inactive"}`}>
      <span className="status-dot" />
      <span>{label}</span>
    </div>
  );
}
