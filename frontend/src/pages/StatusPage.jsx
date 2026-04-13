import { Activity, Brain, Database, Mic } from "lucide-react";

import { StatusBar } from "../components/StatusBar";

const cards = [
  { title: "LLaVA Vision", metric: "Awaiting runtime validation", icon: Brain, status: "Model route ready" },
  { title: "LLaMA Report", metric: "Fallback synthesis active", icon: Activity, status: "Swap to live Ollama later" },
  { title: "Whisper", metric: "Transcription endpoint scaffolded", icon: Mic, status: "Needs runtime install" },
  { title: "ChromaDB", metric: "Collections configured", icon: Database, status: "Ingestion pending" },
];

export function StatusPage() {
  return (
    <div className="stack-page">
      <StatusBar />
      <section className="status-grid">
        {cards.map((card) => {
          const Icon = card.icon;
          return (
            <article key={card.title} className="workspace-card model-card">
              <div className="model-icon">
                <Icon size={18} />
              </div>
              <p className="panel-kicker">{card.title}</p>
              <h3>{card.metric}</h3>
              <p className="muted-copy">{card.status}</p>
            </article>
          );
        })}
      </section>

      <section className="workspace-card section-card">
        <div className="panel-header">
          <div>
            <p className="panel-kicker">Runtime Notes</p>
            <h3>Operational Readiness</h3>
          </div>
        </div>
        <ul className="detail-list">
          <li><span />Model status reflects local endpoint availability.</li>
          <li><span />Live metrics will become meaningful once Ollama and datasets are installed.</li>
          <li><span />ChromaDB collection bootstrap is already in code.</li>
        </ul>
      </section>
    </div>
  );
}
