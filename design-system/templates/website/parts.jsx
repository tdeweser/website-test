// Shared website parts: Icon, Header, Footer
const { Logo, Button } = window.IPEDesignSystem_e09975;

// Lucide icon — renders an <i data-lucide> and asks Lucide to draw it.
function Icon({ name, size = 20, color = "currentColor", strokeWidth = 2, style }) {
  const ref = React.useRef(null);
  React.useEffect(() => {
    if (ref.current && window.lucide) {
      ref.current.innerHTML = "";
      const el = document.createElement("i");
      el.setAttribute("data-lucide", name);
      ref.current.appendChild(el);
      window.lucide.createIcons({
        attrs: { width: size, height: size, stroke: color, "stroke-width": strokeWidth },
        nameAttr: "data-lucide",
      });
    }
  }, [name, size, color, strokeWidth]);
  return <span ref={ref} style={{ display: "inline-flex", lineHeight: 0, ...style }} />;
}

const NAV = ["Onderzoek", "Thema's", "Publicaties", "Over ons"];

function Header({ current, onNav }) {
  return (
    <header style={{
      display: "flex", alignItems: "center", justifyContent: "space-between",
      padding: "20px 48px", borderBottom: "1px solid var(--border-subtle)",
      background: "var(--surface-page)", position: "sticky", top: 0, zIndex: 20,
    }}>
      <button onClick={() => onNav("home")} style={{ border: "none", background: "none", cursor: "pointer", padding: 0 }}>
        <Logo size={17} />
      </button>
      <nav style={{ display: "flex", alignItems: "center", gap: 34 }}>
        {NAV.map((n) => {
          const active = current === n;
          return (
            <button key={n} onClick={() => onNav(n === "Publicaties" ? "publications" : "home")}
              style={{
                border: "none", background: "none", cursor: "pointer", padding: "4px 0",
                font: "var(--fw-medium) var(--text-base)/1 var(--font-sans)",
                color: active ? "var(--brand)" : "var(--text-body)",
                borderBottom: active ? "2px solid var(--brand)" : "2px solid transparent",
              }}>
              {n}
            </button>
          );
        })}
        <button style={{ border: "none", background: "none", cursor: "pointer", padding: 0, color: "var(--text-body)" }}>
          <Icon name="search" size={20} />
        </button>
        <Button variant="primary" size="sm">Nieuwsbrief</Button>
      </nav>
    </header>
  );
}

function Footer() {
  return (
    <footer style={{ background: "var(--ipe-black)", color: "var(--ipe-white)", padding: "56px 48px 40px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", flexWrap: "wrap", gap: 40 }}>
        <div style={{ maxWidth: 320 }}>
          <Logo size={20} variant="inverted" />
          <p style={{ font: "var(--type-small)", color: "var(--ipe-gray-40)", marginTop: 18, lineHeight: 1.6 }}>
            Inhoud met impact. Beter beleid is de snelste weg naar een betere wereld.
          </p>
        </div>
        <div style={{ display: "flex", gap: 64, flexWrap: "wrap" }}>
          <div>
            <div style={{ font: "var(--fw-medium) var(--text-2xs)/1 var(--font-mono)", letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--ipe-red)", marginBottom: 14 }}>Contact</div>
            <div style={{ font: "var(--type-small)", color: "var(--ipe-gray-40)", lineHeight: 1.9 }}>
              Plein 17<br />2511 CS Den Haag<br />info@ipe.nl<br />www.ipe.nl
            </div>
          </div>
          <div>
            <div style={{ font: "var(--fw-medium) var(--text-2xs)/1 var(--font-mono)", letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--ipe-red)", marginBottom: 14 }}>Volg ons</div>
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {["LinkedIn", "X / Twitter", "Nieuwsbrief"].map((l) => (
                <a key={l} href="#" style={{ font: "var(--type-small)", color: "var(--ipe-gray-40)", textDecoration: "none" }}>{l}</a>
              ))}
            </div>
          </div>
        </div>
      </div>
      <div style={{ height: 8, background: "var(--brand)", marginTop: 40, width: 120 }} />
    </footer>
  );
}

Object.assign(window, { Icon, Header, Footer, NAV });
