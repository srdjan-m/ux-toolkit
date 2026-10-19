---
name: spec-driven
description: Language-neutral spec workflow — write what a program does once (requirements, data, flows, input/output examples), then implement or port it to any language on request and verify each implementation against the same examples. Use when the user wants to plan or describe a program before choosing a language, write or review a spec, implement or regenerate code "from the spec", port an implementation to another language, change behaviour across several implementations, or when a spec/ folder with spec.md + examples.yaml exists. Triggers on "spec", "specification", "language-neutral", "language-agnostic", "pseudocode", "implement in <language>", "port to <language>", "same thing in <language>", new_spec.py.
---

# Spec-driven development

A **spec** folder describes *what* a program does without a programming language.
Implementations ("targets") are generated from it and are only correct when every case in
`examples.yaml` passes as a test. The template's own `README.md` (copied into every spec)
defines the neutral type names and pseudocode conventions — read it before writing.

```
spec/
├── README.md        neutral types, pseudocode conventions, request cheat sheet
├── spec.md          purpose · scope · glossary · requirements (R-NNN) · interface · errors · constraints · open questions
├── data.md          entities, fields, invariants, enumerations
├── flows.md         ordered logic and state transitions, in pseudocode
├── examples.yaml    cases E-NNN: covers / call / given / input / expect
└── targets/<lang>.md   per-language how: layout, toolchain, type & error mappings, deviations
```

**The one rule:** the spec owns *what*, a target note owns *how*. Behaviour changes go into
the spec first, then into every target. Never fix behaviour only in code.

## Creating a spec

Scaffold with the toolkit script (it lives at the ux-toolkit repo root, the parent of
this skill's `claude/` folder — find it via the `@` import in `~/.claude/CLAUDE.md`):

```bash
python new_spec.py <name>                       # ./spec/
python new_spec.py <name> --dir <path>/spec --targets python
python new_spec.py <name> --dry-run
```

Where it goes: in a code repo, `spec/` at the root of the thing it describes. In a
ux-toolkit project, beside the source in the dev discipline (`<stage>/01_dev/spec/`).
If several programs share a repo, one spec folder per program.

## Filling it in — interview, don't invent

1. Ask about purpose and users first, then scope and what is explicitly out of scope.
2. Work requirement by requirement. Each one is a single observable behaviour, numbered
   `R-001`…, phrased as *what* happens. Ask for a concrete example of each and write it
   straight into `examples.yaml` — examples surface ambiguity faster than prose.
3. Push for edge cases per requirement: empty, boundary, invalid, duplicate, very large,
   concurrent, missing permission.
4. Anything the user hasn't decided goes into §8 *Open questions*. Never fill a gap with
   your own assumption silently — propose a default and record it as a question.
5. Keep language out: no library names, no language types, no "class"/"async" unless it
   is genuinely part of the behaviour. Use the neutral types from the spec's `README.md`.

Batch questions (a handful at a time), and write answers into the files as you go so the
spec is never only in the conversation.

## Reviewing a spec

Report, most important first:

- requirements with no example in `examples.yaml` (`covers:`), and examples pointing at
  requirement IDs or operations that don't exist;
- error codes used in flows or examples but missing from §6, and vice versa;
- glossary terms used inconsistently, undefined terms, words with two possible readings;
- operations in §5 with no errors listed, or flows that can end without RETURN or FAIL;
- language or library details leaking into the spec;
- unresolved items in §8 that block implementation.

## Implementing a target

1. Read the whole spec. If §8 has open questions that affect this work, ask before coding.
2. Create or read `targets/<lang>.md` (`new_spec.py <name> --dir … --targets <lang>`
   adds one). Fill in location, toolchain, and the mappings for neutral types, error
   codes and operations. Follow the surrounding codebase's conventions where they exist.
3. Turn `examples.yaml` into tests in the target's normal test framework first — one test
   per case, named after its `id` so failures trace back (`test_e_004_…`). Prefer loading
   the YAML at test time over copying values, so a changed example cannot drift from its
   test; fall back to generated tests only where that's awkward.
4. Implement until every example passes. Run the tests; a target is not done until they
   pass, and report honestly if any do not.
5. Record anything that cannot match the spec exactly under *Deviations* in the target
   note, and add a matching item to spec §8.

## Porting to another language

Implement from the **spec**, not by translating the existing code — translation carries
over the first language's idioms and accidental behaviour. Read the other target's notes
only for settled decisions (e.g. how an ambiguity was resolved). Same done-criteria: every
example passes.

## Changing behaviour

1. Update `spec.md` (and `data.md` / `flows.md` if affected).
2. Add or edit cases in `examples.yaml`. Never renumber IDs; mark obsolete cases
   `retired: true` instead of deleting them.
3. Update every target listed in `targets/` and re-run its tests. If a target is not
   updated now, say so and leave a note in its *Deviations* section.

## Keep it proportionate

A small script doesn't need every section — purpose, a few requirements, the interface and
examples are enough; delete empty sections rather than padding them. `flows.md` is only for
logic where order or state matters. Don't propose this workflow for one-off scripts the
user just wants written; offer it when something will live long, be ported, or be built by
several people.
