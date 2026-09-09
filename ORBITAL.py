# ORBITAL.py -- Orbital Box Diagram / Hund's Rule Tool
# Target : TI-84 Evo (TI CircuitPython build)
# Imports: none required
# Notes  : no f-strings (TI Python builds reject them), no file I/O.
#
# Enter a subshell with its electron count, e.g. 2p4 or 3d6.

WIDTH = 30
ORB = "spdf"

# Arrow glyphs. ASCII is the default because the calculator font
# is not guaranteed to carry the Unicode arrows -- menu item 2
# switches to them if your screen renders them.
ASCII_ARROWS = ("^", "v")
UNI_ARROWS = ("↑", "↓")


def parse_subshell(raw):
    """'3d6' -> (3, 2, 6). Raises ValueError with a friendly
    message describing exactly what was wrong."""
    t = raw.strip().lower().replace(" ", "").replace("^", "")
    if len(t) < 3:
        raise ValueError("Too short - try 2p4")
    if t[0] not in "1234567":
        raise ValueError("Start with shell n (1-7)")
    n = int(t[0])
    letter = t[1]
    if letter not in ORB:
        raise ValueError("Letter must be s, p, d or f")
    l = ORB.index(letter)
    if l >= n:
        # e.g. 2d does not exist: l must be <= n-1
        raise ValueError("No {}{} subshell (needs n>{})".format(n, letter, l))
    try:
        e = int(t[2:])
    except ValueError:
        raise ValueError("Electron count must be a number")
    if e < 0:
        raise ValueError("Electron count can't be < 0")
    cap = 4 * l + 2                     # 2(2l+1)
    if e > cap:
        raise ValueError("{}{} holds at most {} e-".format(n, letter, cap))
    return n, l, e


def hund_fill(boxes, e):
    """One electron per box before pairing (Hund's rule).
    Returns per-orbital occupancy, e.g. 2p4 -> [2, 1, 1]."""
    cells = [0] * boxes
    for i in range(e):
        cells[i % boxes] += 1
    return cells


def draw_boxes(cells, arrows):
    up, dn = arrows
    out = ""
    for c in cells:
        if c == 2:
            out += "[" + up + dn + "]"
        elif c == 1:
            out += "[" + up + " ]"
        else:
            out += "[  ]"
    return out


def draw_labels(l):
    """m_l values running -l .. +l under each box."""
    out = ""
    for m in range(-l, l + 1):
        if m > 0:
            lab = "+" + str(m)
        else:
            lab = str(m)
        out += "{:>3} ".format(lab)
    return out


def report(n, l, e, arrows):
    boxes = 2 * l + 1
    cap = 4 * l + 2
    cells = hund_fill(boxes, e)
    unpaired = 0
    pairs = 0
    for c in cells:
        if c == 1:
            unpaired += 1
        elif c == 2:
            pairs += 1

    print("-" * WIDTH)
    print("{}{}{}".format(n, ORB[l], e))
    print("l = {} ({} subshell)".format(l, ORB[l]))
    print("boxes = {}, capacity = {} e-".format(boxes, cap))
    print("")
    # ml runs under each box; kept on its own line so the
    # 7-box f diagram still fits the screen width.
    print("orbitals (ml under box):")
    print(" " + draw_boxes(cells, arrows))
    print(" " + draw_labels(l))
    print("")
    print("unpaired e- : {}".format(unpaired))
    print("paired sets : {}".format(pairs))
    if unpaired > 0:
        print("=> PARAMAGNETIC")
        print("   ({} unpaired spin(s))".format(unpaired))
    else:
        print("=> DIAMAGNETIC")
        print("   (all electrons paired)")
    print("-" * WIDTH)


def main():
    arrows = ASCII_ARROWS
    print("ORBITAL BOX / HUND'S RULE")
    while True:
        print("")
        print("1) Enter subshell (e.g. 2p4)")
        print("2) Toggle arrow style")
        print("3) Quit")
        choice = input("Choice: ").strip()
        if choice == "1":
            raw = input("Subshell: ")
            try:
                n, l, e = parse_subshell(raw)
            except ValueError as err:
                print("! " + str(err))
                continue
            report(n, l, e, arrows)
        elif choice == "2":
            if arrows == ASCII_ARROWS:
                # Probe before committing: if this screen cannot
                # encode the glyphs the print raises, and we would
                # much rather fall back here than crash part-way
                # through drawing a diagram.
                try:
                    print("Arrows: " + UNI_ARROWS[0] + UNI_ARROWS[1])
                    arrows = UNI_ARROWS
                    print("(if those showed as boxes,")
                    print(" toggle back to ASCII)")
                except Exception:
                    arrows = ASCII_ARROWS
                    print("Unicode not supported here.")
                    print("Staying on ASCII ^ v")
            else:
                arrows = ASCII_ARROWS
                print("Arrows: ASCII ^ v")
        elif choice == "3":
            print("Bye.")
            return
        else:
            print("! Pick 1, 2 or 3.")


main()
