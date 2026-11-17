import React from "react";

/**
 * IPE Input — text field with a mono label, hairline border,
 * aqua focus ring.
 */
export function Input({ label, hint, error, id, style, ...rest }) {
  const [focus, setFocus] = React.useState(false);
  const inputId = id || (label ? "ipe-" + String(label).toLowerCase().replace(/\s+/g, "-") : undefined);
  const borderColor = error ? "var(--ipe-red)" : focus ? "var(--focus-ring)" : "var(--border)";
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 6, ...style }}>
      {label && (
        <label htmlFor={inputId} style={{
          font: "var(--fw-medium) var(--text-2xs)/1 var(--font-mono)",
          letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--text-soft)",
        }}>{label}</label>
      )}
      <input
        id={inputId}
        onFocus={() => setFocus(true)}
        onBlur={() => setFocus(false)}
        style={{
          font: "var(--fw-regular) var(--text-base)/1.4 var(--font-sans)",
          color: "var(--text-body)",
          background: "var(--surface-page)",
          padding: "10px 12px",
          border: `var(--border-width) solid ${borderColor}`,
          borderRadius: "var(--radius-sm)",
          outline: focus ? `2px solid color-mix(in srgb, var(--focus-ring) 35%, transparent)` : "none",
          outlineOffset: 1,
          transition: "border-color var(--dur-fast) var(--ease-standard)",
        }}
        {...rest}
      />
      {(hint || error) && (
        <span style={{
          font: "var(--fw-regular) var(--text-xs)/1.3 var(--font-sans)",
          color: error ? "var(--ipe-red)" : "var(--text-muted)",
        }}>{error || hint}</span>
      )}
    </div>
  );
}
