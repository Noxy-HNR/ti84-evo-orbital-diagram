# TI-84 Evo — Orbital Box Diagram / Hund's Rule Tool

Enter a subshell like `2p4` or `3d6` and get the orbital box diagram filled
by Hund's rule, plus the paramagnetic / diamagnetic verdict.

Written for the **TI-84 Evo** (Texas Instruments, April 2026) running TI's
adapted CircuitPython build.

## What it does

```
------------------------------
2p4
l = 1 (p subshell)
boxes = 3, capacity = 6 e-

orbitals (ml under box):
 [^v][^ ][^ ]
  -1   0  +1

unpaired e- : 2
paired sets : 1
=> PARAMAGNETIC
   (2 unpaired spin(s))
------------------------------
```

- Box count from the angular momentum quantum number: s=1, p=3, d=5, f=7.
- Filled by **Hund's rule** — one electron per box, same spin, before any
  pairing begins.
- `m_l` values printed under each box, running `-l` to `+l`.
- Unpaired count, paired count, and the magnetic verdict.

## Input validation

The parser rejects, with a specific message rather than a traceback:

| Input   | Response                          |
|---------|-----------------------------------|
| `2p7`   | `! 2p holds at most 6 e-`         |
| `2d4`   | `! No 2d subshell (needs n>2)`    |
| `zz`    | `! Too short - try 2p4`           |
| `3x2`   | `! Letter must be s, p, d or f`   |

`2d4` is rejected because `l` must satisfy `l <= n-1` — there is no 2d
subshell at all, which is a chemistry error worth catching rather than
quietly diagramming.

Spaces and a caret are tolerated, so `3d^6` and `3 d 6` both parse.

## Arrow glyphs

Defaults to ASCII `^` / `v`, because the calculator font is not guaranteed
to carry the Unicode arrows. Menu option 2 switches to `↑` / `↓`, but it
**probes first**: if printing the glyphs raises, it falls back to ASCII with
a message instead of crashing part-way through drawing a diagram.

## Calculator constraints

- Imports nothing — pure Python.
- No f-strings. TI's Python builds have rejected `f"..."` with a
  `SyntaxError`, so all formatting uses `.format()` and concatenation.
- No file I/O; the Python environment is sandboxed.
- Output is capped at 30 columns. The widest case is the 7-box `4f`
  diagram at 29.

## Transfer

Send `ORBITAL.py` to the calculator with **TI Connect Evo**, then run it
from the Python App's File Manager. The filename is 7 characters — TI
program names follow the 8-character variable-name limit.

## Verification

Checked against known cases: `2p4` → 2 unpaired (paramagnetic), `2p3` → 3
unpaired, `3d6` → 4 unpaired, `3d10` → 0 unpaired (diamagnetic), `4f7` → 7
unpaired (half-filled f shell).
