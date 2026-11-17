import * as React from "react";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  /** Mono uppercase field label. */
  label?: React.ReactNode;
  /** Helper text below the field. */
  hint?: React.ReactNode;
  /** Error message (overrides hint, turns the field red). */
  error?: React.ReactNode;
}

/** Single-line text field with mono label and aqua focus ring. */
export function Input(props: InputProps): JSX.Element;
