import * as React from "react";

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Show a 3px brand-colour top rule. @default false */
  topRule?: boolean;
  /** Colour of the top rule. @default brand red */
  ruleColor?: string;
  /** Lift on hover. @default false */
  interactive?: boolean;
  /** Inner padding in px. @default 24 */
  padding?: number;
  children?: React.ReactNode;
}

/** White content surface with hairline border and minimal shadow. */
export function Card(props: CardProps): JSX.Element;
