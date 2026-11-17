// Publications index — filterable list
const { Tag: PTag, MonoLabel: PMonoLabel, Button: PButton } = window.IPEDesignSystem_e09975;

function Publications({ onOpen }) {
  const D = window.IPE_DATA;
  const [active, setActive] = React.useState("Alle");
  const filters = ["Alle", ...D.themes.map((t) => t.name)];
  const list = active === "Alle" ? D.publications : D.publications.filter((p) => p.theme === active);

  return (
    <main style={{ maxWidth: 1100, margin: "0 auto", padding: "64px 48px 96px" }}>
      <PMonoLabel bullet>Publicaties</PMonoLabel>
      <h1 style={{ font: "var(--fw-bold) var(--text-4xl)/1 var(--font-sans)", letterSpacing: "-0.025em", margin: "16px 0 8px", color: "var(--text-body)" }}>
        Onderzoek &amp; policy papers
      </h1>
      <p style={{ font: "var(--type-lead)", color: "var(--text-soft)", maxWidth: 560, margin: 0 }}>
        Al ons werk — rapporten, papers en bijdragen aan het publieke debat.
      </p>

      {/* Filter row */}
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8, margin: "36px 0 28px", borderBottom: "1px solid var(--border-subtle)", paddingBottom: 24 }}>
        {filters.map((f) => {
          const on = active === f;
          return (
            <button key={f} onClick={() => setActive(f)} style={{
              border: "1px solid " + (on ? "var(--brand)" : "var(--border)"),
              background: on ? "var(--brand)" : "transparent",
              color: on ? "#fff" : "var(--text-body)",
              padding: "7px 14px", borderRadius: "var(--radius-pill)", cursor: "pointer",
              font: "var(--fw-medium) var(--text-sm)/1 var(--font-sans)",
            }}>{f}</button>
          );
        })}
      </div>

      {/* List */}
      <div style={{ display: "flex", flexDirection: "column" }}>
        {list.map((p) => (
          <button key={p.id} onClick={() => onOpen(p.id)} style={{
            border: "none", background: "none", cursor: "pointer", textAlign: "left",
            display: "grid", gridTemplateColumns: "150px 1fr auto", gap: 28, alignItems: "start",
            padding: "28px 0", borderTop: "1px solid var(--border-subtle)",
          }}>
            <div>
              <PMonoLabel color={p.color}>{p.kicker}</PMonoLabel>
              <div style={{ font: "var(--type-small)", color: "var(--text-muted)", marginTop: 8 }}>{p.date}</div>
            </div>
            <div>
              <h3 style={{ font: "var(--type-h3)", margin: "0 0 6px", color: "var(--text-body)" }}>{p.title}</h3>
              <p style={{ font: "var(--type-body)", color: "var(--text-soft)", margin: "0 0 12px", maxWidth: 560 }}>{p.excerpt}</p>
              <div style={{ font: "var(--type-small)", color: "var(--text-muted)" }}>{p.authors.join(" · ")}</div>
            </div>
            <span style={{ display: "inline-flex", color: p.color, marginTop: 4 }}><Icon name="arrow-up-right" size={22} color="currentColor" /></span>
          </button>
        ))}
      </div>
    </main>
  );
}

Object.assign(window, { Publications });
