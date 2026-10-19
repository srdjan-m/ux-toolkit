# {{name}} — flows

> How the behaviour unfolds step by step: the parts where *order* or *state* matters.
> Simple operations don't need a flow — the requirement and the examples are enough.
> Use the pseudocode conventions in `README.md`.

## Flow: `flow_name`

**Trigger:** what starts it
**Covers:** R-001

```
1. ...
2. IF condition THEN
       ...
   ELSE
       FAIL ERROR_CODE
3. RETURN result
```

## States

> Only if something has modes or a lifecycle. List the states, then every allowed
> transition — anything not listed is forbidden.

| From | Event | To | Notes |
|---|---|---|---|
| | | | |
