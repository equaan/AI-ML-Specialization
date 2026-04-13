import { useState } from "react";

import { SourceChip } from "../components/SourceChip";
import { useReportContext } from "../state/ReportContext";

export function EvidencePage() {
  const { currentReport } = useReportContext();
  const sources = currentReport?.sources || [];
  const [activeIndex, setActiveIndex] = useState(0);
  const activeSource = sources[activeIndex];

  return (
    <div className="evidence-layout">
      <section className="workspace-card evidence-sidebar">
        <div className="panel-header">
          <div>
            <p className="panel-kicker">RAG Context Engine</p>
            <h3>Retrieved Fragments</h3>
          </div>
        </div>

        <div className="evidence-source-list">
          {sources.length ? (
            sources.map((source, index) => (
              <SourceChip
                key={`${source.title}-${index}`}
                source={source}
                active={activeIndex === index}
                onClick={() => setActiveIndex(index)}
              />
            ))
          ) : (
            <p className="muted-copy">No evidence sources available yet.</p>
          )}
        </div>
      </section>

      <section className="workspace-card evidence-main">
        <div className="panel-header">
          <div>
            <p className="panel-kicker">Knowledge Context</p>
            <h3>{activeSource?.title || "Select a source"}</h3>
          </div>
        </div>

        {activeSource ? (
          <div className="evidence-detail">
            <p className="source-meta">{activeSource.pmid ? `PMID: ${activeSource.pmid}` : "Local source"}</p>
            <p>
              This panel is now wired to the backend source list. Once live PubMed retrieval is running on the stronger
              machine, this view will show much richer evidence summaries and direct links.
            </p>
            {activeSource.url ? (
              <a href={activeSource.url} target="_blank" rel="noreferrer" className="text-link">
                Open original source
              </a>
            ) : null}
          </div>
        ) : (
          <p className="muted-copy">Choose an evidence source from the left panel.</p>
        )}
      </section>
    </div>
  );
}
