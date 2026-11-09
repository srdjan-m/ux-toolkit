#!/usr/bin/env python3
"""
ux_measure.py - measure instead of eyeballing. Standard library only (Python 3.9+).

Subcommands:

  contrast FG BG [FG BG ...]
      WCAG 2.x luminosity contrast ratio for each colour pair, checked against the
      WCAG 2.2 and VVSG 2.0 thresholds.

        python ux_measure.py contrast 6c6c6c ffffff  ffff00 111111

  size --diag INCHES --res WxH [--px N ...] [--font-px N ...] [--cap-ratio R]
      Convert on-screen pixels to physical millimetres for a given display, so VVSG
      minimums (written in mm) can be checked against a design drawn in px.

        python ux_measure.py size --diag 21.5 --res 1920x1080 --px 48 64 --font-px 28

      --px       sizes to convert as-is (touch targets, gaps, icons)
      --font-px  font sizes; also reports the uppercase-I height VVSG measures text by,
                 using --cap-ratio (cap height / font size, default 0.70 - check the
                 actual font: Arial ~ 0.716, Open Sans ~ 0.714, Inter ~ 0.727)

  oklch HEX [HEX ...]
      Perceived lightness (L), chroma (C) and hue (H) in OKLCH, plus the L/C spread,
      to judge whether colours that share a role sit together.

        python ux_measure.py oklch 2f6fdf 2e9e5b d97706 dc2626

  harmony BASE [--scheme analogous|complementary|split|triadic|tetradic]
      Rotate the base hue in OKLCH at the base's L and C; prints hex, and contrast of
      white and black text on each.

        python ux_measure.py harmony 2f6fdf --scheme triadic

  scale BASE
      Tonal scale 50..950 at the base's hue (OKLCH lightness stops, chroma tapering
      toward the ends), with text contrast on each step.

        python ux_measure.py scale 2f6fdf

Size: assumes square pixels. The display must be shown at 1:1 (design px == device px); if the
design is drawn at a different scale, convert to device px first.
"""

import argparse
import math
import sys

# (label, minimum ratio) - what each threshold is for
CONTRAST_RULES = [
    ("WCAG 1.4.11 non-text / 1.4.3 large text", 3.0),
    ("WCAG 1.4.3 AA body text", 4.5),
    ("WCAG 1.4.6 AAA body text", 7.0),
    ("VVSG 7.1-C default (all info-bearing elements)", 10.0),
]

# (label, minimum mm) - VVSG 2.0 physical minimums
SIZE_RULES = [
    ("VVSG 7.2-I touch-target gap", 2.54),
    ("VVSG 7.1-G smallest allowed text (I-height)", 3.5),
    ("VVSG 7.1-G default text (I-height)", 4.8),
    ("VVSG 7.2-I touch target, each side", 12.7),
]


def parse_hex(value: str) -> tuple[int, int, int]:
    text = value.strip().lstrip("#")
    if len(text) == 3:
        text = "".join(ch * 2 for ch in text)
    if len(text) != 6:
        raise ValueError(f"not a hex colour: {value!r}")
    try:
        return tuple(int(text[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]
    except ValueError:
        raise ValueError(f"not a hex colour: {value!r}") from None


def luminance(rgb: tuple[int, int, int]) -> float:
    """WCAG 2.x relative luminance."""
    def channel(c: int) -> float:
        s = c / 255
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg: str, bg: str) -> float:
    a, b = luminance(parse_hex(fg)), luminance(parse_hex(bg))
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def cmd_contrast(args: argparse.Namespace) -> int:
    colours = args.colours
    if len(colours) % 2:
        print("error: give colours in FG BG pairs", file=sys.stderr)
        return 2
    for fg, bg in zip(colours[::2], colours[1::2]):
        try:
            ratio = contrast_ratio(fg, bg)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        print(f"#{fg.lstrip('#')} on #{bg.lstrip('#')}:  {ratio:.2f}:1")
        for label, minimum in CONTRAST_RULES:
            mark = "pass" if ratio >= minimum else "FAIL"
            print(f"  [{mark}] {minimum:>4}:1  {label}")
        if 4.5 <= ratio <= 8.0:
            print("  [info] inside VVSG 7.1-D low-contrast option range (4.5-8:1)")
        print()
    return 0


# ------------------------------------------------------------------ OKLCH
#
# OKLab / OKLCH (Bjorn Ottosson, 2020, https://bottosson.github.io/posts/oklab/).
# Chosen over HSL because HSL "lightness" is not perceived lightness: HSL yellow and
# blue at L=50% look nothing alike, so rotating hue in HSL gives harmonies whose
# members differ wildly in visual weight. In OKLCH, equal L looks equally light, which
# is what makes rotated hues sit together. Matrix constants are from that post.

def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c: float) -> float:
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def hex_to_oklch(value: str) -> tuple[float, float, float]:
    r, g, b = (_srgb_to_linear(c / 255) for c in parse_hex(value))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(x) ** (1 / 3), x) for x in (l, m, s))
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    a = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    bb = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    C = math.hypot(a, bb)
    H = math.degrees(math.atan2(bb, a)) % 360
    return L, C, H


