/* @ds-bundle: {"format":4,"namespace":"IPEDesignSystem_e09975","components":[{"name":"Bullet","sourcePath":"components/core/Bullet.jsx"},{"name":"BulletList","sourcePath":"components/core/Bullet.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"Logo","sourcePath":"components/core/Logo.jsx"},{"name":"MonoLabel","sourcePath":"components/core/MonoLabel.jsx"},{"name":"Tag","sourcePath":"components/core/Tag.jsx"},{"name":"Callout","sourcePath":"components/feedback/Callout.jsx"},{"name":"Checkbox","sourcePath":"components/forms/Checkbox.jsx"},{"name":"Input","sourcePath":"components/forms/Input.jsx"},{"name":"Card","sourcePath":"components/surfaces/Card.jsx"},{"name":"StatCard","sourcePath":"components/surfaces/StatCard.jsx"}],"sourceHashes":{"components/core/Bullet.jsx":"5a12300f5b55","components/core/Button.jsx":"9dfa4fbd6a3b","components/core/Logo.jsx":"872cfaf2d019","components/core/MonoLabel.jsx":"b3fe1e71d199","components/core/Tag.jsx":"22cdf69cc252","components/feedback/Callout.jsx":"c016bad393fb","components/forms/Checkbox.jsx":"cc7525fd4d43","components/forms/Input.jsx":"c32e65fc3413","components/surfaces/Card.jsx":"fefe54c2ba88","components/surfaces/StatCard.jsx":"6d312091b22d"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.IPEDesignSystem_e09975 = window.IPEDesignSystem_e09975 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/core/Bullet.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * IPE Bullet — the signature red square list marker (▪).
 * Replaces the round dot in lists across the brand.
 */
function Bullet({
  size = 10,
  color = "var(--brand)",
  style,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("span", _extends({
    "aria-hidden": "true",
    style: {
      display: "inline-block",
      width: size,
      height: size,
      background: color,
      flex: "0 0 auto",
      ...style
    }
  }, rest));
}

/**
 * BulletList — an <ul> using the red square marker, aligned to text.
 */
function BulletList({
  items = [],
  color = "var(--brand)",
  gap = 10,
  style,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("ul", _extends({
    style: {
      listStyle: "none",
      margin: 0,
      padding: 0,
      display: "flex",
      flexDirection: "column",
      gap,
      font: "var(--type-body)",
      color: "var(--text-body)",
      ...style
    }
  }, rest), items.map((it, i) => /*#__PURE__*/React.createElement("li", {
    key: i,
    style: {
      display: "flex",
      gap: 12,
      alignItems: "baseline"
    }
  }, /*#__PURE__*/React.createElement(Bullet, {
    color: color,
    style: {
      position: "relative",
      top: 1
    }
  }), /*#__PURE__*/React.createElement("span", null, it))));
}
Object.assign(__ds_scope, { Bullet, BulletList });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Bullet.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * IPE Button — the brand's primary action control.
 * Rectilinear, DM Sans medium, red as the hero accent.
 */
function Button({
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
    sm: {
      padding: "7px 14px",
      font: "var(--text-sm)",
      gap: 6
    },
    md: {
      padding: "10px 20px",
      font: "var(--text-base)",
      gap: 8
    },
    lg: {
      padding: "14px 28px",
      font: "var(--text-md)",
      gap: 10
    }
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
    whiteSpace: "nowrap"
  };
  const variants = {
    primary: {
      background: active ? "var(--brand-active)" : hover ? "var(--brand-hover)" : "var(--brand)",
      color: "var(--text-on-brand)"
    },
    secondary: {
      background: hover ? "var(--ipe-red-l80)" : "transparent",
      color: "var(--brand)",
      borderColor: "var(--brand)"
    },
    ghost: {
      background: hover ? "var(--ipe-gray-20)" : "transparent",
      color: "var(--text-body)"
    },
    dark: {
      background: active ? "#222" : hover ? "#1a1a1a" : "var(--ipe-black)",
      color: "var(--text-on-dark)"
    }
  };
  return /*#__PURE__*/React.createElement("button", _extends({
    type: "button",
    disabled: disabled,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => {
      setHover(false);
      setActive(false);
    },
    onMouseDown: () => setActive(true),
    onMouseUp: () => setActive(false),
    style: {
      ...base,
      ...(variants[variant] || variants.primary),
      ...style
    }
  }, rest), iconLeft, children, iconRight);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/Logo.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
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
function Logo({
  size = 40,
  variant = "default",
  color = "var(--brand)",
  style,
  ...rest
}) {
  const line = {
    font: `300 ${size}px/0.98 var(--font-mono)`,
    letterSpacing: "-0.01em",
    margin: 0,
    display: "block"
  };
  const blockPad = `${size * 0.18}px ${size * 0.34}px ${size * 0.16}px`;
  const plainPad = `${size * 0.16}px ${size * 0.34}px 0`;
  const Block = ({
    children
  }) => /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-block",
      background: color,
      color: "var(--ipe-white)",
      padding: blockPad
    }
  }, children);
  const Plain = ({
    children,
    top
  }) => /*#__PURE__*/React.createElement("span", {
    style: {
      display: "block",
      color,
      padding: top ? `0 ${size * 0.34}px ${size * 0.06}px` : plainPad
    }
  }, children);
  return /*#__PURE__*/React.createElement("span", _extends({
    role: "img",
    "aria-label": "Instituut voor Publieke Economie",
    style: {
      display: "inline-block",
      lineHeight: 0,
      ...style
    }
  }, rest), variant === "inverted" ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Plain, {
    top: true
  }, /*#__PURE__*/React.createElement("span", {
    style: line
  }, "Instituut"), /*#__PURE__*/React.createElement("span", {
    style: line
  }, "voor")), /*#__PURE__*/React.createElement(Block, null, /*#__PURE__*/React.createElement("span", {
    style: line
  }, "Publieke"), /*#__PURE__*/React.createElement("span", {
    style: line
  }, "Economie"))) : /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Block, null, /*#__PURE__*/React.createElement("span", {
    style: line
  }, "Instituut"), /*#__PURE__*/React.createElement("span", {
    style: line
  }, "voor")), /*#__PURE__*/React.createElement(Plain, null, /*#__PURE__*/React.createElement("span", {
    style: line
  }, "Publieke"), /*#__PURE__*/React.createElement("span", {
    style: line
  }, "Economie"))));
}
Object.assign(__ds_scope, { Logo });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Logo.jsx", error: String((e && e.message) || e) }); }

