import * as React from "react";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /** Visual style. @default "primary" */
  variant?: "primary" | "secondary" | "ghost" | "dark";
  /** Control size. @default "md" */
  size?: "sm" | "md" | "lg";
  /** Optional icon node rendered before the label. */
  iconLeft?: React.ReactNode;
  /** Optional icon node rendered after the label. */
  iconRight?: React.ReactNode;
  disabled?: boolean;
  /** Stretch to fill the container width. @default false */
  fullWidth?: boolean;
  children?: React.ReactNode;
}

/**
 * Primary action control for IPE interfaces.
 * @startingPoint section="Core" subtitle="Buttons in every variant and size" viewport="700x180"
 */
export function Button(props: ButtonProps): JSX.Element;
