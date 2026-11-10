#!/usr/bin/env python3
"""Generate {input-mouse,input-keyboard,audio-headset}-battery-NNN[-charging].svg icons.

Takes Breeze's status/<size>/battery-NNN[-charging].svg, shifts the battery up,
cuts out the bottom-right corner and puts a small pixel-aligned mouse or
keyboard glyph there. Colors stay KDE color-scheme aware (currentColor + classes).

Usage: generate.py [ICONS_DIR] [OUT_DIR]
Writes OUT_DIR/{breeze,breeze-dark}/status/<size>/...
"""
import re
import sys
from pathlib import Path

ICONS = Path(sys.argv[1] if len(sys.argv) > 1 else "/usr/share/icons")
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else Path(__file__).parent / "icons")
THEMES = {"breeze": "#232629", "breeze-dark": "#fcfcfc"}  # ColorScheme-Text

# size: how far the battery is moved up to make room for the badge
BATTERY_DY = {16: -2, 22: -2, 24: -2, 32: -4}
LEVELS = [f"{n:03d}" for n in range(0, 101, 10)]


def rect(x, y, w, h):
    return f"M{x} {y}h{w}v{h}h{-w}z"


def rrect(x, y, w, h, r):
    """Rounded rect, clockwise."""
    if r <= 0:
        return rect(x, y, w, h)
    return (f"M{x + r} {y}h{w - 2 * r}a{r} {r} 0 0 1 {r} {r}v{h - 2 * r}"
            f"a{r} {r} 0 0 1 {-r} {r}h{-(w - 2 * r)}a{r} {r} 0 0 1 {-r} {-r}"
            f"v{-(h - 2 * r)}a{r} {r} 0 0 1 {r} {-r}z")


def mouse(x, y, w, h):
    r = (w - 1) / 2
    d = rrect(x, y, w, h, r) + rrect(x + 1, y + 1, w - 2, h - 2, r - 1)
    d += rect(x + (w - 1) // 2, y + 1, 1, max(2, round(h * 0.4) - 1))
    return d


def keyboard(x, y, w, h):
    d = rect(x, y, w, h) + rect(x + 1, y + 1, w - 2, h - 2)
    row = y + 2
    rows = []
    while row + 2 <= y + h - 1:
        rows.append(row)
        row += 2
    for r in rows[:-1]:
        for kx in range(x + 2, x + w - 2, 2):
            d += rect(kx, r, 1, 1)
    d += rect(x + 4, rows[-1], w - 8, 1)  # spacebar
    return d


def headset(x, y, w, h):
    """Headband + ear cups + mic boom. Use an even width so the arc is pixel-centred."""
    r = w // 2
    cw = 3 if w >= 12 else 2  # ear cup width
    cup = max(3, round(h * 0.4))
    d = f"M{x} {y + r}A{r} {r} 0 0 1 {x + w} {y + r}h-1A{r - 1} {r - 1} 0 0 0 {x + 1} {y + r}z"
    d += rect(x, y + r, 1, h - r) + rect(x + w - 1, y + r, 1, h - r)
    d += rect(x, y + h - cup, cw, cup) + rect(x + w - cw, y + h - cup, cw, cup)
    d += rect(x + cw, y + h - 1, max(1, w // 2 - cw), 1)  # microphone boom
    return d


# icon name prefix: (glyph, fill-rule, {size: (w, h)})
GLYPHS = {
    "input-mouse": (mouse, "evenodd", {16: (5, 7), 22: (7, 10), 24: (7, 10), 32: (9, 14)}),
    "input-keyboard": (keyboard, "evenodd", {16: (9, 6), 22: (13, 9), 24: (13, 9), 32: (17, 11)}),
    "audio-headset": (headset, "nonzero", {16: (6, 7), 22: (8, 10), 24: (8, 10), 32: (12, 14)}),
}


def compose(src: str, size: int, kind: str, text_color: str) -> str:
    dy = BATTERY_DY[size]
    fn, fill_rule, dims = GLYPHS[kind]
    w, h = dims[size]
    bx, by = size - w, size - h
    cx, cy = bx - 1, by - 1  # 1px gap around the badge

    style = re.search(r"<style.*?</style>", src, re.S).group(0)
    if ".ColorScheme-Text" not in style:
        style = style.replace("</style>",
                              f"    .ColorScheme-Text {{ color:{text_color}; }}\n        </style>")
    body = re.search(r"<svg[^>]*>(.*)</svg>", src, re.S).group(1)
    body = re.sub(r"<defs.*?</defs>", "", body, flags=re.S)
    body = re.sub(r"<style.*?</style>", "", body, flags=re.S).strip()

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
    <defs>
        {style}
        <mask id="badge-cut" maskUnits="userSpaceOnUse" x="0" y="0" width="{size}" height="{size}">
            <path fill="#fff" d="M0 0H{size}V{cy}H{cx}V{size}H0z"/>
        </mask>
    </defs>
    <g mask="url(#badge-cut)">
        <g transform="translate(0,{dy})">
            {body}
        </g>
    </g>
    <path class="ColorScheme-Text" fill="currentColor" fill-rule="{fill_rule}" d="{fn(bx, by, w, h)}"/>
</svg>
"""


def main():
    count = 0
    for theme, text_color in THEMES.items():
        for size in BATTERY_DY:
            outdir = OUT / theme / "status" / str(size)
            outdir.mkdir(parents=True, exist_ok=True)
            for level in LEVELS:
                for suffix in ("", "-charging"):
                    src = (ICONS / theme / "status" / str(size) / f"battery-{level}{suffix}.svg").read_text()
                    for kind in GLYPHS:
                        name = f"{kind}-battery-{level}{suffix}.svg"
                        (outdir / name).write_text(compose(src, size, kind, text_color))
                        count += 1
    print(f"wrote {count} icons to {OUT}")


if __name__ == "__main__":
    main()
