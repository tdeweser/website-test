import * as React from "react";

export interface CheckboxProps {
  label?: React.ReactNode;
  checked?: boolean;
  onChange?: (checked: boolean) => void;
  disabled?: boolean;
  style?: React.CSSProperties;
}

/** Square checkbox with red fill when selected. */
export function Checkbox(props: CheckboxProps): JSX.Element;
