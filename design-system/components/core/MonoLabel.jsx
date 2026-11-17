import React from "react";

/**
 * IPE MonoLabel — a small uppercase DM Mono label/eyebrow.
 * Used for kickers, data labels and section tags. Optional
 * leading red square.
 */
export function MonoLabel({ children, color = "var(--brand)", bullet = false, style, ...rest }) {
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 8,
        font: "var(--fw-medium) var(--text-2xs)/1 var(--font-mono)",
        letterSpacing: "0.08em",
        textTransform: "uppercase",
        color,
        ...style,
      }}
      {...rest}
    >
      {bullet && (
        <span style={{ width: 8, height: 8, background: "var(--brand)", display: "inline-block" }} aria-hidden="true" />
      )}
      {children}
    </span>
  );
}
