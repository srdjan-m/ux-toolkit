---
name: ux-personas
description: Election-system personas — voters with different civic knowledge, languages, literacy and disabilities (including overseas/military remote voters), plus poll workers, election programmers, administrators, adjudicators, L&A testers, auditors, poll watchers, vendor help desk and certification (VSTL) test engineers — for persona-based walkthroughs of a design and for recruiting real usability-test participants (VVSG 2.0 8.3-A / 8.4-A). Use when asked to test or walk through a UI "as" a user, check a design against personas, pick personas for a screen, plan a usability test or write a recruiting screener. Used by the ux-critic and ux-designer agents. Triggers on "persona", "personas", "walk through as", "cognitive walkthrough", "usability test", "recruit", "participants", "voter types", "poll worker", "election programmer".
---

# UX personas (election systems)

Personas make "the user" specific enough to test against. Here each one is a **testing
instrument**: concrete abilities, knowledge, devices and language, plus the design
failures most likely to stop them. They're fictional composites — no real people.

**They don't replace real participants.** VVSG 2.0 8.3-A requires usability tests with
real voters (native speakers of every supported language; blind voters on audio +
tactile; low-vision voters on enhanced visual, with and without audio; limited-dexterity
voters on low/no-dexterity controls), and 8.4-A with real election workers of varied
experience. Personas catch problems before those tests and tell you whom to recruit;
each file ends with a recruiting profile.

## Roster

Voters — `personas/voters/`

| ID | Persona | Mode / key trait | 8.3-A group |
|---|---|---|---|
| V01 | Jordan, 19, first-time voter | Visual; phone-native, low civic knowledge | General |
| V02 | Dorothy, 78, low vision (AMD) | Enhanced visual: large text, high contrast | Low vision |
| V03 | Marcus, 41, blind | Audio + tactile keypad, braille, expert screen-reader user | Blind |
| V04 | Priya, 34, quadriplegia | Two-switch / sip-and-puff, wheelchair | Limited dexterity |
| V05 | Walter, 71, essential tremor + arthritis | Touch, frequent mis-taps, can't drag | Limited dexterity |
| V06 | Lucía, 46, Spanish-dominant | Visual in Spanish; limited English reading | Native speaker (es) |
| V07 | Wei, 68, Mandarin-dominant | Visual in Chinese; non-Latin script, name order | Native speaker (zh) |
| V08 | Harold, 74, Navajo speaker | Audio in Navajo (oral language), limited English reading | Native speaker (nv) |
| V09 | Darnell, 52, low literacy / dyslexia | Visual; slow reader, relies on layout and icons | General |
| V10 | Emma, 29, traumatic brain injury | Visual; memory and attention limits, fatigue | General (cognitive) |
| V11 | Sofia, 37, Deaf, ASL first language | Visual only; English is her second, written language | General |
| V12 | Kevin, 44, rushed parent, colour-blind | Visual; interrupted, fast, deuteranopia | General |
| V13 | Ruth, 63, distrustful verifier | Visual; checks everything, paper record matters | General |
| V14 | Danielle, 31, overseas military voter | Remote ballot marking on own device, print and return | — (remote; WCAG) |

Election staff and other roles — `personas/staff/`

| ID | Persona | Main tasks | 8.4-A coverage |
|---|---|---|---|
| S01 | Gloria, 66, first-time poll worker | Set up, activate ballots, help voters, close | Low experience |
| S02 | Frank, 58, precinct lead / chief judge | Opening/closing, reports, troubleshooting, chain of custody | High experience |
| S03 | Aisha, 36, election programmer | Build election definitions: districts, contests, ballot styles, translations | — (EMS) |
| S04 | Tom, 55, county election administrator | Oversight, results, certification, public communication | — (EMS / reports) |
| S05 | Rosa & Jim, central-count adjudication team | Scan ballots, resolve ambiguous marks (bipartisan pair) | — (central count) |
| S06 | Ben, 27, L&A tester / warehouse tech | Pre-election logic & accuracy testing, device prep, seals | — (device prep) |
| S07 | Dr. Nkechi Obi, 49, post-election auditor | Risk-limiting audits, reconciling paper with reports | — (audit) |
| S08 | Raymond, 60, partisan poll watcher | Observes from a distance: public counters, tapes, adjudication | — (public screens) |
| S09 | Kim, 33, vendor help desk | Diagnoses devices by phone from what poll workers read aloud | — (messages) |
| S10 | Dr. Elena Petrov, 45, VSTL test engineer | Certification testing against VVSG; TDP and evidence | — (pre-certification check) |

**On diversity:** names and backgrounds vary on purpose, but no design decision should
key off ethnicity. What changes a design is **language, script, literacy, culture of
use (name order, date formats), abilities, assistive technology, device habits and
context**. Each persona states those explicitly.

## Choosing personas for a screen

Don't run all 24. Pick by what the screen does:

| Screen / feature | Always include | Add when relevant |
|---|---|---|
| Any voter screen | V02, V03, V06 | V09 for dense text, V10 for multi-step, V12 for colour |
| Contest selection, review, cast | V01, V03, V04, V05 | V13 (verification), V10 (memory) |
| Ballot measures / long text | V09, V06 | V07, V08 (translation length, audio length) |
| Warnings, timeouts, errors | V10, V11, V12 | V03 (audio equivalent), V05 (mis-taps) |
| Language / settings controls | V06, V07, V08, V02 | V03 |
| Paper record / VVPAT / ballot | V13, V02 | V07 (English-only auditability 5.1-C) |
| Remote ballot marking / absentee | V14 | V02, V03 (accessible absentee) |
| Poll-worker device screens | S01, S02 | S06 |
| Device messages, errors, status screens | S01, S09 | S08 (if visible to the public) |
| Public-facing counters, tapes, posted reports | S08 | V13 |
| EMS / ballot definition | S03 | S04 |
| Reports, results, audit | S04, S07 | S02 (closing reports), S08 |
| Adjudication | S05 | S07, S08 |
| Settings, documentation, certification evidence | S10 | S09 |

## Persona walkthrough (method)

A cognitive walkthrough per persona (Wharton et al., 1994), run on one concrete task
(the persona file suggests tasks):

1. State the persona, their mode/devices and the task. Start from the real entry point.
2. For **every step**, answer as that person, with their abilities and knowledge:
   - **Goal:** will they try to do the right thing here?
   - **Notice:** will they notice the correct control — in their mode (audio order,
     switch scanning order, zoomed view, Spanish label)?
   - **Associate:** will they know that control does what they want?
   - **Feedback:** after acting, will they know it worked — perceivable to them?
3. Any "no" is a finding: which step, which question, why for this persona, the rule it
   breaks (ux-review references), and a fix.
4. Also note **time and effort** (a step that works but takes V04 forty switch presses
   is a finding) and **dignity/privacy** (does it force them to ask for help or reveal
   their choices — 6.1-B).

Report per persona, then merge: one root cause hitting several personas is one finding
listing all of them, ranked with ux-review's severity scale. Say which personas you
**didn't** walk and why.

## Persona file template

Every persona file uses the same sections, so they can be compared and extended:
Snapshot · Context · Goals · Knowledge · Language & literacy · Abilities & assistive
tech · Devices & modes · Behaviours · What breaks for them (testable, with rule IDs) ·
Walkthrough tasks · Recruiting profile. To add a persona, copy the closest file and
keep the sections.