// components/core/MonoLabel.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * IPE MonoLabel — a small uppercase DM Mono label/eyebrow.
 * Used for kickers, data labels and section tags. Optional
 * leading red square.
 */
function MonoLabel({
  children,
  color = "var(--brand)",
  bullet = false,
  style,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: 8,
      font: "var(--fw-medium) var(--text-2xs)/1 var(--font-mono)",
      letterSpacing: "0.08em",
      textTransform: "uppercase",
      color,
      ...style
    }
  }, rest), bullet && /*#__PURE__*/React.createElement("span", {
    style: {
      width: 8,
      height: 8,
      background: "var(--brand)",
      display: "inline-block"
    },
    "aria-hidden": "true"
  }), children);
}
Object.assign(__ds_scope, { MonoLabel });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/MonoLabel.jsx", error: String((e && e.message) || e) }); }

// components/core/Tag.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * IPE Tag — a pill chip for categories, topics, filters.
 * One of the few rounded shapes in the system.
 */
function Tag({
  children,
  color = "red",
  solid = false,
  style,
  ...rest
}) {
  const map = {
    red: {
      fg: "var(--ipe-red)",
      bg: "var(--ipe-red-l80)",
      solidFg: "#fff"
    },
    navy: {
      fg: "var(--ipe-navy)",
      bg: "var(--ipe-navy-l80)",
      solidFg: "#fff"
    },
    aqua: {
      fg: "var(--ipe-aqua)",
      bg: "color-mix(in srgb, var(--ipe-aqua) 16%, white)",
      solidFg: "#fff"
    },
    green: {
      fg: "var(--ipe-green)",
      bg: "color-mix(in srgb, var(--ipe-green) 16%, white)",
      solidFg: "#fff"
    },
    gray: {
      fg: "var(--ipe-ink-40)",
      bg: "var(--ipe-gray-20)",
      solidFg: "#fff"
    }
  };
  const c = map[color] || map.red;
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: 6,
      padding: "4px 12px",
      font: "var(--fw-medium) var(--text-sm)/1 var(--font-sans)",
      borderRadius: "var(--radius-pill)",
      background: solid ? c.fg : c.bg,
      color: solid ? c.solidFg : c.fg,
      whiteSpace: "nowrap",
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { Tag });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Tag.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Callout.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * IPE Callout — a flat note block in a brand colour, with a red
 * (or accent) left rule. For source notes, key takeaways, alerts.
 */
