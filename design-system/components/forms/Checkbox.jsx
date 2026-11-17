import React from "react";

/**
 * IPE Checkbox — square check with red fill when selected.
 */
export function Checkbox({ label, checked, onChange, disabled = false, style, ...rest }) {
  return (
    <label style={{
      display: "inline-flex", alignItems: "center", gap: 10, cursor: disabled ? "not-allowed" : "pointer",
      opacity: disabled ? 0.5 : 1, font: "var(--type-body)", color: "var(--text-body)", ...style,
    }}>
      <span
        onClick={() => !disabled && onChange && onChange(!checked)}
        style={{
          width: 18, height: 18, flex: "0 0 auto",
          border: `var(--border-width-strong) solid ${checked ? "var(--brand)" : "var(--border-strong)"}`,
          background: checked ? "var(--brand)" : "transparent",
          borderRadius: "var(--radius-xs)",
          display: "inline-flex", alignItems: "center", justifyContent: "center",
          transition: "background var(--dur-fast) var(--ease-standard), border-color var(--dur-fast) var(--ease-standard)",
        }}
      >
        {checked && (
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="3.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="20 6 9 17 4 12" />
          </svg>
        )}
      </span>
      {label && <span>{label}</span>}
      <input type="checkbox" checked={checked} disabled={disabled} onChange={(e) => onChange && onChange(e.target.checked)} style={{ position: "absolute", opacity: 0, width: 0, height: 0 }} {...rest} />
    </label>
  );
}
