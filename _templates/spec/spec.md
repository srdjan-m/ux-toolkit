# {{name}} — specification

_Created {{date}} · {{author}} · status: draft_

> This spec is the source of truth. Every implementation in `targets/` is generated from
> it and checked against `examples.yaml`. **Change this file first**, then regenerate.
> Lines starting with `>` are guidance — delete them as you fill each section.

## 1. Purpose

> One paragraph: what problem this solves, for whom, and what "done" looks like.

## 2. Scope

**In scope**

-

**Out of scope** (decided, not forgotten)

-

## 3. Glossary

> Every domain word used below, defined once. If two people could read a word
> differently, it belongs here.

| Term | Meaning |
|---|---|
| | |

## 4. Requirements

> One observable behaviour per line, numbered so examples and code can point at them.
> Write *what* happens, never *how*. Use MUST for required, SHOULD for preferred.

| ID | Requirement |
|---|---|
| R-001 | |

## 5. Interface

> The operations the outside world can call — functions, CLI commands, API endpoints or
> UI actions. Types use the neutral vocabulary in `README.md`. Each operation lists the
> errors it can produce; codes are defined in §6.

### `operation_name`

- **Input:** `field: type` — meaning
- **Output:** `type` — meaning
- **Errors:** `ERROR_CODE`
- **Covers:** R-001

## 6. Errors

> Language-neutral error codes. Each target maps them to its own mechanism (exceptions,
> result types, exit codes, HTTP statuses) in `targets/<lang>.md`.

| Code | When | Message for the user |
|---|---|---|
| | | |

## 7. Constraints

> Non-functional limits that hold in every language: performance, size, platforms,
> security, accessibility, offline use, dependencies allowed.

-

## 8. Open questions

> Anything undecided. Implementation must not silently pick an answer — resolve it here
> first, then move the decision into the relevant section.

- [ ]
