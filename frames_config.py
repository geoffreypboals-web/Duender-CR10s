"""T-021 frame manuals: what each of the seven frames is and where every piece comes from.

Used by make_frame_editions.py. One entry per frame manual (manual/editions/frame-<id>/). `src` is the full build
manual whose frame chapter (04-frame-mgn9x.md) is the starting text; `tag` is the CAD model's file suffix
(cad/designs/duender-large/out/c<size>-mgn9x-steps<tag>.json and the pictures step-*<tag>.png).

`source` per key letter: (where that piece comes from, cut?). Cut frames have no `source`: everything is cut from
new bars (STOCK_2040 / STOCK_2020), with a bar plan worked out by the script.
"""

STOCK_2040, STOCK_2020 = 800, 1000          # new bars: QNK 2040 x 800 (owner, 2026-10-12), 2020 x 1000

FRAMES = {
    "c300-cut": dict(
        size="300", src="c300-v3", tag="", donor=None,
        title="C300 frame, cut to size",
        intro="Every extrusion is cut to length from new stock (2040 × 800 and 2020 × 1000 bars), or from longer donor "
              "pieces. The lengths are the official Creality CR-10's, so two original CR-10s give this frame without "
              "cutting: see the [CR-10 frame manual](../frame-c300-cr10/README-mgn9x.md)."),
    "c300-cr10": dict(
        bom=[("Upright", "2040", "550", 2, "standing at each side, bolted to the base sides", "**C** upright"),
                 ("Base side", "2040", "460", 2, "the two outer floor rails, front to back", "**A** lower / **D** upper base side"),
                 ("Base cross member", "2020", "400", 2, "the front and back ends of the base", "**B**, **G**, **U** (and **L**, cut)"),
                 ("Top bar", "2020", "400", 1, "across the tops of the uprights", "as the cross members"),
                 ("X gantry", "2020", "415", 1, "across the uprights, carries the hotend", "**E** rear side Z carrier"),
                 ("Y beam", "2040", "509", 1, "the centre rail of the base, front to back; the bed rolls on it", "**F** Y side")],
        
        size="300", src="c300-v3", tag="-cr10", donor="CR-10", donors_needed=2,
        title="C300 frame from two CR-10s (original)",
        intro="Two original Creality CR-10s give every frame extrusion at its stock length, except the short front "
              "stub and the X beam. The lengths are from Creality's own CAD files, the most reliable source.",
        lengths_source="the official Creality CR-10 CAD (`cad/donors/creality-official/source/CR-10`)",
        source={"A": ("CR-10 base 2040 × 460 (2 per printer)", False),
                "D": ("CR-10 base 2040 × 460 (as A)", False),
                "B": ("CR-10 2020 × 400 (3 per printer: 2 base cross members + the top bar)", False),
                "G": ("CR-10 2020 × 400 (as B)", False),
                "U": ("CR-10 2020 × 400 (the 5th of the 6)", False),
                "C": ("CR-10 upright 2040 × 550 (2 per printer)", False),
                "E": ("CR-10 X gantry 2020 × 415 (1 per printer)", False),
                "F": ("CR-10 Y beam 2040 × 509 (1 per printer)", False),
                "L": ("cut from the 6th CR-10 2020 × 400", True),
                "S": ("cut from a new 2020 × 1000 (measure first, Step 7.4)", True)}),
    "c300-cr10v2": dict(
        bom=[("Upright", "2040", "560", 2, "standing at each side, bolted to the base sides", "**C** upright (2 of the 4)"),
                 ("Base side", "2040", "480", 2, "the two outer floor rails, front to back", "**A** lower / **D** upper base side"),
                 ("Base cross member", "2020", "400", 2, "the front and back ends of the base", "**B**, **G**"),
                 ("Top bar", "2020", "400", 1, "across the tops of the uprights", "as the cross members"),
                 ("X gantry", "2020", "410", 1, "across the uprights, carries the hotend", "**U** front Z carrier; the 2nd printer's → **L** (cut)"),
                 ("Y beam", "2040", "500 (with a cutout)", 1, "the centre rail of the base, front to back", "not used (spare)")],
        
        size="300", src="c300-v3", tag="-cr10v2", donor="CR-10 V2", donors_needed=2,
        title="C300 frame from two CR-10 V2s",
        intro="The CR-10 V2 kit gives most frame extrusions at their stock length; two of the four uprights are cut from new stock. The V2's 560 uprights and 480 "
              "base sides make this frame 10 mm taller and 20 mm deeper than the CR-10 one.",
        lengths_source="measured on the donor printers", volt="24V",   # owner table 2026-10-17
        source={"A": ("V2 base 2040 × 480 (2 per printer)", False),
                "D": ("V2 base 2040 × 480 (as A)", False),
                "B": ("V2 2020 × 400 (3 per printer: 2 base + the top bar)", False),
                "G": ("V2 2020 × 400 (as B)", False),
                "C": ("2 × V2 upright 2040 × 560, + 2 cut to 560 from a new 2040 × 800", True),   # owner 2026-10-16: two 560s short
                "U": ("V2 X gantry 2020 × 410 (1 per printer)", False),
                "E": ("cut from a new 2020 × 1000 (2 per bar): the V2 has no 2020 this long", True),
                "F": ("a straight 2040 × 520 from stock, or cut from a 2040 × 800. **Not on the V2**: its Y beam is "
                      "500, with a cutout", True),
                "L": ("cut from the 2nd V2 X gantry (410)", True),
                "S": ("cut from a new 2020 × 1000 (measure first, Step 7.4)", True)}),
    "c400-cut": dict(
        size="400", src="c400-s4", tag="", donor=None,
        title="C400 frame, cut to size",
        intro="Every extrusion is cut to length from new stock (2040 × 800 and 2020 × 1000 bars), or from longer donor "
              "pieces. A CR-10 S4 gives the uprights, base sides and Y sides uncut: see the "
              "[CR-10 S4 frame manual](../frame-c400-cr10s4/README-mgn9x.md)."),
    "c400-cr10s4": dict(
        bom=[("Upright", "2040", "550", 2, "standing at each side, bolted to the base sides", "**C** upright (2 of the 4)"),
                 ("Base side", "2040", "560", 2, "the two outer floor rails, front to back", "**A** lower base side (2 of 4)"),
                 ("Y rail (base centre)", "2040", "600", 2, "the two centre rails on the base, full depth; the bed's wheels run on them", "**F** Y side"),
                 ("Base cross member", "2020", "600", 2, "the front and back ends of the base, full width", "**B** / **G**, cut to 500"),
                 ("Top bar", "2020", "500", 1, "across the tops of the uprights", "**B** / **G**"),
                 ("X gantry", "2020", "520", 1, "across the uprights, carries the hotend", "**B** / **G**, cut to 500")],
        
        size="400", src="c400-s4", tag="-s4", donor="CR-10 S4", donors_needed=1,
        title="C400 frame from a CR-10 S4",
        intro="One Creality CR-10 S4 gives two uprights, two base sides and both Y sides at their stock length. Two more "
              "2040 × 560 base sides and the Z carriers fit uncut from CR-10 or V2 pieces. The 2020 cross members are cut "
              "from the S4's own 2020s.",
        lengths_source="measured on the donor printer",   # owner table 2026-10-17
        source={"A": ("2 × S4 base 2040 × 560, + 2 × 2040 × 560 from stock (CR-10 V2 uprights are 560)", False),
                "D": ("2040 × 560 (as A)", False),
                "C": ("2 × S4 upright 2040 × 550, + 2 cut to 550 from a longer 2040 (a V2 560, or a 2040 × 800)", True),
                "F": ("S4 base 2040 × 600 (2): uncut, flush with the frame at both ends", False),
                "B": ("the S4 top bar 2020 × 500 (1), + 3 cut to 500 from the S4's 2 × 2020 × 600 and its X gantry 520", True),
                "G": ("2020 × 500 (as B)", True),
                "E": ("CR-10 X gantry 2020 × 415 (2), uncut; or cut from 2020 × 1000", False),
                "U": ("CR-10 2020 × 400 (1), uncut; or cut from 2020 × 1000", False),
                "L": ("cut from a 2020 offcut", True),
                "S": ("cut from a new 2020 × 1000 (measure first, Step 7.4)", True)}),
    "c500-cut": dict(
        size="500", src="c500-s5", tag="", donor=None,
        title="C500 frame, cut to size",
        intro="Every extrusion is cut to length from new stock (2040 × 800 and 2020 × 1000 bars). Two CR-10 S5s give almost "
              "the whole frame uncut: see the [CR-10 S5 frame manual](../frame-c500-cr10s5/README-mgn9x.md)."),
    "c500-cr10s5": dict(
        bom=[("Upright", "2040", "650", 2, "standing at each side, bolted to the base sides", "**C** upright (2 of the 4)"),
                 ("Base side", "2040", "660", 2, "the two outer floor rails, front to back, between the cross members", "**A** / **D** base side (2 of the 4), uncut"),
                 ("Y rail (base centre)", "2040", "700", 2, "the two centre rails on top of the cross members; the bed's wheels run on them", "**F** Y side (1 of the 2), uncut; the second printer's two are spare"),
                 ("Base cross member", "2020", "600", 2, "the front and back ends of the base, full width", "**B** / **G**, uncut"),
                 ("Top bar", "2020", "600", 1, "across the tops of the uprights", "**B** / **G**, **U** (cut to 500) or **S** (cut to 571)"),
                 ("X gantry", "2020", "615", 1, "across the uprights above the bed, carries the hotend", "**E** rear side Z carrier, cut to 515"),
                 ("Lead screw (T8)", "—", "615", 2, "Z, one each side", "**K** / **V** lead screws, uncut (4 from 2 printers: 3 used, 1 spare)"),
                 ("Bed frame, front/back", "2020", "439.6", 2, "under the bed plate, bolted into a square", "keep with the bed (Chapter 5); or **L**, cut"),
                 ("Bed frame, sides", "2020", "399.6", 2, "under the bed plate, between the front/back bars", "keep with the bed (Chapter 5)")],
        size="500", src="c500-s5", tag="-s5", donor="CR-10 S5", donors_needed=2,
        title="C500 frame from two CR-10 S5s",
        intro="Two Creality CR-10 S5s give every upright, base side, Y side, base member and top brace at their stock length. "
              "Only the two rear Z carriers, the front Z carrier, the X beam and the front Z stub are cut, all from the S5's own "
              "2020s. The frame is 640 × 700, the same footprint as the cut C500, and its 650 uprights make it 35 mm lower.",
        lengths_source="measured on two stripped CR-10 S5s (`design/sizes/S5-HARVESTED.md`). Which piece is which "
                       "(660 base sides, 700 Y rails) follows the S5 layout: *check yours before cutting*",   # owner harvest 2026-10-18
        source={"A": ("S5 base side 2040 × 660, uncut (2 per printer)", False),
                "D": ("S5 base side 2040 × 660, uncut (as A)", False),
                "C": ("S5 upright 2040 × 650, uncut (2 per printer)", False),
                "B": ("S5 2020 × 600, uncut (base cross members)", False),
                "G": ("S5 2020 × 600, uncut (top bars)", False),
                "F": ("S5 Y rail 2040 × 700, uncut, flush front and back (2 spare)", False),
                "E": ("cut from the two S5 X gantries (2020 × 615)", True),
                "U": ("cut from the 5th S5 2020 × 600", True),
                "L": ("cut from an S5 bed-frame 2020 × 439.6, or any 2020 offcut 150 or longer", True),
                "S": ("cut from the 6th S5 2020 × 600 (measure first, Step 7.4)", True)}),
}
