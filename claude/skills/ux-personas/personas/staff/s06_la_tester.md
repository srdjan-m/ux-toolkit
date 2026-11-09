# S06 — Ben Thompson, 27, logic & accuracy tester / warehouse technician

**Snapshot:** County elections technician. Before each election he prepares and tests
every device: loads the election definition, runs logic and accuracy (L&A) test decks,
checks results against expected totals, seals devices, logs serial numbers.

**Context:** A warehouse with 200 devices, two weeks, a public L&A test with observers
and press on one day. Repetitive work at scale; a skipped step means a device fails on
election morning.

**Goals:** Every device loaded with the right definition and verified; test results
that clearly pass or fail; a complete, auditable log.

**Knowledge:** Tech — high; procedure — good. Election law — moderate.

**Language & literacy:** English native.

**Abilities & assistive tech:** None; works standing, often with gloves in a cold
warehouse.

**Devices & modes:** Device admin screens, USB/media loading, test-deck scanning, L&A
reports, barcode scanner for serials.

**Behaviours:** Batches the same step across many devices. Reads only the result line.
Trusts green.

**What breaks for them:**
- Pass/fail not unambiguous at a glance, or shown by colour only.
- Expected vs actual totals not side by side; mismatch not highlighted by contest.
- No confirmation of *which* election definition (name, version, hash in human terms)
  is loaded (7.3-O: workers shouldn't guess the setup is right).
- Small touch targets with gloves; long-press or gestures.
- Logs that can't be exported or matched to device serials.

**Walkthrough tasks:** Load the definition on a device, confirm the version, run a test
deck, find the one contest whose total is off, re-test, seal and log.

**Recruiting profile:** County technicians or vendor field staff who run L&A. Not in
8.4-A (pre-election) — test separately.
