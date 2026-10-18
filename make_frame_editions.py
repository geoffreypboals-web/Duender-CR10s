"""T-021: write the seven frame manuals (manual/editions/frame-<id>/) from the CAD model and frames_config.py.

Each frame manual covers the mechanical build up to a printer that moves freely by hand: extrusions, frame, triple Z
and bed plate, A/B motors and MGN9 Y rails, the reversed (V-Back) X axis and the belts. No wiring, electronics or
toolhead: those are separate manuals shared by all seven frames.

Every length comes from the model JSON (cad/designs/duender-large/out/c<size>-mgn9x-steps<tag>.json, written by
build_lego_mgn9_v2.py); where each piece comes from is in frames_config.py. Chapters 4-8 are templates in
frame-templates/ with {NAME} placeholders; chapters 0-3 and the README are built here. Chapter 2 (parts list) adds up
the "You need" tables of chapters 4-8, so it can't drift from them.

    python3 manual/make_frame_editions.py            # all seven
    python3 manual/make_frame_editions.py c400-cr10s4
"""
import json, math, os, re, sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CAD = os.path.join(ROOT, "cad", "designs", "duender-large", "out")
TPL = os.path.join(HERE, "frame-templates")
sys.path.insert(0, HERE)
from frames_config import FRAMES, STOCK_2040, STOCK_2020

KERF = 3                                    # saw cut, mm (bar plan)
QTY = OrderedDict([("A", 2), ("B", 2), ("C", 4), ("D", 2), ("E", 2), ("L", 1), ("U", 1), ("F", 2), ("G", 2), ("S", 1)])
NAMES = {"A": "lower base side", "B": "base member (front/back)", "C": "upright", "D": "upper base side",
         "E": "rear side Z carrier", "L": "front Z stub", "U": "front Z carrier", "F": "Y side", "G": "top brace (front/back)",
         "S": "X beam"}
PROFILE = {"A": "2040", "C": "2040", "D": "2040", "F": "2040"}            # the rest are 2020
BED = {"300": "bed plate 310 × 310 (the CR-10 bed, or any 310 plate with 4 corner holes)",
       "400": "AC 400 bed (410 × 410 plate)",
       "500": "bed plate 510 × 510 *(est.)* (the CR-10 S5 plate with its 12V heater removed)"}
PRINTED = {"TB", "J2", "M", "M2", "YF", "YB", "TN", "X1", "X2", "CM"}            # printed keys in the model JSON
CHAPTERS = [("00", "extrusions", "Before you start: the extrusions"), ("01", "tools-printing", "Safety, tools and printing the parts"),
            ("02", "parts-list", "Parts list"), ("03", None, None), ("04", "frame", "Building the frame"),
            ("05", "z-axis-bed", "Z axis (triple Z) and bed"), ("06", "ab-motors", "A/B motors and Y rails"),
            ("07", "x-axis", "X axis on MGN9 (reversed for rear docks)"), ("08", "belts", "Belts")]


def lengths(dims):
    """Key letter -> length (mm), from the model's dims."""
    W, D = dims["outer_width"], dims["outer_depth"]
    return dict(A=D - 40, B=W - 40, C=dims["upright"], D=D - 40, E=dims["rear_z_carrier"], L=dims["front_z_stub"],
                U=dims["front_z_carrier"], F=dims["y_side"], G=W - 40, S=dims["x_beam"])


def bar_plan(pieces, stock):
    """First-fit decreasing: pieces = [(key, length)], -> list of bars, each [(key, length), ...]."""
    bars = []
    for k, n in sorted(pieces, key=lambda t: -t[1]):
        assert n + KERF <= stock, (k, n, stock)
        for b in bars:
            if sum(x + KERF for _, x in b) + n <= stock:
                b.append((k, n)); break
        else:
            bars.append([(k, n)])
    return bars


