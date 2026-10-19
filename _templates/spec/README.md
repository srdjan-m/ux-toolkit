# {{name}} — spec

A language-neutral description of **{{name}}**. Implementations in any language are
generated from these files and verified against `examples.yaml`.

| File | Holds | Answers |
|---|---|---|
| `spec.md` | purpose, scope, requirements, interface, errors, constraints | *what* it must do |
| `data.md` | entities, fields, invariants, enumerations | *what* it works with |
| `flows.md` | step-by-step logic, states and transitions | *in what order* |
| `examples.yaml` | concrete input → expected output cases | *how we know it works* |
| `targets/<lang>.md` | per-language decisions: layout, toolchain, mappings | *how*, in one language |

**The rule:** the spec says *what*, a target note says *how*. Change the spec first,
then regenerate the implementations — never fix behaviour only in code.

---

## Neutral types

Use these names in `data.md` and `spec.md` §5 so no language leaks into the spec.

| Type | Meaning |
|---|---|
| `text` | Unicode string |
| `integer` | whole number; state the range if it matters |
| `decimal` | exact decimal (money, measurements) — not a float |
| `number` | floating point, where approximation is acceptable |
| `boolean` | true / false |
| `date`, `time`, `datetime` | calendar values; `datetime` always states its timezone rule |
| `duration` | length of time |
| `bytes` | raw binary data |
| `list<T>` | ordered, may repeat |
| `set<T>` | unordered, no repeats |
| `map<K, V>` | key → value lookup |
| `optional<T>` | may be absent — say what absence means |
| `enum EnumName` | one of a closed set, defined in `data.md` |
| `EntityName` | a record defined in `data.md` |

## Pseudocode conventions

For `flows.md`. Capitals are keywords; everything else is plain English.

```
SET total TO 0
FOR EACH item IN order.items
    IF item.quantity < 1 THEN FAIL INVALID_QUANTITY
    ADD item.price * item.quantity TO total
END
WHILE condition ... END
CALL other_operation WITH field: value
RETURN total
```

- `FAIL CODE` raises an error code from `spec.md` §6 — never invent codes in a flow.
- Refer to requirements inline as `(R-003)` where a step implements one.
- Say *what* a step achieves, not which library does it ("sort by date, newest first",
  not "call sorted() with a lambda").

---

## Working with Claude Code

The `spec-driven` skill knows this layout. Typical requests:

| Goal | Ask |
|---|---|
| Write the spec | "Interview me and fill in the spec for {{name}}." |
| Review it | "Review the spec for gaps, ambiguity and requirements without examples." |
| First implementation | "Implement the spec in Python. Turn examples.yaml into tests." |
| Another language | "Implement the same spec in TypeScript." |
| Change behaviour | "R-004 should also … — update the spec, then every target." |
| Check a target | "Does the Python target still match the spec? Run the examples." |

A target is finished when **every case in `examples.yaml` passes** as a test in that
language, and its `targets/<lang>.md` lists any deviations.
