# NN/g guidance: patterns, feedback and content

Nielsen Norman Group recommendations, gathered 2026-11-09 from the pages linked under
each heading (all URLs confirmed then). Bullets are close paraphrases, not NN/g's exact
wording, except text in quotes. Check a figure on the live page before quoting it to a
client. `[interp]` marks our reading, not NN/g's statement.

The 10 heuristics as review questions are in ux-review's `heuristics.md`; design to them.
[ten-usability-heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)

## Familiar patterns and memory

[mental-models](https://www.nngroup.com/articles/mental-models/) ·
[recognition-and-recall](https://www.nngroup.com/articles/recognition-and-recall/) ·
[Jakob's law (video)](https://www.nngroup.com/videos/jakobs-law-internet-ux/) ·
[Hick's law (video)](https://www.nngroup.com/videos/hicks-law-long-menus/)
- Jakob's law: "Users spend most of their time on other sites" — design with patterns
  they already know. Innovate only where the new way is clearly better.
- Fit the design to users' shared mental model; where the system can't change, fix the
  model with clearer labels and short contextual help. A distinction users won't grasp
  may not be worth keeping.
- Recognition over recall: keep options and information visible; show recent items and
  saved lists; visible menus over typed commands; search suggestions; label icons, at
  least early on.
- Hick's law: more choices → slower decisions. Shorten and group option lists.

## Forms

[web-form-design](https://www.nngroup.com/articles/web-form-design/) ·
[form-design-placeholders](https://www.nngroup.com/articles/form-design-placeholders/) ·
[required-fields](https://www.nngroup.com/articles/required-fields/) ·
[errors-forms-design-guidelines](https://www.nngroup.com/articles/errors-forms-design-guidelines/)
- Fewest fields possible: drop, derive or defer anything you can.
- **One column.** Exception: short related fields (city / state / ZIP) on one row.
- Labels outside and close to the field; group related fields under section labels.
- **No placeholder text as a label or for essential hints**: it disappears on typing,
  looks like a filled value, usually fails contrast and is skipped by some screen
  readers. Hints go outside the field. Floating labels beat placeholders but still look
  pre-filled; outside labels are best when space allows.
- Mark **every** required field: asterisk *before* the label (scannable down the left
  edge) in a contrasting colour, or the word "Required" on long forms; plus markup so
  screen readers announce it. Not "all fields required" as a single note. A plain
  username/password login may skip markers.
- Keep optional fields to one or two and label them "optional".
- Match the control to the input: radio buttons, not a dropdown, for 2–3 options; size
  text fields to the expected answer.
- State format and password rules **before** input, not only in the error.
- No Reset/Clear buttons. A low-key Cancel is fine on sensitive forms.
- Inline validation fires when the user **leaves** a field, not while typing; error next
  to the field. Success marks only for complex inputs (username availability, new
  password strength).

## Errors

[error-message-guidelines](https://www.nngroup.com/articles/error-message-guidelines/) ·
[indicators-validations-notifications](https://www.nngroup.com/articles/indicators-validations-notifications/)
- Next to the cause; visible by more than colour or animation alone.
- Severity sets the treatment: subtle inline for minor issues, modal only for serious.
- Plain language naming the specific problem; error codes only when needed for support.
- Say how to fix it. Neutral tone — no blame, no jokes. Apologise for system failures.
- Keep the user's input; offer likely corrections; catch predictable mistakes before
  submit (e.g. "you mentioned an attachment but didn't attach one").
- **Never put errors in toasts** — they fade and get missed.

## Feedback, waiting and status

[response-times-3-important-limits](https://www.nngroup.com/articles/response-times-3-important-limits/) ·
[progress-indicators](https://www.nngroup.com/articles/progress-indicators/) ·
[skeleton-screens](https://www.nngroup.com/articles/skeleton-screens/) ·
[empty-state-interface-design](https://www.nngroup.com/articles/empty-state-interface-design/)

| Wait | Show |
|---|---|
| < 0.1 s | Nothing; it feels instant. |
| 0.1–1 s | Nothing special; flow is kept. Acknowledge the press (pressed state) at once. |
| ~1–10 s | Spinner/looped animation **with text saying what's happening**; skeleton for a full-page load. |
| > 10 s | Percent-done bar with a (padded) time estimate and a way to cancel. Series work: "Updating 3 of 50". |

- Spinner for one module, skeleton for a page (static, not shimmering — animation
  distracts and can be an accessibility problem), progress bar for uploads/exports.
  Header-and-footer-only skeletons are no better than a spinner.
- No static "Loading…" text, no "don't click twice" warnings.
- **Empty states** must say which it is — truly empty, still loading, or failed (never
  "No records" while loading) — explain the feature and give a direct first action.
- Passive information → indicators, badges, non-modal popovers. Modal notification only
  when urgent and a response is required. Every notification makes sense on its own.

## Navigation and finding

[menu-design](https://www.nngroup.com/articles/menu-design/) ·
[breadcrumbs](https://www.nngroup.com/articles/breadcrumbs/) ·
[information-scent](https://www.nngroup.com/articles/information-scent/) ·
[filters-vs-facets](https://www.nngroup.com/articles/filters-vs-facets/) ·
[infinite-scrolling-tips](https://www.nngroup.com/articles/infinite-scrolling-tips/)
- Desktop: visible navigation, not a hamburger. Show where the user is.
- Menu labels clear, specific, familiar, front-loaded; icons may support labels, never
  replace them. Carets on items with submenus; submenus open on **click**, not hover.
  No multi-level cascading menus — use mega menus or landing pages.
- Breadcrumbs show the place in the hierarchy (not the path taken), start at Home, end
  with the current page as unlinked text; skip them on 1–2-level or linear sites. On
  mobile show only the last 1–2 levels without shrinking targets.
- Information scent: every link label predicts its destination; no "More" / "Learn
  more"; users' vocabulary, not internal names; labels work out of context.
- Filters only on dimensions users actually care about; a simple filter often beats a
  full faceted system.
- Infinite scroll only for aimless browsing. For finding, comparing or "top results"
  use pagination or **Load more** (keeps the footer reachable). Restore scroll position
  on Back.

## Complexity: progressive disclosure, wizards, defaults, onboarding

[progressive-disclosure](https://www.nngroup.com/articles/progressive-disclosure/) ·
[wizards](https://www.nngroup.com/articles/wizards/) ·
[the-power-of-defaults](https://www.nngroup.com/articles/the-power-of-defaults/) ·
[onboarding-tutorials](https://www.nngroup.com/articles/onboarding-tutorials/) ·
[mobile-tutorials](https://www.nngroup.com/articles/mobile-tutorials/) ·
[mobile-app-onboarding](https://www.nngroup.com/articles/mobile-app-onboarding/)
- Progressive disclosure: **at most 2 levels**. Frequent needs on the first display;
  the "more" control clearly labelled with what it reveals. Decide the split from usage
  data, not guesses.
- Wizards for novices or rare tasks, with a fast path for experts. Show all steps and
  the current one; order is fixed (if users need any order, it's not a wizard); buttons
  name the destination ("Continue to Billing"); save and resume; each step
  self-sufficient; help in a side panel, not an overlay.
- Defaults are powerful (top search result: 42 % of clicks vs 8 % for the second):
  pre-fill the common value, choose defaults deliberately, never a manipulative one.
- Avoid up-front tutorials: in NN/g's study they didn't raise success and made apps
  feel harder. Fix the interface first; prefer contextual "pull" help at the moment of
  need; keep any tutorial re-findable.

## Destructive actions and control

[confirmation-dialog](https://www.nngroup.com/articles/confirmation-dialog/) ·
[user-control-and-freedom](https://www.nngroup.com/articles/user-control-and-freedom/)
- Prefer **undo** to confirmation. Confirm only serious or irreversible actions —
  routine confirmations get clicked through.
- Confirmation text restates what will happen to which items; buttons name outcomes
  ("Delete 3 files" / "Keep files"), not Yes/No/OK; often no default button.
- Extreme cases: a deliberate extra step (type the name). Use rarely.
- Every multi-step task has a visible Cancel; offer to keep a draft. Back goes one step
  and must not break; Back closes a full-screen overlay.
- Undo messages stay long enough to act on.

## Writing: reading behaviour, labels, plain language

[f-shaped-pattern](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/) ·
[how-people-read-online](https://www.nngroup.com/articles/how-people-read-online/) ·
[inverted-pyramid](https://www.nngroup.com/articles/inverted-pyramid/) ·
[plain-language-experts](https://www.nngroup.com/articles/plain-language-experts/) ·
[writing-links](https://www.nngroup.com/articles/writing-links/) ·
[ui-copy](https://www.nngroup.com/articles/ui-copy/) ·
[microcontent](https://www.nngroup.com/articles/microcontent-how-to-write-headlines-page-titles-and-subject-lines/)
- People scan. Most important content in the first two paragraphs; headings clearly
  stronger than body; **first two words** of headings, links and list items carry the
  meaning; bullets; selective bold; short chunks.
- Inverted pyramid: conclusion first, then details from broad to niche.
- Plain language even for experts: ~15–20-word sentences, one idea per paragraph;
  reading level grades 6–8 for the public, 10–12 for experts; jargon only if the
  audience shares it.
- Links: visibly links; text predicts the destination (never "click here" / "read
  more"); same text → same destination; mark file types (PDF).
- Commands: 2–4 words, specific verbs ("Discard", not "OK"); "…" when more input
  follows; label the resulting state ("Pause" while playing); add the noun when
  ambiguous ("Delete Folder"); no cute or branded terms.
- Page titles ~40–60 characters, keywords first.