def _oklch_to_linear_rgb(L: float, C: float, H: float) -> tuple[float, float, float]:
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def oklch_to_hex(L: float, C: float, H: float) -> tuple[str, float]:
    """Return (hex, chroma actually used). Not every L/C/H exists in sRGB; rather than
    clipping channels (which shifts hue and lightness), keep L and H and lower C by
    bisection until the colour fits. The caller reports the reduction."""
    def fits(c: float) -> bool:
        return all(-1e-6 <= x <= 1 + 1e-6 for x in _oklch_to_linear_rgb(L, c, H))
    if not fits(C):
        lo, hi = 0.0, C
        for _ in range(30):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if fits(mid) else (lo, mid)
        C = lo
    rgb = (_linear_to_srgb(min(1.0, max(0.0, x))) for x in _oklch_to_linear_rgb(L, C, H))
    return "".join(f"{round(x * 255):02x}" for x in rgb), C


def _text_on(hex_value: str) -> str:
    w, k = contrast_ratio("ffffff", hex_value), contrast_ratio("000000", hex_value)
    return f"white {w:5.2f}:1  black {k:5.2f}:1"


def cmd_oklch(args: argparse.Namespace) -> int:
    rows = []
    for value in args.colours:
        try:
            rows.append((value.lstrip("#").lower(), *hex_to_oklch(value)))
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
    print("  hex       L      C      H     text on it")
    for hx, L, C, H in rows:
        # Below C~0.02 hue is noise (a grey has no meaningful hue), so don't print one.
        hue = f"{H:5.1f}" if C >= 0.02 else "    -"
        print(f"  #{hx}  {L:.3f}  {C:.3f}  {hue}  {_text_on(hx)}")
    if len(rows) > 1:
        Ls, Cs = [r[1] for r in rows], [r[2] for r in rows]
        print(f"\n  spread: L {max(Ls) - min(Ls):.3f}   C {max(Cs) - min(Cs):.3f}")
        print("  colours sharing a role (series, badges, tags) read as a set when the"
              " L and C spreads are small (roughly L < 0.08, C < 0.05)")
    return 0


# Hue offsets in degrees from the base colour.
HARMONIES = {
    "analogous": (-30, 0, 30),
    "complementary": (0, 180),
    "split": (0, 150, 210),
    "triadic": (0, 120, 240),
    "tetradic": (0, 90, 180, 270),
}


def cmd_harmony(args: argparse.Namespace) -> int:
    try:
        L, C, H = hex_to_oklch(args.base)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"base #{args.base.lstrip('#').lower()}:  L {L:.3f}  C {C:.3f}  H {H:.1f}")
    if C < 0.02:
        print("  base is (near) grey - hue rotation is meaningless; pick a coloured base")
        return 1
    names = [args.scheme] if args.scheme else list(HARMONIES)
    for name in names:
        print(f"\n{name}")
        for offset in HARMONIES[name]:
            h = (H + offset) % 360
            hx, used = oklch_to_hex(L, C, h)
            note = f"  (C lowered to {used:.3f} to fit sRGB)" if used < C - 0.002 else ""
            print(f"  {offset:+4d}  #{hx}  H {h:5.1f}  {_text_on(hx)}{note}")
    return 0


