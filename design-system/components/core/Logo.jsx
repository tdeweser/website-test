import React from "react";

/**
 * IPE Logo — the stacked wordmark, reconstructed in DM Mono.
 *
 * - "default":  a coloured block holds "Instituut / voor" (white text),
 *   with "Publieke / Economie" in the brand colour below on the page.
 * - "inverted": "Instituut / voor" in the brand colour on the page above,
 *   with "Publieke / Economie" in a coloured block (white text) below.
 *   On a brand-colour background the lower block merges into it, leaving a
 *   clean white-text lock-up — this is the variant used on the red title slide.
 *
 * For print/official use prefer the supplied logos (assets/logo/).
 */
export function Logo({ size = 40, variant = "default", color = "var(--brand)", style, ...rest }) {
  const line = {
    font: `300 ${size}px/0.98 var(--font-mono)`,
    letterSpacing: "-0.01em",
    margin: 0,
    display: "block",
  };
  const blockPad = `${size * 0.18}px ${size * 0.34}px ${size * 0.16}px`;
  const plainPad = `${size * 0.16}px ${size * 0.34}px 0`;

  const Block = ({ children }) => (
    <span style={{ display: "inline-block", background: color, color: "var(--ipe-white)", padding: blockPad }}>{children}</span>
  );
  const Plain = ({ children, top }) => (
    <span style={{ display: "block", color, padding: top ? `0 ${size * 0.34}px ${size * 0.06}px` : plainPad }}>{children}</span>
  );

  return (
    <span
      role="img"
      aria-label="Instituut voor Publieke Economie"
      style={{ display: "inline-block", lineHeight: 0, ...style }}
      {...rest}
    >
      {variant === "inverted" ? (
        <>
          <Plain top><span style={line}>Instituut</span><span style={line}>voor</span></Plain>
          <Block><span style={line}>Publieke</span><span style={line}>Economie</span></Block>
        </>
      ) : (
        <>
          <Block><span style={line}>Instituut</span><span style={line}>voor</span></Block>
          <Plain><span style={line}>Publieke</span><span style={line}>Economie</span></Plain>
        </>
      )}
    </span>
  );
}
