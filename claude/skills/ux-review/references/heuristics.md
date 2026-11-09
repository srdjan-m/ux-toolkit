# Usability heuristics — Nielsen's 10, as check questions

Source: Jakob Nielsen, *10 Usability Heuristics for User Interface Design* (1994,
updated 2020, nngroup.com). Cite as "H1"…"H10". Ask each question of the screen *and*
of the flow around it — many problems only show between screens.

| # | Heuristic | Ask | Typical findings |
|---|---|---|---|
| H1 | Visibility of system status | After every action, can the user tell it worked? Is there a loading state, progress for multi-step tasks, a "you are here"? | No feedback after save; spinner with no context; step 3 of ? |
| H2 | Match the real world | Are words, icons and order the user's, not the system's? | Internal jargon, database field names, error codes as messages. |
| H3 | User control and freedom | Is there a clearly marked way back, cancel, undo? Can the user leave without losing work? | Modal with no close; destructive action with no undo; wizard without "Back". |
| H4 | Consistency and standards | Does the same thing look and behave the same everywhere — and match platform conventions? | Two button styles for primary; "Delete" red here, grey there. |
| H5 | Error prevention | Does the design stop errors before they happen (constraints, defaults, confirmations for destructive actions)? | Free-text date field; "Delete all" next to "Save". |
| H6 | Recognition rather than recall | Are options, previous inputs and needed info visible instead of remembered? | Codes the user must remember from a previous screen; icon-only toolbars. |
| H7 | Flexibility and efficiency | Do frequent users have shortcuts (bulk actions, keyboard, saved filters) without cluttering for novices? | Repeating a 5-step task one item at a time. |
| H8 | Aesthetic and minimalist design | Does every element earn its place? Is the most important thing the most prominent? | Competing primary actions; decorative noise; dense paragraphs. |
| H9 | Recognise, diagnose, recover from errors | Do error messages say what happened, in plain words, and how to fix it — next to the problem? | "Error 0x80004005"; error banner at top, field at bottom. |
| H10 | Help and documentation | Is help available in context, at the moment it's needed, and task-focused? | Help only in a separate manual; tooltip that repeats the label. |

## How to use them well

- Pair each finding with **the user's task** that it blocks — "H5 violation" alone
  teaches nothing; "a voter can select a second candidate in a vote-for-1 contest
  without being told the first was removed (H1, VVSG 7.2-C)" does.
- Heuristics find problems; they don't rank them. Rank with the SKILL.md severity scale.
- Three to five independent evaluators find ~75 % of problems; one finds ~35 %. Say in
  the summary that a single review is not a usability test (VVSG 8.3-A requires real
  voter testing for voting systems).