# Tonal-scale lightness stops, 50 (lightest) .. 950 (darkest). Even-ish steps in OKLCH
# L, with the ends compressed: UI uses many near-white and near-black tints (subtle
# backgrounds, dark surfaces) and few mid tones. The mapping is a design choice made
# 2026-11-09 for this toolkit, not a standard; adjust per project.
SCALE_L = {50: 0.97, 100: 0.93, 200: 0.87, 300: 0.79, 400: 0.70,
           500: 0.61, 600: 0.52, 700: 0.44, 800: 0.36, 900: 0.28, 950: 0.21}


def cmd_scale(args: argparse.Namespace) -> int:
    try:
        L0, C0, H = hex_to_oklch(args.base)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    grey = C0 < 0.02
    print(f"base #{args.base.lstrip('#').lower()}:  L {L0:.3f}  C {C0:.3f}  "
          f"H {'-' if grey else f'{H:.1f}'}   (closest step marked *)")
    closest = min(SCALE_L, key=lambda k: abs(SCALE_L[k] - L0))
    for step, L in SCALE_L.items():
        # Chroma tapers toward both ends: very light and very dark colours can't hold
        # much colour in sRGB, and forcing it makes pale tints look neon. Peak at the
        # base's own lightness.
        taper = max(0.0, 1 - abs(L - L0) / 0.6) ** 0.7
        hx, used = oklch_to_hex(L, C0 * taper, H)
        mark = "*" if step == closest else " "
        print(f"  {step:>3}{mark} #{hx}  L {L:.2f}  C {used:.3f}  {_text_on(hx)}")
    print("\n  the base itself is not in the scale; use the * step or replace it with the base")
    return 0


def mm_per_px(diag_in: float, width_px: int, height_px: int) -> float:
    diag_px = math.hypot(width_px, height_px)
    return diag_in * 25.4 / diag_px


def cmd_size(args: argparse.Namespace) -> int:
    try:
        w, h = (int(n) for n in args.res.lower().split("x"))
    except ValueError:
        print("error: --res must look like 1920x1080", file=sys.stderr)
        return 2
    scale = mm_per_px(args.diag, w, h)
    print(f'{args.diag}" at {w}x{h}: {scale:.4f} mm/px  ({1 / scale:.2f} px/mm)\n')

    print("VVSG minimums on this display:")
    for label, minimum in SIZE_RULES:
        print(f"  {minimum:>5} mm = {minimum / scale:6.1f} px   {label}")
    print()

    for px in args.px or []:
        print(f"{px:>6g} px = {px * scale:6.2f} mm")
    for px in args.font_px or []:
        cap = px * args.cap_ratio * scale
        verdict = ("meets 4.8 mm default" if cap >= 4.8
                   else "below 4.8 mm default" if cap >= 3.5
                   else "below 3.5 mm minimum")
        print(f"font {px:>4g} px -> I-height {cap:5.2f} mm  ({verdict}, cap-ratio {args.cap_ratio})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Contrast and physical-size checks for UI review.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_contrast = sub.add_parser("contrast", help="contrast ratio for FG BG pairs")
    p_contrast.add_argument("colours", nargs="+", metavar="HEX")
    p_contrast.set_defaults(func=cmd_contrast)

    p_size = sub.add_parser("size", help="convert px to mm for a display")
    p_size.add_argument("--diag", type=float, required=True, help="diagonal in inches")
    p_size.add_argument("--res", required=True, help="resolution, e.g. 1920x1080")
    p_size.add_argument("--px", type=float, nargs="*", help="pixel sizes to convert")
    p_size.add_argument("--font-px", type=float, nargs="*", help="font sizes in px")
    p_size.add_argument("--cap-ratio", type=float, default=0.70,
                        help="cap height / font size (default 0.70)")
    p_size.set_defaults(func=cmd_size)

    p_oklch = sub.add_parser("oklch", help="perceived lightness/chroma/hue of colours")
    p_oklch.add_argument("colours", nargs="+", metavar="HEX")
    p_oklch.set_defaults(func=cmd_oklch)

    p_harm = sub.add_parser("harmony", help="hue harmonies from a base colour")
    p_harm.add_argument("base", metavar="HEX")
    p_harm.add_argument("--scheme", choices=sorted(HARMONIES),
                        help="one scheme only (default: all)")
    p_harm.set_defaults(func=cmd_harmony)

    p_scale = sub.add_parser("scale", help="tonal scale 50..950 for one hue")
    p_scale.add_argument("base", metavar="HEX")
    p_scale.set_defaults(func=cmd_scale)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