def values(fid, f):
    j = json.load(open(os.path.join(CAD, f"c{f['size']}-mgn9x-steps{f['tag']}.json")))
    d = j["dims"]; L = lengths(d); W, D, P = d["outer_width"], d["outer_depth"], d["bed_plate"]
    donor, size = f.get("donor"), f["size"]
    fy0 = D - d["y_side"]                    # Y side front end (y); -9 = 9 mm past the front
    syr = 61 + P - 35
    yr = int(re.search(r"x (\d+)", d["y_rails"]).group(1))
    big = size != "300"; mm = d["middle_mount"]
    v = dict(SIZE=size, TAG=f["tag"], NAME=f["title"], W=W, D=D, P=P, TOP=d["upright"] + 20, FH=d["frame_height"],
             SYR=syr, WH=f"{W / 2:g}", REAR_GAP=D - 20 - syr - 10, DIAG=round(math.hypot(W, D)), XR=d["x_rail"],
             YR=yr, Y_RAIL=yr, YR_HALF=round(yr / 40), YR_SCREWS=2 * round(yr / 40), XR_HALF=round(d['x_rail'] / 40),
             BELT_M=round((2 * (D - 100) + 2 * (W - 70)) / 1000 + 0.2, 1),   # CoreXY: about 2 Y runs + 2 X runs, + clamps
             X_RAIL=d["x_rail"], X_BEAM=d["x_beam"], ZR=d["rear_z_rail"], ZRF=d["front_z_rail"],
             SCREW=d["lead_screw"], MM=mm, ZTRAVEL=d["z_travel_est"], KY=P - 35, KX2=P + 4, KXF=f"{P / 2:g}",
             # rear docks (toolhead manual): 58 mm pitch, 127 mm of X beam kept clear -> the most docks; one Back Mount M5
             # between each pair, held by 2 M5 into the back brace (its top slot and back slot)
             MAXD=1 + (d["x_beam"] - 127) // 58, BK=(d["x_beam"] - 127) // 58, BRACE_NUTS=8 + 2 * ((d["x_beam"] - 127) // 58),
             CH4_NUTS=102 + 2 * ((d["x_beam"] - 127) // 58),
             SIDE_FREE=f"{(W - P) / 2:g}", BACK_FREE=D - 61 - P, DOCK_GAP=D - 82 - 61 - P, BED=BED[size],
             BENCH=f"{W + 100} × {D + 100} mm", HELPER=" **Get a helper** from Step 4.7 on: the frame gets big and heavy." if size == "500" else "",
             STRETCH_NOTE=f" (the plates and screws are longer for the {size}; the middle mount is widened)" if big else "",
             MM_NOTE=f": Andizzle's is 265 mm wide, so for the {size} it must be **remixed to about {mm} mm** *(est.)*" if big else "",
             MM_PART=f", remixed to about {mm} mm *(est.)*" if big else " (Andizzle's, 265 wide)",
             MM_WARN=" and the widened middle mount (orange blocks in the pictures)" if big else "",
             Y_PLATE="Fit the **CR-10 Y plate (N2)** on the holders first if you have it (the CR-10 bed's own carrier); otherwise the bed sits directly on the holders."
                     if size == "300" else "The Y plate (**N2**) is **optional**: use the donor's Y carriage plate as a subframe **only if its holes line up** with the holders and the bed. Otherwise the bed sits directly on the holders.",
             MOTOR_SRC=f"from the {donor}" if donor else "donor or new",
             SCREW_SRC=(("3 donor, matched" if f.get("donors_needed", 1) > 1 else "2 donor + 1 bought") if donor else "a matched set, donor or new"),
             CH3_TITLE="Stripping the donor" if donor else "Getting the stock", CH3_FILE="donor-teardown" if donor else "stock",
             **{k: n for k, n in L.items() if k != "D"})     # {D} is the frame depth; the D piece = A
    v["CH3_LINK"] = f"03-{v['CH3_FILE']}-mgn9x.md"
    if fy0 == -9:
        v["F_RULE"] = f"The **Y sides (F)** = this depth **+ 9** (model: **{L['F']}**; the extra 9 mm sticks out at the front)."
        v["F_PLACE"] = "Make it **flush with the back** of the frame. It sticks out **9 mm past the front**."
        v["F_CHECK"] = "9 mm proud at the front"
    else:
        assert fy0 == 0, fy0
        v["F_RULE"] = f"The **Y sides (F)** are **{L['F']}**, the same as the depth: **flush at both ends**."
        v["F_PLACE"] = "Make it **flush with the back and the front** of the frame."
        v["F_CHECK"] = "flush at the front"
    src = f.get("source", {})
    cut = {k: (src[k][1] if k in src else True) for k in QTY}
    lab = lambda k: f"{k} {NAMES[k]} ×{QTY[k]} ({L[k]})" if QTY[k] > 1 else f"{k} {NAMES[k]} ({L[k]})"
    now = [k for k in "CADBEUL"]; later = [k for k in "FGS"]
    def cut_list(keys):
        c = [lab(k) for k in keys if cut[k]]; u = [lab(k) for k in keys if not cut[k]]
        out = ", ".join(c) if c else "nothing to cut"
        if u: out += f". **Check** the uncut {', '.join(u)}: cut them only if they're long"
        return out + "."
    v["CUT_NOW"], v["CUT_LATER"] = cut_list(now), cut_list(later)
    if donor:
        v["FRAME_NOTE"] = f"Most pieces come off the {donor} at their stock length ([Chapter 0](00-extrusions-mgn9x.md)); only the ones marked **cut** are cut."
        v["CUT_INTRO"] = "Most pieces in this manual are used **at the length they come off the donor**. Only the pieces marked **cut** in [Chapter 0](00-extrusions-mgn9x.md) go near the saw."
    else:
        v["FRAME_NOTE"] = "Every piece is cut to length from new bars ([Chapter 0](00-extrusions-mgn9x.md), bar plan in Chapter 3)."
        v["CUT_INTRO"] = "Every frame piece in this manual is **cut from new bars**: the bar plan is in [Chapter 3](03-stock-mgn9x.md)."
    return v, j, L, cut


def fill(text, v, where):
    def sub(m):
        assert m.group(1) in v, (where, m.group(1))
        return str(v[m.group(1)])
    return re.sub(r"\{([A-Z][A-Z0-9_]*)\}", sub, text)


def nav(i, v):
    """The navigation line of chapter i (index into CHAPTERS)."""
    t = lambda k: (v["CH3_TITLE"] if CHAPTERS[k][0] == "03" else CHAPTERS[k][2])
    f = lambda k: (v["CH3_LINK"] if CHAPTERS[k][0] == "03" else f"{CHAPTERS[k][0]}-{CHAPTERS[k][1]}-mgn9x.md")
    parts = []
    if i > 0: parts.append(f"[← {t(i - 1)}]({f(i - 1)})")
    parts.append("[Contents](README-mgn9x.md)")
    if i < len(CHAPTERS) - 1: parts.append(f"[Next: {t(i + 1)} →]({f(i + 1)})")
    return " · ".join(parts)


def ch00(fid, f, v, L, cut):
    rows = []
    src = f.get("source", {})
    for k, q in QTY.items():
        s = src.get(k, (f"cut from a new {PROFILE.get(k, '2020')} × {STOCK_2040 if PROFILE.get(k) else STOCK_2020}", True))[0]
        if k == "S" and "S" not in src: s = "cut from a new 2020 × 1000 (measure first, Step 7.4)"
        rows.append(f"| {k} | {NAMES[k]} | {PROFILE.get(k, '2020')} × **{L[k]}** | {q} | {s} | {'**cut**' if cut[k] else 'uncut'} |")
    head = (f"# Chapter 0: Before you start: the extrusions\n\n{nav(0, v)}\n\n"
            f"![Every extrusion in the {f['title']}](../../images/c{v['SIZE']}/lego-mgn9x/step-ext{v['TAG']}.png)\n\n"
            f"{f['intro']}\n\n")
    if f.get("donor"):
        head += f"**Where the lengths come from:** {f['lengths_source']}. The CAD model (`c{v['SIZE']}-duender-3z-mgn9x{v['TAG']}.step`) is built from them.\n\n"
    tbl = ["| Key | Part | Profile × length (mm) | Qty | Where it comes from | |", "|---|---|---|---|---|---|"] + rows
    rails = ["", "**Rails (bought; cut to length):**", "",
             "| Part | Length (mm) | Qty |", "|---|---|---|",
             f"| MGN12H rear Z rail + carriage | {v['ZR']} | 2 |", f"| MGN12H front Z rail + carriage | {v['ZRF']} | 1 |",
             f"| **MGN9** Y rail + MGN9H carriage | {v['YR']} | 2 |", f"| **MGN9** X rail + MGN9H carriage | {v['XR']} | 1 |"]
    tail = ["", f"Frame outside: **{v['W']} × {v['D']} mm**, **{v['FH']} mm** from the floor to the top of the Y sides. "
            f"Bed plate {v['P']} × {v['P']}: **61 mm** free in front, **{v['SIDE_FREE']} mm** each side, **{v['BACK_FREE']} mm** behind (the MedusaHC docks go there).",
            "", "✅ **Check:** lay every piece out by key letter and label it with tape (\"C " + str(L["C"]) + "\"). Measure the uncut pieces now: "
            "if one is more than 1 mm off this table, write the real length down and use it in Chapter 4.",
            "", f"[Full length table for all seven frames](../../../design/sizes/FRAME-LENGTHS.md)"]
    return head + "\n".join(tbl + rails + tail) + "\n"


def ch01(v, j):
    printed = OrderedDict()
    for s in j["steps"]:
        for p in s["new"]:
            if p["key"] in PRINTED:
                printed[p["label"]] = printed.get(p["label"], 0) + p["qty"]
    printed["Bed Hold L/R (Duender) under Andizzle's L/R triple-Z bed mounts"] = 2
    printed["F688ZZ top bearing bracket"] = 3
    printed["Adjuster wheel (bed)"] = 4
    rows = [f"| {k} | {n} |" for k, n in printed.items()]
    return (f"# Chapter 1: Safety, tools and printing the parts\n\n{nav(1, v)}\n\n"
            "## Step 1.1: Safety\n\n"
            "- **Saw:** eye protection, clamp the bar, never hold a short offcut by hand. Aluminium chips are sharp: brush, don't wipe.\n"
            "- **Rails:** keep the carriages on their rails (tape the ends). Lost balls ruin a carriage.\n"
            "- **No mains in this manual.** Nothing here is plugged in.\n\n"
            "## Step 1.2: Tools\n\n"
            "| Tool | Use |\n|---|---|\n"
            "| Mitre or cold-cut saw, non-ferrous blade, length stop | cutting extrusions (Chapter 4) |\n"
            "| Abrasive cut-off wheel | cutting rails |\n"
            "| Engineer's square, steel rule, calipers, file | squaring and facing |\n"
            "| M5 tap + handle | tapping extrusion ends |\n"
            "| Hex keys 2, 2.5, 3; soldering iron for heat-set inserts | assembly |\n\n"
            "## Step 1.3: Print the parts\n\n"
            "Material: **ABS or ASA** for parts near the motors and bed; PETG is fine for the rest. **5 walls, 40 %+ infill** for every part that carries load "
            "(Sergei prints MedusaHC's functional parts in ABS at 98 % infill).\n\n"
            "| Printed part (from the model) | Qty |\n|---|---|\n" + "\n".join(rows) + "\n\n"
            "Sources: Andizzle's CR10 Duender files (Z parts, T-brackets), Sergei's MedusaHC V0.2 (`STLs/`: Y front/back blocks, tensioners, "
            "`V-Back Mounts/X-Back 1/2 MGN9H L/R`, `Toolhead/MGN9H Mount Main`), the Duender repo (bed holders). The middle mount for the 400 and "
            "500 is a remix (Chapter 5).\n\n"
            "## Step 1.4: Fit tests\n\n"
            "Before printing everything, print one T-bracket and one bed holder. Check: an M5 T-nut slides in its slot, an F688ZZ bearing presses "
            "into the top bearing bracket and stays, heat-set inserts go in straight.\n\n"
            "✅ **Check:** every part on the list printed and fit-tested.\n")


def totals(text):
    """The 'Chapter totals' of a chapter: its table, or (chapter 4) its one-line count."""
    m = re.search(r"\*\*Chapter totals[^\n]*?\*\*:?([^\n]*)\n", text)
    if not m: return None
    if m.group(1).strip(): return m.group(1).strip()
    lines = text[m.end():].lstrip("\n").splitlines()
    end = next((i for i, l in enumerate(lines) if not l.startswith("|")), len(lines))
    return "\n".join(lines[:end])


def ch02(v, chapters):
    files = {c[0]: f"{c[0]}-{c[1]}-mgn9x.md" for c in CHAPTERS if c[1]}
    titles = {c[0]: c[2] for c in CHAPTERS}
    out = [f"# Chapter 2: Parts list\n\n{nav(2, v)}\n",
           "What each chapter uses, from its **Chapter totals** (the same tables as in the chapters). The extrusions and rails are in "
           "[Chapter 0](00-extrusions-mgn9x.md), the printed parts in [Chapter 1](01-tools-printing-mgn9x.md).\n"]
    for n, text in chapters:
        t = totals(text)
        if t:
            out += [f"## Chapter {int(n)}: [{titles[n]}]({files[n]})\n", t, ""]
    out += ["⚠️ Buy **10 % spare** T-nuts and M3/M5 screws: some always vanish.", ""]
    return "\n".join(out)


def ch03(fid, f, v, L, cut):
    head = f"# Chapter 3: {v['CH3_TITLE']}\n\n{nav(3, v)}\n\n"
    if f.get("donor"):
        n = f.get("donors_needed", 1)
        take = [f"| ☐ | {k} {NAMES[k]} | {f['source'][k][0]} |" for k in QTY if k in f["source"] and not f["source"][k][1]]
        cutp = [f"| ☐ | {k} {NAMES[k]} → **{L[k]}** | {f['source'][k][0]} |" for k in QTY if k in f["source"] and f["source"][k][1]]
        return head + "\n".join([
            f"This frame uses **{n} × {f['donor']}**. Keep any **working** printer intact for troubleshooting: strip only a donor that's already "
            "out of service.", "",
            "## Step 3.1: Check the donor (checklist)", "",
            f"Tick each piece as it comes off. Lengths are **per printer**; {'you have ' + str(n) + ' printers, so double the quantities' if n > 1 else 'one printer'}. "
            f"Where a length is marked *(est.)* or *measure*, measure it before you plan any cut.", "",
            "| ☐ | Part | Profile | Length (mm) | Qty | Where on the donor | Becomes in this frame |", "|---|---|---|---|---|---|---|",
            *[f"| ☐ | {p_} | {pr} | {ln} | {q} | {w} | {u} |" for p_, pr, ln, q, w, u in f.get("bom", [])], "",
            "**Other parts to keep:**", "",
            "| ☐ | Part | Used here |", "|---|---|---|",
            "| ☐ | NEMA17 motors (X, Y, Z, extruder) | **5** in total: 3 × Z (**J**, Chapter 5) and 2 × A/B (**R**, Chapter 6) |",
            ("| ☐ | Lead screws, each with its nut and coupler | 3 (**K**, **V**, Chapter 5) from the donors; keep the 4th as a spare |" if n > 1 else
             "| ☐ | Lead screws, each with its nut and coupler | 2 (**K**, **V**, Chapter 5); the third is bought to match (Step 3.4) |"),
            f"| ☐ | Bed plate | **N**: {v['BED']} |",
            "| ☐ | Corner brackets, T-nuts, M5 screws | bag by size: Chapter 4 |",
            "| ☐ | Electrics: PSU, board, screen, fans, bed wiring | not in this manual (Step 3.2) |",
            "| ☐ | V-wheels, eccentric nuts, belts, pulleys, hotend, extruder, spool holder | not used: keep as spares |", "",
            "## Step 3.2: Set the electrics aside", "",
            f"Nothing electrical from the donor goes into this manual. The {f['donor']}'s supply is **{f.get('volt', '12V')}**; whether any of its "
            "electrics are reused is decided in the electronics manual. Unplug and bag them: PSU, board, screen, fans, bed wiring.", "",
            "## Step 3.3: Take the extrusions and motion parts", "",
            "1. Take the frame apart: top bar, X gantry, uprights, base, Y beam. **Bag the screws, T-nuts and corner brackets** by size.",
            "2. Remove the **stock motor pulleys** (a printed puller, or carefully with a Dremel). New GT2 pulleys go on the A/B motors; the Z motors need bare shafts.",
            "3. Keep each **lead screw with its nut and coupler** in one bag. Store the screws flat.", "",
            "**Uncut pieces (used at their stock length):**", "", "| ☐ | Piece | From |", "|---|---|---|", *take, "",
            "**Pieces that are cut (Chapter 4, Step 4.1):**", "", "| ☐ | Piece → length | From |", "|---|---|---|", *cutp, "",
            "## Step 3.4: Measure", "",
            "| Measure | Value | Model |", "|---|---|---|",
            f"| Uprights (each) | | {L['C']} |", f"| Base sides (each) | | {L['A']} |", f"| Lead screws: length, lead (8 mm per turn), straight? | | {v['SCREW']} |", "",
            ("1. All three Z screws must have the **same length and lead**: use three from the donors that match; keep the 4th as a spare." if n > 1 else
             "1. All three Z screws must have the **same length and lead**: order the third to match what you measured."),
            "2. If a donor piece is more than 1 mm off the model, write the real length into Chapter 0's table and use it in Chapter 4.", "",
            ("✅ **Check:** every piece labelled with its key letter; the electrics bagged and set aside; three matching screws picked." if n > 1 else
             "✅ **Check:** every piece labelled with its key letter; the electrics bagged and set aside; screws measured and the third ordered."), ""])
    pieces = {"2040": [], "2020": []}
    for k, q in QTY.items():
        if k != "S":
            pieces[PROFILE.get(k, "2020")] += [(k, L[k])] * q
    out = [head, "Every frame piece is cut from new bars: **2040 × 800** and **2020 × 1000**. The X beam (S) is cut last, after measuring (Step 7.4).", ""]
    for prof, stock in (("2040", STOCK_2040), ("2020", STOCK_2020)):
        bars = bar_plan(pieces[prof], stock)
        out += [f"## {prof} × {stock} bars: **{len(bars)}**", "", "| Bar | Pieces | Offcut *(after {KERF} mm cuts)* |".replace("{KERF}", str(KERF)), "|---|---|---|"]
        for i, b in enumerate(bars, 1):
            out.append(f"| {i} | {' + '.join(f'{k} {n}' for k, n in b)} | {stock - sum(n + KERF for _, n in b)} |")
        out.append("")
    out += ["Any donor piece at least as long as a piece here can replace a bar cut: check Chapter 0's lengths against your stock first.", "",
            "✅ **Check:** bars bought; the plan marked on each bar with tape before the first cut.", ""]
    return "\n".join(out)


def readme(fid, f, v, chapter_titles):
    rows = [f"| {n} | [{t}]({fn}) |" for n, t, fn in chapter_titles]
    return "\n".join([
        f"# {f['title']}", "",
        f"{f['intro']}", "",
        "**This manual** builds the frame and everything that moves: extrusions, the triple Z and bed plate, the A/B motors and **MGN9** Y rails, "
        "the X axis (turned to the rear for the MedusaHC docks) and the belts. It ends with a printer that moves freely by hand. "
        "**Not in this manual:** wiring, electronics and Klipper (the electronics manual) and the toolhead and docks (the toolhead manual). "
        "Both are shared by all seven frames.", "",
        "## Chapters", "", "| Ch | Chapter |", "|---|---|", *rows, "",
        "## The frame", "", "| Spec | Value |", "|---|---|",
        f"| Frame outside | {v['W']} × {v['D']} mm, {v['FH']} mm tall |", f"| Bed plate | {v['P']} × {v['P']} |",
        f"| Z | triple Z (Andizzle), T8×8 × {v['SCREW']}, travel {v['ZTRAVEL']} mm *(est.)* |",
        f"| Y | 2 × MGN9 × {v['YR']} (MedusaHC V-Back kit) |", f"| X | 2020 × {v['S']} beam, MGN9 × {v['XR']} on its back face |",
        f"| Docks | MedusaHC V-Back, behind the bed |", "",
        "**How to read the pictures:** new parts of a step are in full colour, earlier ones faded; red callouts carry the key letters used in the tables. "
        f"Model: `cad/designs/duender-large/out/c{v['SIZE']}-duender-3z-mgn9x{v['TAG']}.step`.", "",
        "Real parts: Andizzle's CR10 Duender (GPL-2.0) and Sergei Irbenek's MedusaHC V0.2 (GPL-3.0). Lengths are from the CAD model *(est.)*: measure as you go.", ""])


def build(fid):
    f = FRAMES[fid]
    v, j, L, cut = values(fid, f)
    out = os.path.join(HERE, "editions", f"frame-{fid}")
    os.makedirs(out, exist_ok=True)
    files, texts = [], []
    for i, (n, slug, title) in enumerate(CHAPTERS):
        slug = slug or v["CH3_FILE"]; title = title or v["CH3_TITLE"]
        fn = f"{n}-{slug}-mgn9x.md"
        if n in ("04", "05", "06", "07", "08"):
            t = open(os.path.join(TPL, fn), encoding="utf-8").read()
            t = fill(t, v, fn)
            t = re.sub(r"^\[←.*\]\(README-mgn9x\.md\).*$", nav(i, v), t, count=1, flags=re.M)
            texts.append((n, t))
        files.append((n, title, fn))
    body = {n: t for n, t in texts}
    body["00"] = ch00(fid, f, v, L, cut)
    body["01"] = ch01(v, j)
    body["03"] = ch03(fid, f, v, L, cut)
    body["02"] = ch02(v, texts)
    for n, title, fn in files:
        open(os.path.join(out, fn), "w", encoding="utf-8").write(body[n])
    open(os.path.join(out, "README-mgn9x.md"), "w", encoding="utf-8").write(readme(fid, f, v, files))
    left = [m for n in body for m in re.findall(r"\{[A-Z][A-Z0-9_]*\}", body[n])]
    assert not left, (fid, left)
    print(fid, "->", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    # self-check: the saw kerf counts (two 400s need two 800 bars), first-fit packs where it can
    assert len(bar_plan([("A", 400)] * 2, 800)) == 2 and len(bar_plan([("A", 400), ("B", 390)], 800)) == 1
    for fid in (sys.argv[1:] or FRAMES):
        build(fid)
