# Voting systems — VVSG 2.0 checks a designer can verify

Source: *Voluntary Voting System Guidelines 2.0 — Requirements*, EAC, adopted
February 10, 2021, Principles 5–8. Numbers below are quoted from that text. Cite the
requirement ID in every finding. Only design-checkable rules are listed — hardware
certification, security and audit requirements are out of scope for a design review.

VVSG 2.0 is **stricter than WCAG** in several places (contrast 10:1, touch targets
12.7 mm). When both apply, the stricter one wins. 8.2-A also requires Section 508 and
WCAG 2.0 AA for every electronic interface, including the election management system.

Physical sizes are in **mm on the real device**. A screenshot alone can't prove them —
use `scripts/ux_measure.py size` with the display's diagonal and resolution, and state
the display you assumed. VVSG 8.1-A: a primary voting display is at least 12" and
1920×1080; a message display for voters/poll workers at least 7.9" and 1024×768.

## Contents

1. Visual presentation (7.1)
2. Controls and interaction (7.2)
3. Understandable information (7.3)
4. Equivalence, languages, privacy (5, 6)
5. Paper ballots and records
6. Audio — what to look for in a flow

---

## 1. Visual presentation (7.1)

| ID | Check | Exact rule |
|---|---|---|
| 7.1-C | Default contrast | **≥ 10:1** for every element that conveys information: text, controls, icons, the outline of the marking target, a broken arrow. Decorative-only elements are exempt. |
| 7.1-D | Contrast options exist | High contrast: white bg / dark text **≥ 20:1**; black bg (#000000–#111111) with yellow ~#FFFF00 **≥ 17.5:1**, cyan ~#00FFFF **≥ 15:1**, white ~#FAFAFA **≥ 18:1**. Low contrast option **4.5:1 – 8:1**. Options apply to the whole screen, decorative elements included. |
| 7.1-E | Colour conventions | Green / blue / white = information or normal status. Amber / yellow = warning or marginal. Red = error or needs immediate attention. Flag any inversion (e.g. green "Cast ballot" fine; red used for a neutral action is not). |
| 7.1-F | Not colour alone | Colour is never the only way to show information, an action, a prompt, a distinction or feedback. Selection must also show shape, text, or a mark. |
| 7.1-G | Text size (screen) | Default **≥ 4.8 mm**, measured as the height of an uppercase **I**. Voter can make text bigger *and* smaller. Either continuous scaling in ≤ 0.5 mm steps across **3.5–9.0 mm**, or **≥ 4 discrete sizes** where main ballot options fall in 3.5–4.2 / 4.8–5.6 / 6.4–7.1 / 8.5–9.0 mm. |
| 7.1-H | Scaling | Icons, titles, buttons and marking targets scale with the text. Up to 200 % (7.1 mm) → **no horizontal scrolling or panning**. Above 200 % horizontal panning is allowed if it keeps options next to their targets. |
| 7.1-J | Sans-serif | Voter-facing text can be shown in a sans-serif font. |
| 7.1-P | Distinguishable controls | Buttons with different navigation/selection functions differ in **both shape and colour** (on screen, shape includes the label). Groups may share a colour (e.g. volume up/down). |
| 7.1-A/B | Reset | Settings reset to default when the session ends; the voter can restore defaults mid-session **without losing votes**. Check a "Reset settings" control exists and its copy says votes are kept. |

## 2. Controls and interaction (7.2)

| ID | Check | Exact rule |
|---|---|---|
| 7.2-B | Contest navigation | Voter can go to the next **and previous** contest before finishing — not forced to go through every contest first. |
| 7.2-C | Voter control of selections | Vote-for-1: selecting another candidate may switch the vote, but the change must be **announced visually and in audio**. Vote-for-N: the system **never deselects automatically**; on too many selections it tells the voter and offers a way to change. Straight-party: clear feedback on what was selected. Ranked choice: never re-order candidates except on the voter's explicit command. |
| 7.2-D | Long contests | If a contest doesn't fit on one screen (at the voter's text size): paginate or scroll, with a **fixed header or footer** that always shows navigation, the contest name and its voting rule; **easily perceivable "more options" cues**; not only platform scroll bars; controls labelled with words or symbols; review/correct before leaving the contest. |
| 7.2-E | Gestures | Optional extra only, consistent everywhere, never navigate off the contest, simple and well known, **no double-tap, multi-finger, long-press or timed gestures**. |
| 7.2-H | Accidental activation | Nothing in easy-to-bump spots (e.g. bottom-left corner where people hold the unit). Activate on release ("up event") or confirm. |
| 7.2-I | Touch targets | **≥ 12.7 mm × 12.7 mm**, **≥ 2.54 mm apart**, no overlap. Much larger than mobile guidelines — check every button, checkbox and option row. |
| 7.2-M | No repeat on hold | Holding a key/button acts once (e.g. one "e" in a write-in). |
| 7.2-N | Response time | Visual response to any action ≤ **0.1 s**; audio ≤ 0.5 s; marking a vote ≤ 1 s; screen complete ≤ 1 s or show a "working" indicator. Design must include that indicator. |
| 7.2-O | Inactivity | After a documented 2–5 min of inactivity, show an alert offering more time; alert lasts **20–45 s**; then the session goes inactive and needs a poll worker. Design the alert with plain-language copy (see 7.3-K). |

## 3. Understandable information (7.3)