function Callout({
  children,
  title,
  tone = "neutral",
  style,
  ...rest
}) {
  const tones = {
    neutral: {
      bar: "var(--ipe-black)",
      bg: "var(--surface-sunken)"
    },
    brand: {
      bar: "var(--ipe-red)",
      bg: "var(--ipe-red-l80)"
    },
    info: {
      bar: "var(--ipe-aqua)",
      bg: "color-mix(in srgb, var(--ipe-aqua) 14%, white)"
    },
    positive: {
      bar: "var(--ipe-green)",
      bg: "color-mix(in srgb, var(--ipe-green) 14%, white)"
    }
  };
  const t = tones[tone] || tones.neutral;
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      background: t.bg,
      borderLeft: `4px solid ${t.bar}`,
      padding: "16px 20px",
      display: "flex",
      flexDirection: "column",
      gap: 4,
      ...style
    }
  }, rest), title && /*#__PURE__*/React.createElement("span", {
    style: {
      font: "var(--fw-semibold) var(--text-base)/1.3 var(--font-sans)",
      color: "var(--text-body)"
    }
  }, title), /*#__PURE__*/React.createElement("div", {
    style: {
      font: "var(--fw-regular) var(--text-sm)/1.5 var(--font-sans)",
      color: "var(--text-soft)"
    }
  }, children));
}
Object.assign(__ds_scope, { Callout });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Callout.jsx", error: String((e && e.message) || e) }); }

// components/forms/Checkbox.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * IPE Checkbox — square check with red fill when selected.
 */
function Checkbox({
  label,
  checked,
  onChange,
  disabled = false,
  style,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("label", {
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: 10,
      cursor: disabled ? "not-allowed" : "pointer",
      opacity: disabled ? 0.5 : 1,
      font: "var(--type-body)",
      color: "var(--text-body)",
      ...style
    }
  }, /*#__PURE__*/React.createElement("span", {
    onClick: () => !disabled && onChange && onChange(!checked),
    style: {
      width: 18,
      height: 18,
      flex: "0 0 auto",
      border: `var(--border-width-strong) solid ${checked ? "var(--brand)" : "var(--border-strong)"}`,
      background: checked ? "var(--brand)" : "transparent",
      borderRadius: "var(--radius-xs)",
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      transition: "background var(--dur-fast) var(--ease-standard), border-color var(--dur-fast) var(--ease-standard)"
    }
  }, checked && /*#__PURE__*/React.createElement("svg", {
    width: "12",
    height: "12",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "#fff",
    strokeWidth: "3.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("polyline", {
    points: "20 6 9 17 4 12"
  }))), label && /*#__PURE__*/React.createElement("span", null, label), /*#__PURE__*/React.createElement("input", _extends({
    type: "checkbox",
    checked: checked,
    disabled: disabled,
    onChange: e => onChange && onChange(e.target.checked),
    style: {
      position: "absolute",
      opacity: 0,
      width: 0,
      height: 0
    }
  }, rest)));
}
Object.assign(__ds_scope, { Checkbox });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Checkbox.jsx", error: String((e && e.message) || e) }); }

// components/forms/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * IPE Input — text field with a mono label, hairline border,
 * aqua focus ring.
 */
