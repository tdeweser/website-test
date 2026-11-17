import React from "react";

/**
 * IPE Bullet — the signature red square list marker (▪).
 * Replaces the round dot in lists across the brand.
 */
export function Bullet({ size = 10, color = "var(--brand)", style, ...rest }) {
  return (
    <span
      aria-hidden="true"
      style={{
        display: "inline-block",
        width: size,
        height: size,
        background: color,
        flex: "0 0 auto",
        ...style,
      }}
      {...rest}
    />
  );
}

/**
 * BulletList — an <ul> using the red square marker, aligned to text.
 */
export function BulletList({ items = [], color = "var(--brand)", gap = 10, style, ...rest }) {
  return (
    <ul
      style={{
        listStyle: "none",
        margin: 0,
        padding: 0,
        display: "flex",
        flexDirection: "column",
        gap,
        font: "var(--type-body)",
        color: "var(--text-body)",
        ...style,
      }}
      {...rest}
    >
      {items.map((it, i) => (
        <li key={i} style={{ display: "flex", gap: 12, alignItems: "baseline" }}>
          <Bullet color={color} style={{ position: "relative", top: 1 }} />
          <span>{it}</span>
        </li>
      ))}
    </ul>
  );
}
