# S03 — Aisha Karimi, 36, election programmer / ballot definition specialist

**Snapshot:** Works in a mid-sized county elections office (or as vendor services
staff for several counties). Builds each election in the election management system
(EMS): jurisdictions, precincts and splits, districts, contests, candidates, rotation,
ballot styles, translations, audio, and exports to devices.

**Context:** Hard legal deadlines (ballots to print and military/overseas voters weeks
before election day). Last-minute changes: a candidate withdraws, a court order alters
a measure's wording. One mistake can put the wrong contest on thousands of ballots.

**Goals:** Correct ballots for every precinct split, in every language, on deadline;
fast verification that what she built is what was certified.

**Knowledge:** Domain — expert in election law details (rotation, vote-for-N, write-in
rules, ranked choice). Tech — high; power user; spreadsheets, imports, keyboard.

**Language & literacy:** English native; works with translated content she can't read
(Spanish, Chinese, Vietnamese) and must verify structurally.

**Abilities & assistive tech:** None; works 10–12-hour days in peak weeks; dual
monitors.

**Devices & modes:** EMS desktop application, large monitors, keyboard-heavy; proof
PDFs; test decks.

**Behaviours:** Bulk-imports from spreadsheets; wants to edit many records at once;
checks proofs side by side; keeps her own checklist because the tool doesn't.

**What breaks for them:**
- No bulk editing or import validation; errors discovered only at proof stage.
- Dense tables without frozen headers, filters or "N hidden columns" cues (NN/g
  data-tables).
- No diff between versions ("what changed since the certified definition?").
- Translations and audio that can silently fall out of sync with the English text.
- Modal dialogs and confirmations on routine edits (NN/g: confirm only consequential
  actions); irreversible operations without strong confirmation.
- Proofs that don't let her verify every ballot style quickly (style count, contest
  list per style).
- Vague validation messages ("Invalid data in row") instead of row, field and fix.

**Walkthrough tasks:** Import 400 candidates from a spreadsheet with 3 errors; withdraw a
candidate after proofs; add a precinct split; verify all ballot styles contain the
right contests; confirm every Spanish translation exists.

**Recruiting profile:** County or vendor staff who build election definitions (2+
elections). Not in 8.4-A (which covers polling-place tasks) — test separately.