function Input({
  label,
  hint,
  error,
  id,
  style,
  ...rest
}) {
  const [focus, setFocus] = React.useState(false);
  const inputId = id || (label ? "ipe-" + String(label).toLowerCase().replace(/\s+/g, "-") : undefined);
  const borderColor = error ? "var(--ipe-red)" : focus ? "var(--focus-ring)" : "var(--border)";
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 6,
      ...style
    }
  }, label && /*#__PURE__*/React.createElement("label", {
    htmlFor: inputId,
    style: {
      font: "var(--fw-medium) var(--text-2xs)/1 var(--font-mono)",
      letterSpacing: "0.08em",
      textTransform: "uppercase",
      color: "var(--text-soft)"
    }
  }, label), /*#__PURE__*/React.createElement("input", _extends({
    id: inputId,
    onFocus: () => setFocus(true),
    onBlur: () => setFocus(false),
    style: {
      font: "var(--fw-regular) var(--text-base)/1.4 var(--font-sans)",
      color: "var(--text-body)",
      background: "var(--surface-page)",
      padding: "10px 12px",
      border: `var(--border-width) solid ${borderColor}`,
      borderRadius: "var(--radius-sm)",
      outline: focus ? `2px solid color-mix(in srgb, var(--focus-ring) 35%, transparent)` : "none",
      outlineOffset: 1,
      transition: "border-color var(--dur-fast) var(--ease-standard)"
    }
  }, rest)), (hint || error) && /*#__PURE__*/React.createElement("span", {
    style: {
      font: "var(--fw-regular) var(--text-xs)/1.3 var(--font-sans)",
      color: error ? "var(--ipe-red)" : "var(--text-muted)"
    }
  }, error || hint));
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Input.jsx", error: String((e && e.message) || e) }); }

// components/surfaces/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * IPE Card — white surface, hairline border, small radius, minimal
 * shadow. Brand identity comes from an optional red top-rule or a
 * mono label, not heavy chrome.
 */
function Card({
  children,
  topRule = false,
  ruleColor = "var(--brand)",
  interactive = false,
  padding = 24,
  style,
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", _extends({
    onMouseEnter: () => interactive && setHover(true),
    onMouseLeave: () => interactive && setHover(false),
    style: {
      background: "var(--surface-card)",
      border: "var(--border-width) solid var(--border)",
      borderTop: topRule ? `3px solid ${ruleColor}` : "var(--border-width) solid var(--border)",
      borderRadius: "var(--radius-md)",
      padding,
      boxShadow: hover ? "var(--shadow-md)" : "var(--shadow-sm)",
      transform: hover ? "translateY(-2px)" : "none",
      transition: "box-shadow var(--dur-base) var(--ease-standard), transform var(--dur-base) var(--ease-standard)",
      cursor: interactive ? "pointer" : "default",
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/surfaces/Card.jsx", error: String((e && e.message) || e) }); }

// components/surfaces/StatCard.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * IPE StatCard — a headline figure set in DM Mono (the brand's
 * data cue) with a label and optional source note.
 */
function StatCard({
  value,
  label,
  source,
  color = "var(--brand)",
  style,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 6,
      padding: "20px 24px",
      background: "var(--surface-card)",
      borderLeft: `4px solid ${color}`,
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("span", {
    style: {
      font: `var(--fw-medium) var(--text-3xl)/1 var(--font-mono)`,
      color,
      letterSpacing: "-0.02em"
    }
  }, value), /*#__PURE__*/React.createElement("span", {
    style: {
      font: "var(--fw-medium) var(--text-base)/1.3 var(--font-sans)",
      color: "var(--text-body)"
    }
  }, label), source && /*#__PURE__*/React.createElement("span", {
    style: {
      font: "var(--fw-regular) var(--text-2xs)/1.3 var(--font-mono)",
      color: "var(--text-muted)",
      letterSpacing: "0.02em"
    }
  }, source));
}
Object.assign(__ds_scope, { StatCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/surfaces/StatCard.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Bullet = __ds_scope.Bullet;

__ds_ns.BulletList = __ds_scope.BulletList;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Logo = __ds_scope.Logo;

__ds_ns.MonoLabel = __ds_scope.MonoLabel;

__ds_ns.Tag = __ds_scope.Tag;

__ds_ns.Callout = __ds_scope.Callout;

__ds_ns.Checkbox = __ds_scope.Checkbox;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.StatCard = __ds_scope.StatCard;

})();
