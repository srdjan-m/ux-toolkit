# Content and microcopy — review checklist

Words are part of the design. Read every string on the screen, in order, as the user
would. For voting, the plain-language rules are a requirement (VVSG 7.3-P, 7.3-K) —
legally required text is the only exception.

## 1. Plain language (VVSG 7.3-P; also general best practice)

- Common words, not system or legal jargon. "There are more contests on the other side"
  — not "Additional contests are presented on the reverse."
- Tell people **what to do**, not what not to do. "Fill in the oval for your write-in
  vote to count" — not "If the oval is not marked, your write-in vote cannot be counted."
- Address the user directly, **active voice**. "Remove and keep this stub" — not "This
  stub must be removed and retained by the voter."
- **Condition first**, then action: "To change your vote, select another candidate."
- No gendered pronouns: "your candidate's name", not "his name".
- One idea per sentence; one step per line (VVSG 7.3-K: separate each instruction step
  spatially).
- Reading level *(guideline)*: aim for US grade 6–8 for public-facing text.

## 2. Buttons and labels

- Buttons say the **action and object**: "Print ballot", "Save changes" — not "OK",
  "Submit", "Yes". A dialog's buttons should make sense without reading the dialog.
- Same action → same word everywhere (WCAG 3.2.4, H4).
- Labels are visible, short, and above or beside the field; not placeholder-only.
- Headings describe the content (WCAG 2.4.6) — "Review your choices", not "Step 4".
- Links describe the destination; no "click here" / "learn more" alone.

## 3. Messages: errors, warnings, confirmations

Every warning or error says (VVSG 7.3-K, WCAG 3.3.1/3.3.3, H9):
1. **What happened**, in the user's words.
2. **Whose problem it is** — something the user did, or a system fault.
3. **What to do now** — the specific next step or the available choices.

| Bad | Good |
|---|---|
| "System detects imminent timeout condition." | "Do you need more time? Select 'Yes' or 'No'." |
| "Invalid input." | "Enter your ZIP code as 5 digits, like 80202." |
| "Error 503." | "We couldn't save your changes because the connection dropped. Try again." |

- Error text sits next to the problem, not only in a banner at the top.
- Confirmations of serious actions state the consequence: "Cast your ballot? You can't
  change it after this."
- Success messages are real: never claim success before it's confirmed (VVSG 7.3-J
  calls a false success notice a violation).
- Tone: calm, specific, no blame, no jokes in errors.

## 4. Empty, loading and edge states

- Empty states explain why it's empty and what to do next.
- Loading states say what is loading if it takes more than ~1 s.
- Undervote/"no selection" states are neutral, not alarming — the voter may skip a
  contest on purpose (VVSG 7.3-I: they can submit an undervoted ballot).

## 5. Language and translation

- Every string is translatable — no text baked into images.
- Layout tolerates ~30 % longer text (Spanish, German) and right-to-left scripts if
  supported.
- Language selector shows each language's **native name** and stays visible on voting
  screens (VVSG 7.3-M).
- Warnings, instructions and over/undervote notices exist in every supported language
  (VVSG 5.2-B). A mock with an English-only warning in a Spanish flow is a finding.
