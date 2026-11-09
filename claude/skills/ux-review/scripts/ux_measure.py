#!/usr/bin/env python3
"""
ux_measure.py - measure instead of eyeballing. Standard library only (Python 3.9+).

Two subcommands:

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

Assumes square pixels. The display must be shown at 1:1 (design px == device px); if the
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

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
