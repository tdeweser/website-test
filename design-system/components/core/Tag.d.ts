import * as React from "react";

export interface TagProps extends React.HTMLAttributes<HTMLSpanElement> {
  /** Accent colour. @default "red" */
  color?: "red" | "aqua" | "green" | "blue" | "gray";
  /** Solid fill instead of tint. @default false */
  solid?: boolean;
  children?: React.ReactNode;
}

/** Pill chip for topics, categories and filters. */
export function Tag(props: TagProps): JSX.Element;
