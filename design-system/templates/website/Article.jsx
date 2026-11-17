// Article / report detail
const { Tag: ATag, MonoLabel: AMonoLabel, Button: AButton, Callout: ACallout, StatCard: AStatCard, BulletList: ABulletList } = window.IPEDesignSystem_e09975;

function Article({ id, onBack }) {
  const D = window.IPE_DATA;
  const p = D.publications.find((x) => x.id === id) || D.publications[0];
  return (
    <main>
      {/* Cover band */}
      <section style={{ background: "var(--surface-alt)", padding: "40px 48px 0" }}>
        <div style={{ maxWidth: 840, margin: "0 auto" }}>
          <button onClick={onBack} style={{ border: "none", background: "none", cursor: "pointer", display: "inline-flex", alignItems: "center", gap: 8, color: "var(--text-soft)", font: "var(--type-small)", padding: 0, marginBottom: 28 }}>
            <Icon name="arrow-left" size={16} /> Terug naar publicaties
          </button>
          <AMonoLabel color={p.color}>{p.kicker}</AMonoLabel>
          <h1 style={{ font: "var(--fw-bold) var(--text-4xl)/1.02 var(--font-sans)", letterSpacing: "-0.025em", margin: "16px 0 10px", color: "var(--text-body)", textWrap: "balance" }}>{p.title}</h1>
          <p style={{ font: "var(--type-lead)", color: "var(--text-soft)", margin: 0 }}>{p.subtitle}</p>
          <div style={{ display: "flex", gap: 24, margin: "28px 0 0", paddingBottom: 0, flexWrap: "wrap" }}>
            <Meta label="Auteurs" value={p.authors.join(", ")} />
            <Meta label="Gepubliceerd" value={p.date} />
            <Meta label="Thema" value={p.theme} />
          </div>
          <div style={{ height: 56, background: p.color, margin: "32px -48px 0", maxWidth: 840, marginLeft: "auto", marginRight: "auto", width: "100%" }} />
        </div>
      </section>

      {/* Body */}
      <article style={{ maxWidth: 840, margin: "0 auto", padding: "48px 48px 96px" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: 24 }}>
          <p style={{ font: "var(--fw-regular) var(--text-md)/1.7 var(--font-sans)", color: "var(--text-body)", margin: 0 }}>
            <strong>{p.excerpt}</strong>
          </p>
          <p style={{ font: "var(--type-body)", lineHeight: 1.75, color: "var(--text-soft)", margin: 0 }}>
            Het Nederlandse beleid is over de jaren heen vastgelopen in een opeenstapeling van regelingen, toeslagen en uitzonderingen. Elk afzonderlijk goed bedoeld, maar samen vormen ze een doolhof dat noch voor burgers, noch voor uitvoerders nog te begrijpen is. Wij analyseren waar de complexiteit vandaan komt en wat het kost.
          </p>

          <ACallout tone="brand" title="Kernpunt">
            Een landelijke basis met ruimte voor lokaal maatwerk is eerlijker voor mensen én eenvoudiger voor gemeenten.
          </ACallout>

          <h2 style={{ font: "var(--type-h2)", margin: "16px 0 0", color: "var(--text-body)" }}>De cijfers</h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 16 }}>
            <AStatCard value={D.stats[1].value} label={D.stats[1].label} source={D.stats[1].source} color={p.color} />
            <AStatCard value={D.stats[0].value} label={D.stats[0].label} source={D.stats[0].source} color="var(--ipe-aqua)" />
          </div>

          <h2 style={{ font: "var(--type-h2)", margin: "16px 0 0", color: "var(--text-body)" }}>Onze voorstellen</h2>
          <ABulletList items={[
            "Eén landelijke basisregeling die bestaanszekerheid garandeert.",
            "Lokaal maatwerk binnen heldere kaders, zonder nieuwe loketten.",
            "Automatische toekenning waar dat kan — geen aanvraag, geen drempel.",
          ]} style={{ font: "var(--type-lead)" }} />

          <ACallout tone="neutral">Bron: Modelschatting op basis van CBS micro-data. Toelichting: n = 282.421 huishoudens.</ACallout>

          <div style={{ display: "flex", gap: 12, marginTop: 12 }}>
            <AButton variant="primary" iconLeft={<Icon name="download" size={18} />}>Download het rapport (PDF)</AButton>
            <AButton variant="secondary">Deel</AButton>
          </div>
        </div>
      </article>
    </main>
  );
}

function Meta({ label, value }) {
  return (
    <div>
      <div style={{ font: "var(--fw-medium) var(--text-2xs)/1 var(--font-mono)", letterSpacing: "0.06em", textTransform: "uppercase", color: "var(--text-muted)", marginBottom: 6 }}>{label}</div>
      <div style={{ font: "var(--fw-medium) var(--text-sm)/1.3 var(--font-sans)", color: "var(--text-body)" }}>{value}</div>
    </div>
  );
}

Object.assign(window, { Article });
