import React from "react";

/**
 * IPE StatCard — a headline figure set in DM Mono (the brand's
 * data cue) with a label and optional source note.
 */
export function StatCard({ value, label, source, color = "var(--brand)", style, ...rest }) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 6,
        padding: "20px 24px",
        background: "var(--surface-card)",
        borderLeft: `4px solid ${color}`,
        ...style,
      }}
      {...rest}
    >
      <span style={{ font: `var(--fw-medium) var(--text-3xl)/1 var(--font-mono)`, color, letterSpacing: "-0.02em" }}>
        {value}
      </span>
      <span style={{ font: "var(--fw-medium) var(--text-base)/1.3 var(--font-sans)", color: "var(--text-body)" }}>
        {label}
      </span>
      {source && (
        <span style={{ font: "var(--fw-regular) var(--text-2xs)/1.3 var(--font-mono)", color: "var(--text-muted)", letterSpacing: "0.02em" }}>
          {source}
        </span>
      )}
    </div>
  );
}
