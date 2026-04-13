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

  return (
    <div className="status-strip">
      <StatusPill label="LLaMA 3.1" state={status?.llama3 ? "online" : "warning"} />
      <StatusPill label="LLaVA" state={status?.llava ? "online" : "warning"} />
      <StatusPill label="Whisper" state={status?.whisper ? "online" : "warning"} />
      <StatusPill label="ChromaDB" state={status?.chromadb ? "online" : "warning"} />
      {error ? <span className="status-pill warning">{error}</span> : null}
    </div>
  );
}

function StatusPill({ label, state }) {
  return (
    <div className={`status-pill ${state}`}>
      <span className="dot" />
      <span>{label}</span>
    </div>
  );
}
