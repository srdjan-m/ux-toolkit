# Reports, tables and data-heavy screens

For generated reports, audit/compliance output, dashboards, admin tables and anything
whose job is to tell the reader the state of some data. Here the worst failure isn't
ugliness or friction. It's the **page telling the reader something false**, so
check content truth before style.

Added 2026-11-09 after a review of a third-party licence report. The review found 4 of
126 packages that had no licence badge and appeared in no summary, count or filter.
That was the most serious finding, and it came from cross-checking counts, not from any
visual rule.

## 1. Does the page tell the truth? (check first)

- **Summaries match the rows.** Recount totals, per-status counts and "N need
  attention" banners against the table/source. Count markers (badges, icons, status
  cells) per row: a row with *no* marker is a state the designer didn't foresee.
  A mismatch is a **Blocker** when people sign off on the page (compliance,
  certification, finance), **Major** otherwise.
- **Unknown is a state.** Missing, unparseable or unrecognised values must be shown
  and counted, never silently skipped or shown as the default/OK style.
- **Severity matches meaning.** Things that need different actions (e.g. "text missing"
  vs "value contradicts itself" vs "not identified") shouldn't share one heading or
  colour.
- **Same visual for different risk is a finding.** If every category gets the same badge,
  the reader has to read every row to find the one that matters.

## 2. Do the controls do what they say?

Run filters, search and sort **against the real data with realistic queries**, not
only an empty and an obvious one. Reading the code and reproducing its logic offline
over the page's own data is fine; that's analysis, not building tooling.

- Search scope matches its label. A "filter by licence" box that does substring
  matching over full text matches nearly everything ("mit" → "permitted").
- Every filter combination can reach every state, including "unknown".
- Result counts update and are announced (WCAG 4.1.3). Empty results say why and
  offer a way out.
- In-page links (summary → row) still work when a filter hides the target, and
  don't land under a sticky header (`scroll-margin-top`).
- Filter state survives reload / can be shared if people discuss views.

## 3. Is the vocabulary consistent?

One term per state across header, banner, filter label, row cell and legend. Four
wordings for one state ("missing licence", "without licence text", "text not found"…)
make readers wonder if they're four states.

## 4. Does the output survive its real medium?

If the page is printed, exported to PDF or attached to a submission, **that output
is the deliverable; review it**, not just the screen:

- Columns fit the paper (fixed table layout, widths); no text wrapping one character
  per line, no clipping at the edge.
- Header row repeats; rows don't split across pages; a running footer identifies the
  document, its date/version and "page X of Y".
- Links that only show a domain ("nuget.org") lose their target on paper.
- Meaning doesn't depend on background tints (print dialogs often drop them).
- Repeated boilerplate (identical licence texts, disclaimers) is deduplicated, or page
  count balloons.
- Interactive-only state (collapsed sections, active filters) doesn't hide content in
  print.

## 5. Traceability (audit / compliance artefacts)

Can a reviewer tie the page back to its source: what was scanned (repo, commit,
version), when, by which tool and version, and integrity data (hashes) where they
exist? Missing provenance is Minor on a dashboard and Major on a certification
artefact.
