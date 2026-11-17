Square checkbox with a red fill and white tick when selected.

```jsx
const [on, setOn] = React.useState(false);
<Checkbox label="Ik ga akkoord" checked={on} onChange={setOn} />
```

Controlled: pass `checked` and an `onChange(next)` handler.
