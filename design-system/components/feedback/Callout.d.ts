import * as React from "react";

export interface CalloutProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Optional bold heading line. */
  title?: React.ReactNode;
  /** Colour tone. @default "neutral" */
  tone?: "neutral" | "brand" | "info" | "positive";
  children?: React.ReactNode;
}

/** Flat note block with an accent left rule — source notes, takeaways, alerts. */
export function Callout(props: CalloutProps): JSX.Element;