| ID | Check | Exact rule |
|---|---|---|
| 7.3-B | No split contests | A contest is never split across two columns, two pages, or visually into two groups. Strong evidence this causes overvotes and missed candidates. |
| 7.3-C | Contest header, in this order | 1) office/question title with distinguishing info (term, jurisdiction); 2) maximum selections allowed; 3) (audio only) number of options; 4) selections **remaining**, once any are made; 5) (audio only) current selections; 6) instructions or where to find them — **last**. |
| 7.3-D | Consistent marking relationship | The marking target is in the same spatial position relative to the name throughout the ballot for each contest type — never left of some names and right of others. |
| 7.3-E | Feedback | Unambiguous confirmation of each selection (check mark, clear state change). Audio phrases must sound different at top speed — "selected" vs "deselected" is a known trap. |
| 7.3-F | Correcting | Voter can change a vote within a contest before moving on, and correct the ballot before it's cast or printed, without help. |
| 7.3-G | Review screen | Shows **every** contest with: the selections, or "no selection made", or "fewer selections than allowed". Lets the voter jump to a contest, change it, and **return straight to the review screen**. Lets the voter continue to cast at any time without correcting. |
| 7.3-H | Overvotes | Electronic interfaces **must prevent** overvotes (not just warn). Scanners identify the specific overvoted contests, visually plus audio or sound. |
| 7.3-I | Undervotes | Notify the **specific contest** visually and in audio; the voter **can still submit** an undervoted ballot. |
| 7.3-J | Cast confirmation | Tell the voter, visually and in audio, whether the ballot was cast **successfully or not**; on failure, give clear next steps. A false success message is a violation. |
| 7.3-K | Warnings and alerts | Visually distinct from other information. In plain language they state: what the problem is; whether it's the **voter's action or a system fault**; what the voter can do. Each instruction step separated spatially (and by a pause in audio). Good: "Do you need more time? Select 'Yes' or 'No'." Bad: "System detects imminent timeout condition." |
| 7.3-L | Icon labels | Every meaningful icon has a text label. (Only exception: the headset and wheelchair icons on audio/PAT jacks.) |
| 7.3-M | Language switch | Language control **visible on screen at all times**, not inside help or settings; each language listed by its **native name** (e.g. "Español", "中文"), optionally also in English. |
| 7.3-N | Help | Voter can get help from the system at any point; situation-specific instructions sit **near where they're needed**, only general ones at the start. |
| 7.3-P | Plain language | Common words ("There are more contests on the other side", not "Additional contests are presented on the reverse"); say what to do, not what not to do; address the voter directly, active voice; **condition first**, then action ("To change your vote, do X"); no gendered pronouns. Legally required text is exempt. Also applies to poll-worker messages. |
| 7.3-O | Poll-worker screens | Setup / polling / shutdown messages understandable by non-experts and let them verify the machine is set up, working, and shut down correctly. |

## 4. Equivalence, languages, privacy (Principles 5 and 6)

- **5.2-A No bias** — every candidate/option gets identical treatment: same text size,
  weight, colour, spacing, target size, audio volume and rate. Order and write-in rules
  come from state law. Flag *any* visual difference between options (one name bolder,
  one row taller, a photo for some candidates only).
- **5.1-A / 7.2-A Modes** — visual, enhanced visual, audio, touch and limited-dexterity
  modes all support the full flow (instructions, navigation, write-ins, changing votes,
  final submission). If a design adds a feature, ask how it works in audio-only and
  with a two-switch input.
- **5.2-B / 5.2-C** — every instruction, warning and over/undervote notice exists in all
  supported languages and in all modes. Hard-coded English in a mock is a finding.
- **5.2-E Sound + visual cues** — every sound cue has a visual cue and vice versa (unless
  the voter chose audio-only / visual-only).
- **5.2-F Preserving votes** — changing language, text size, contrast or audio settings
  mid-session keeps all votes, the navigation position and screen position.
- **5.1-C** — any paper record is auditable by English-only readers (at least the
  contest option, e.g. "Yes / No", is in English).
- **6.1-B Private warnings** — warnings (overvote etc.) never reveal selections to
  bystanders: no loud audio through speakers, no huge red banner naming the candidate.
- **6.1-C** — voter can turn audio or the screen off independently and is told it changed.

## 5. Paper ballots and records

| ID | Rule |
|---|---|
| 7.1-C | Contrast ≥ 10:1 at ≥ 300 lx ambient light. |
| 7.1-I | Font ≥ **3.5 mm (10 pt)**. Large-print option, if offered: 6.4–7.1 mm. |
| 7.2-J | Hand-marked target (oval/box) **≥ 3 mm across** in every direction. |
| 7.3-B | No contest split across columns or pages. |
| 7.3-D | Target on the same side of every name in a contest type. |
| 7.3-N | Ballot can carry text **and images** explaining how to mark it; instructions near where needed. |
| 7.3-H | Overvote effect explained in instructions on the ballot. |
| 7.3-F | Instructions say how to correct a mistake (e.g. ask for a new ballot). |

## 6. Audio — what to look for in a flow

You usually review screens, but audio requirements change what a screen must *contain*:

- 7.2-G: voter can pause/resume, repeat, skip to next/previous contest, skip the reading
  of a ballot question — the flow needs these commands.
- 7.1-K: default 60–70 dB SPL, adjustable 20–100 dB in ≤ 10 dB steps; speech rate
  default 120–125 wpm, 6–8 steps from ~60–70 to ~240–250 wpm — check the settings
  screen offers these ranges and steps.
- 7.3-C items 3 and 5 are audio-only: the script announces how many options exist and
  what's already selected.
- Say in "Not checked" that audio quality itself (7.1-L, 7.1-M) can't be judged from a
  design.
