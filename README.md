# breeze-device-battery-icons

Battery-level icons for wireless mice and keyboards, built from KDE's
[Breeze](https://invent.kde.org/frameworks/breeze-icons) battery icons with a
small mouse or keyboard glyph in the bottom-right corner.

```
input-mouse-battery-{000..100}[-charging].svg
input-keyboard-battery-{000..100}[-charging].svg
```

The icons come in steps of 10, in 16, 22, 24 and 32 px, for both `breeze` and `breeze-dark`.
They use Breeze's `current-color-scheme` classes, so they follow your Plasma color scheme.

## Install

Arch Linux:

```sh
makepkg -si
```

Manual install:

```sh
cp -r icons/breeze icons/breeze-dark /usr/share/icons/
```

## Regenerate

`generate.py` reads the installed Breeze battery icons and writes `icons/`:

```sh
python3 generate.py [/usr/share/icons] [./icons]
```

You need Qt ≥ 6.7 (QtSvg `clip-path` support) for the cut-out around the badge.

## License

These are derived from Breeze icons, so they're under LGPL-3.0-or-later like Breeze.
