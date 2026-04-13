import { useEffect, useState } from "react";

import { getModelsStatus } from "../api/client";
import { LoadingCard } from "./LoadingCard";

export function StatusBar() {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    getModelsStatus()
      .then((data) => {
        if (active) {
          setStatus(data);
          setLoading(false);
        }
      })
      .catch(() => {
        if (active) {
          setError("Status unavailable");
          setLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, []);

  if (loading) {
    return <LoadingCard title="Checking local model status..." />;
  }

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
