import React from "react";

/**
 * IPE Button — the brand's primary action control.
 * Rectilinear, DM Sans medium, red as the hero accent.
 */
export function Button({
  children,
  variant = "primary",
  size = "md",
  iconLeft,
  iconRight,
  disabled = false,
  fullWidth = false,
  style,
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  const [active, setActive] = React.useState(false);

  const sizes = {
    sm: { padding: "7px 14px", font: "var(--text-sm)", gap: 6 },
    md: { padding: "10px 20px", font: "var(--text-base)", gap: 8 },
    lg: { padding: "14px 28px", font: "var(--text-md)", gap: 10 },
  };
  const s = sizes[size] || sizes.md;

  const base = {
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    gap: s.gap,
    padding: s.padding,
    font: `var(--fw-medium) ${s.font}/1 var(--font-sans)`,
    letterSpacing: "0.01em",
    borderRadius: "var(--radius-sm)",
    border: "var(--border-width-strong) solid transparent",
    cursor: disabled ? "not-allowed" : "pointer",
    opacity: disabled ? 0.45 : 1,
    width: fullWidth ? "100%" : "auto",
    transition: "background var(--dur-fast) var(--ease-standard), color var(--dur-fast) var(--ease-standard), border-color var(--dur-fast) var(--ease-standard), transform var(--dur-fast) var(--ease-standard)",
    transform: active && !disabled ? "translateY(1px)" : "none",
    whiteSpace: "nowrap",
  };

  const variants = {
    primary: {
      background: active ? "var(--brand-active)" : hover ? "var(--brand-hover)" : "var(--brand)",
      color: "var(--text-on-brand)",
    },
    secondary: {
      background: hover ? "var(--ipe-red-l80)" : "transparent",
      color: "var(--brand)",
      borderColor: "var(--brand)",
    },
    ghost: {
      background: hover ? "var(--ipe-gray-20)" : "transparent",
      color: "var(--text-body)",
    },
    dark: {
      background: active ? "#222" : hover ? "#1a1a1a" : "var(--ipe-black)",
      color: "var(--text-on-dark)",
    },
  };

  return (
    <button
      type="button"
      disabled={disabled}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => { setHover(false); setActive(false); }}
      onMouseDown={() => setActive(true)}
      onMouseUp={() => setActive(false)}
      style={{ ...base, ...(variants[variant] || variants.primary), ...style }}
      {...rest}
    >
      {iconLeft}
      {children}
      {iconRight}
    </button>
  );
}
