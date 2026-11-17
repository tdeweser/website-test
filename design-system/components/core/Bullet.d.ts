import * as React from "react";

export interface BulletProps extends React.HTMLAttributes<HTMLSpanElement> {
  /** Square size in px. @default 10 */
  size?: number;
  /** Marker colour (any CSS colour / token). @default brand red */
  color?: string;
}

export interface BulletListProps extends React.HTMLAttributes<HTMLUListElement> {
  items?: React.ReactNode[];
  color?: string;
  /** Row gap in px. @default 10 */
  gap?: number;
}

/** The signature red-square list marker. */
export function Bullet(props: BulletProps): JSX.Element;
/** A list using the red-square marker. */
export function BulletList(props: BulletListProps): JSX.Element;
