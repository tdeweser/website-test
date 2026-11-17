import React from "react";

/**
 * IPE Card — white surface, hairline border, small radius, minimal
 * shadow. Brand identity comes from an optional red top-rule or a
 * mono label, not heavy chrome.
 */
export function Card({
  children,
  topRule = false,
  ruleColor = "var(--brand)",
  interactive = false,
  padding = 24,
  style,
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  return (
    <div
      onMouseEnter={() => interactive && setHover(true)}
      onMouseLeave={() => interactive && setHover(false)}
      style={{
        background: "var(--surface-card)",
        border: "var(--border-width) solid var(--border)",
        borderTop: topRule ? `3px solid ${ruleColor}` : "var(--border-width) solid var(--border)",
        borderRadius: "var(--radius-md)",
        padding,
        boxShadow: hover ? "var(--shadow-md)" : "var(--shadow-sm)",
        transform: hover ? "translateY(-2px)" : "none",
        transition: "box-shadow var(--dur-base) var(--ease-standard), transform var(--dur-base) var(--ease-standard)",
        cursor: interactive ? "pointer" : "default",
        ...style,
      }}
      {...rest}
    >
      {children}
    </div>
  );
}
