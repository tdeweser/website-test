import React from "react";

/**
 * IPE Tag — a pill chip for categories, topics, filters.
 * One of the few rounded shapes in the system.
 */
export function Tag({ children, color = "red", solid = false, style, ...rest }) {
  const map = {
    red:   { fg: "var(--ipe-red)",   bg: "var(--ipe-red-l80)",  solidFg: "#fff" },
    navy:  { fg: "var(--ipe-navy)",  bg: "var(--ipe-navy-l80)", solidFg: "#fff" },
    aqua:  { fg: "var(--ipe-aqua)",  bg: "color-mix(in srgb, var(--ipe-aqua) 16%, white)",  solidFg: "#fff" },
    green: { fg: "var(--ipe-green)", bg: "color-mix(in srgb, var(--ipe-green) 16%, white)", solidFg: "#fff" },
    gray:  { fg: "var(--ipe-ink-40)",bg: "var(--ipe-gray-20)",  solidFg: "#fff" },
  };
  const c = map[color] || map.red;
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 6,
        padding: "4px 12px",
        font: "var(--fw-medium) var(--text-sm)/1 var(--font-sans)",
        borderRadius: "var(--radius-pill)",
        background: solid ? c.fg : c.bg,
        color: solid ? c.solidFg : c.fg,
        whiteSpace: "nowrap",
        ...style,
      }}
      {...rest}
    >
      {children}
    </span>
  );
}
