import React from "react";

/**
 * IPE Callout — a flat note block in a brand colour, with a red
 * (or accent) left rule. For source notes, key takeaways, alerts.
 */
export function Callout({ children, title, tone = "neutral", style, ...rest }) {
  const tones = {
    neutral: { bar: "var(--ipe-black)", bg: "var(--surface-sunken)" },
    brand:   { bar: "var(--ipe-red)",   bg: "var(--ipe-red-l80)" },
    info:    { bar: "var(--ipe-aqua)",  bg: "color-mix(in srgb, var(--ipe-aqua) 14%, white)" },
    positive:{ bar: "var(--ipe-green)", bg: "color-mix(in srgb, var(--ipe-green) 14%, white)" },
  };
  const t = tones[tone] || tones.neutral;
  return (
    <div
      style={{
        background: t.bg,
        borderLeft: `4px solid ${t.bar}`,
        padding: "16px 20px",
        display: "flex",
        flexDirection: "column",
        gap: 4,
        ...style,
      }}
      {...rest}
    >
      {title && (
        <span style={{ font: "var(--fw-semibold) var(--text-base)/1.3 var(--font-sans)", color: "var(--text-body)" }}>{title}</span>
      )}
      <div style={{ font: "var(--fw-regular) var(--text-sm)/1.5 var(--font-sans)", color: "var(--text-soft)" }}>{children}</div>
    </div>
  );
}
