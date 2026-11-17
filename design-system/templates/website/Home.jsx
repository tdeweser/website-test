// Home screen
const { Button: HButton, Tag: HTag, MonoLabel: HMonoLabel, Card: HCard, StatCard: HStatCard, BulletList: HBulletList } = window.IPEDesignSystem_e09975;

function PubCard({ pub, onOpen }) {
  return (
    <HCard topRule ruleColor={pub.color} interactive onClick={() => onOpen(pub.id)} style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <HMonoLabel color={pub.color}>{pub.kicker}</HMonoLabel>
      <h3 style={{ font: "var(--type-h3)", margin: "12px 0 6px", color: "var(--text-body)", textWrap: "balance" }}>{pub.title}</h3>
      <p style={{ font: "var(--type-small)", color: "var(--text-soft)", margin: "0 0 16px", flex: 1 }}>{pub.subtitle}</p>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <HTag color={pub.color === "var(--ipe-red)" ? "red" : pub.color === "var(--ipe-aqua)" ? "aqua" : pub.color === "var(--ipe-green)" ? "green" : "blue"}>{pub.theme}</HTag>
        <span style={{ display: "inline-flex", color: pub.color }}><Icon name="arrow-up-right" size={20} color="currentColor" /></span>
      </div>
    </HCard>
  );
}

function Home({ onOpen }) {
  const D = window.IPE_DATA;
  const featured = D.publications.find((p) => p.featured) || D.publications[0];
  const rest = D.publications.filter((p) => p !== featured).slice(0, 3);
  return (
    <main>
      {/* Hero */}
      <section style={{ padding: "72px 48px 0", maxWidth: 1320, margin: "0 auto" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1.15fr 0.85fr", gap: 56, alignItems: "center" }}>
          <div>
            <HMonoLabel bullet>Onafhankelijke denktank · Den Haag</HMonoLabel>
            <h1 style={{ font: "var(--fw-bold) var(--text-5xl)/0.98 var(--font-sans)", letterSpacing: "-0.025em", margin: "20px 0 0", color: "var(--text-body)", textWrap: "balance" }}>
              Inhoud met impact
            </h1>
            <p style={{ font: "var(--type-lead)", color: "var(--text-soft)", margin: "24px 0 0", maxWidth: 520 }}>
              Beter beleid is de snelste weg naar een betere wereld. Daarom brengen wij de overheid in beweging — met onderzoek, scherpe voorstellen en een onafhankelijke stem in het publieke debat.
            </p>
            <div style={{ display: "flex", gap: 14, marginTop: 32 }}>
              <HButton variant="primary" size="lg" onClick={() => onOpen(featured.id)}>Lees ons werk</HButton>
              <HButton variant="secondary" size="lg">Over het instituut</HButton>
            </div>
          </div>
          {/* Featured cover */}
          <div style={{ position: "relative" }}>
            <div style={{ background: "var(--surface-alt)", aspectRatio: "3/4", borderRadius: "var(--radius-md)", padding: 36, display: "flex", flexDirection: "column", justifyContent: "flex-start", overflow: "hidden", position: "relative" }}>
              <HMonoLabel color={featured.color}>{featured.kicker}</HMonoLabel>
              <h2 style={{ font: "var(--fw-bold) var(--text-2xl)/1.05 var(--font-sans)", letterSpacing: "-0.02em", margin: "16px 0 0", color: "var(--text-body)", textWrap: "balance" }}>{featured.title}</h2>
              <p style={{ font: "var(--type-small)", color: "var(--text-soft)", marginTop: 10 }}>{featured.subtitle}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Stats strip */}
      <section style={{ maxWidth: 1320, margin: "64px auto 0", padding: "0 48px" }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 1, background: "var(--border)", border: "1px solid var(--border)" }}>
          {D.stats.map((s, i) => (
            <HStatCard key={i} value={s.value} label={s.label} source={s.source} color={i === 0 ? "var(--ipe-aqua)" : i === 1 ? "var(--ipe-red)" : "var(--ipe-green)"} style={{ background: "var(--surface-page)" }} />
          ))}
        </div>
      </section>

      {/* Latest publications */}
      <section style={{ maxWidth: 1320, margin: "80px auto 0", padding: "0 48px" }}>
        <div style={{ display: "flex", alignItems: "flex-end", justifyContent: "space-between", marginBottom: 28 }}>
          <div>
            <HMonoLabel bullet>Publicaties</HMonoLabel>
            <h2 style={{ font: "var(--type-h2)", margin: "10px 0 0", color: "var(--text-body)" }}>Recent onderzoek</h2>
          </div>
          <HButton variant="ghost" iconRight={<Icon name="arrow-right" size={18} />}>Alle publicaties</HButton>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 20 }}>
          {rest.map((p) => <PubCard key={p.id} pub={p} onOpen={onOpen} />)}
        </div>
      </section>

      {/* Mission + themes */}
      <section style={{ background: "var(--surface-alt)", marginTop: 80, padding: "72px 48px" }}>
        <div style={{ maxWidth: 1320, margin: "0 auto" }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 64, alignItems: "start" }}>
            <div>
              <HMonoLabel bullet>Over het instituut</HMonoLabel>
              <h2 style={{ font: "var(--type-h2)", margin: "10px 0 20px", color: "var(--text-body)", textWrap: "balance" }}>Een onafhankelijke denktank</h2>
              <p style={{ font: "var(--type-lead)", color: "var(--text-soft)", margin: 0 }}>{D.about.intro}</p>
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
              {D.about.pillars.map((p, i) => (
                <div key={i} style={{ display: "flex", gap: 16, paddingBottom: 16, borderBottom: i < 2 ? "1px solid var(--border)" : "none" }}>
                  <span style={{ width: 12, height: 12, background: "var(--brand)", flex: "0 0 auto", marginTop: 6 }} />
                  <div>
                    <h3 style={{ font: "var(--fw-bold) var(--text-md)/1.3 var(--font-sans)", margin: "0 0 4px", color: "var(--text-body)" }}>{p.title}</h3>
                    <p style={{ font: "var(--type-small)", color: "var(--text-soft)", margin: 0 }}>{p.body}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div style={{ marginTop: 56 }}>
            <HMonoLabel bullet>Thema's</HMonoLabel>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 10, marginTop: 16 }}>
              {D.themes.map((t) => (
                <span key={t.name} style={{ display: "inline-flex", alignItems: "center", gap: 8, padding: "8px 14px", background: "var(--surface-page)", border: "1px solid var(--border)", borderRadius: "var(--radius-pill)", font: "var(--fw-medium) var(--text-sm)/1 var(--font-sans)", color: "var(--text-body)" }}>
                  <span style={{ width: 9, height: 9, background: t.color }} />{t.name}
                </span>
              ))}
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

Object.assign(window, { Home, PubCard });
