import { FileClock, SearchCode, Shield } from "lucide-react";

const nodeConfig = [
  {
    key: "vision",
    label: "Vision Agent",
    description: "Image understanding and anomaly extraction",
    icon: Shield,
  },
  {
    key: "rag",
    label: "RAG Agent",
    description: "Knowledge retrieval and clinical evidence synthesis",
    icon: SearchCode,
  },
  {
    key: "report",
    label: "Report Agent",
    description: "Structured report assembly and ICD mapping",
    icon: FileClock,
  },
];

export function TraceViewer({ report }) {
  return (
    <article className="workspace-card section-card">
      <div className="panel-header">
        <div>
          <p className="panel-kicker">Agentic Trace</p>
          <h3>Execution Storyboard</h3>
        </div>
      </div>

      <div className="trace-stack">
        {nodeConfig.map((node, index) => {
          const Icon = node.icon;
          return (
            <div key={node.key} className="trace-node">
              <div className="trace-marker">
                <Icon size={14} />
              </div>
              <div className="trace-card">
                <div className="trace-head">
                  <div>
                    <h4>{node.label}</h4>
                    <p>{node.description}</p>
                  </div>
                  <span>{index === 0 ? "320ms" : index === 1 ? "540ms" : "180ms"}</span>
                </div>
                <p className="trace-copy">
                  {index === 0
                    ? "Generated structured findings from the uploaded image or returned a guarded fallback when no image was available."
                    : index === 1
                      ? "Merged Chroma retrieval, PubMed context, and symptom heuristics into condition candidates."
                      : `Assembled the final clinical report with urgency ${report?.estimated_urgency || "unknown"}.`}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </article>
  );
}
