import * as React from "react";

export interface LogoProps extends React.HTMLAttributes<HTMLSpanElement> {
  /** Base font size in px (the mark scales from this). @default 40 */
  size?: number;
  /** "default" coloured block over plain text, or "inverted" (swapped). @default "default" */
  variant?: "default" | "inverted";
  /** Brand colour of the lock-up. @default brand red */
  color?: string;
}

/**
 * The IPE stacked wordmark, reconstructed in DM Mono.
 * @startingPoint section="Brand" subtitle="The IPE wordmark lock-up" viewport="700x260"
 */
export function Logo(props: LogoProps): JSX.Element;
