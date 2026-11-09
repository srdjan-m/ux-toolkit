# Building a palette

What to aim for and why is in ux-review's `references/color.md` §5 (harmony) and §1–4
(contrast, meaning, dark mode). This file is the **procedure**. Every colour you propose
leaves this process with a hex value, its OKLCH and a measured contrast for its role.

Tools (`ux_measure.py` in the ux-review skill):

```
python ux_measure.py scale   HEX              tonal scale 50..950 for one hue
python ux_measure.py harmony HEX [--scheme X] related hues at equal lightness
python ux_measure.py oklch   HEX HEX ...      do these sit together? (L/C spread)
python ux_measure.py contrast FG BG ...       pass/fail per role
```

## 1. Start from what exists

- Design system present → map the request onto its tokens. Usually the answer is "use
  these existing tokens differently", not new colours.
- Brand colour given → that's the accent hue. Don't fight it; adjust its lightness for
  UI use (a brand colour is rarely the right button colour as-is).
- Nothing given → pick one accent hue from the product's personality and context. Blue
  is the safe default for trust/forms; avoid red, amber or green as the accent (they're
  needed for status).

## 2. The minimum complete set

| Role | How to make it |
|---|---|
| **Neutral scale** (surfaces, borders, text) | `scale` on a grey tinted toward the accent (C ≈ 0.01–0.02 at the accent's hue). |
| **Accent scale** (primary action, links, focus, selection) | `scale` on the accent. Primary fill is usually step 600–700 so white text passes 4.5:1. |
| **Status: error, warning, success, info** | Hues ~25° (red), ~75° (amber), ~145° (green), ~250° (blue) in OKLCH. Keep them ≥ ~40° away from the accent hue; if the accent *is* blue, info can reuse it. Match their L and C to each other (`oklch` spread). |
| **Data series** (charts only) | `harmony --scheme triadic/tetradic` from the accent, or a dedicated categorical set; check colour-blind separation and that each has a label or pattern too. |

Resist more. Every extra hue dilutes the accent and needs its own states and dark
variant.

## 3. Assign roles, then measure

For each role write the pair that actually appears in the UI and measure it:

- body text on surface ≥ 4.5:1 (VVSG work: ≥ 10:1)
- secondary text on surface ≥ 4.5:1 — the one most often missed
- primary button text on fill ≥ 4.5:1, button fill vs surface ≥ 3:1
- input border vs surface ≥ 3:1, focus ring vs both surface and component ≥ 3:1
- status colour used as text ≥ 4.5:1; as an icon or fill ≥ 3:1
- warning (amber) fills almost always need dark text — check both

## 4. States

From the same scale, one step apart, consistently: hover = +1 step darker (light
theme), pressed = +2, selected/subtle background = step 50–100, disabled = neutral, not
a faded accent. Same rule in every component.

## 5. Dark theme

Not an inversion. Surfaces from the neutral scale's 900–950 (near-black, not #000 for
general products), raised surfaces lighter, text 50–200. Accent and status at a
**lighter step with lower chroma** than in light theme (use `scale` and pick the step
that passes on the dark surface; usually 300–400). Re-measure every pair from §3.

## 6. Deliver

- Tokens by role name, not by hue: `--color-action-primary`, not `--blue-600`. Hue
  scales may exist underneath; components reference roles only.
- A table: token → hex → OKLCH → where used → measured pair and ratio.
- For a design system with its own token format (PES: `--app-*`), use that format and
  list proposals as gaps.
- A swatch preview (HTML) showing every role in context — buttons, text, badges, an
  input in each state, both themes — is more convincing than a list of hexes.
