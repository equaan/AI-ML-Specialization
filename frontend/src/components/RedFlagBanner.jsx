import { TriangleAlert } from "lucide-react";

export function RedFlagBanner({ redFlags }) {
  if (!redFlags?.length) return null;

  return (
    <section className="red-flag-banner">
      <TriangleAlert size={24} />
      <div>
        <h3>Red Flags Detected</h3>
        {redFlags.map((flag) => (
          <p key={flag}>{flag}</p>
        ))}
      </div>
    </section>
  );
}
