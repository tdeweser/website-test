import * as React from "react";

export interface StatCardProps extends React.HTMLAttributes<HTMLDivElement> {
  /** The headline figure (string so units/% are preserved). */
  value: React.ReactNode;
  /** Short description of the figure. */
  label: React.ReactNode;
  /** Optional source / footnote line. */
  source?: React.ReactNode;
  /** Accent colour for the figure + left rule. @default brand red */
  color?: string;
}

/** A headline data figure in DM Mono with a label and source note. */
export function StatCard(props: StatCardProps): JSX.Element;
