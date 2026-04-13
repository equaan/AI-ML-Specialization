import { ExternalLink, LibraryBig } from "lucide-react";

export function SourceChip({ source, active = false, onClick }) {
  const content = (
    <>
      <div className="source-chip-icon">
        <LibraryBig size={14} />
      </div>
      <div className="source-chip-content">
        <strong>{source.title}</strong>
        <span>{source.pmid ? `PMID: ${source.pmid}` : "Retrieved source"}</span>
      </div>
      {source.url ? <ExternalLink size={14} /> : null}
    </>
  );

  if (onClick) {
    return (
      <button type="button" className={`source-chip ${active ? "active" : ""}`} onClick={onClick}>
        {content}
      </button>
    );
  }

  return source.url ? (
    <a className="source-chip" href={source.url} target="_blank" rel="noreferrer">
      {content}
    </a>
  ) : (
    <div className="source-chip">{content}</div>
  );
}
