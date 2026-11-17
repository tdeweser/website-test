import * as React from "react";

export interface MonoLabelProps extends React.HTMLAttributes<HTMLSpanElement> {
  /** Text colour. @default brand red */
  color?: string;
  /** Show a leading red square. @default false */
  bullet?: boolean;
  children?: React.ReactNode;
}

/** Small uppercase DM Mono eyebrow / data label. */
export function MonoLabel(props: MonoLabelProps): JSX.Element;
