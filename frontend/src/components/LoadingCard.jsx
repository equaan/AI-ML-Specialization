export function LoadingCard({ title = "Loading data..." }) {
  return (
    <div className="workspace-card loading-card">
      <p className="panel-kicker">Live State</p>
      <h3>{title}</h3>
      <div className="loading-skeleton-lines">
        <span />
        <span />
        <span />
      </div>
    </div>
  );
}
