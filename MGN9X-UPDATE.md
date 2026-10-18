# MGN9 X gantry update (T-012, 2026-10-13)

> **Confirmed by the owner (2026-10-13): X only on MGN9; Y and Z stay MGN12H.** **X beam: 2020 for all sizes** (owner, 2026-10-13).

The owner's decision, on the original designer's advice: **the X gantry runs on MGN9**, because MGN12 is too heavy on the moving axis. New chapter versions and Lego-style pictures sit next to the originals; nothing original was overwritten.

| Edition | Start here (Lego edition, full contents) |
|---|---|
| C500-S5 (build priority 1) | [editions/c500-s5/README-mgn9x.md](editions/c500-s5/README-mgn9x.md) |
| C400-S4 | [editions/c400-s4/README-mgn9x.md](editions/c400-s4/README-mgn9x.md) |
| C300-V3 | [editions/c300-v3/README-mgn9x.md](editions/c300-v3/README-mgn9x.md) |

## Lego editions (T-014, 2026-10-14)

Each edition now has a 🧱 **Lego version** of every chapter that has step pictures, next to the original:
`02-parts-list-mgn9x` (+ a tick list of every lettered part), `04-frame-mgn9x` (F1–F6), `05-z-axis-bed-mgn9x` (Z1–Z3),
`06-ab-motors-mgn9x` (G1), `07-x-axis-mgn9x` (G2, every step written out), `08-toolhead-mgn9x`, `09-belts-mgn9x` (B1 and
the complete machine). Every one of the 16 pictures per size is in its step, with an *In the picture* line whose keys match
the red callouts. Navigation runs through the 🧱 chapters. Chapters 1, 3 and 10–12 are unchanged.

Checked against the real-part model (`out/c<size>-duender-3z-mgn9x.step`) and marked **🔧 From the model** in the text:
- Andizzle's **side Z motor mounts sit on the lower base sides** (20–41 mm up), not on the carrier ends; the Z motors end
  about **2 mm above the table**, so the frame needs feet or its base case.
- The upper base sides are at **135–155 mm**: the spacer blocks standing on the lower sides are **115 mm** (the C400/C500
  texts said 135).
- Andizzle's model has **5 T-brackets** on the outside faces: foot and top of each rear carrier, and the front column top.
- The **Y rails** start 7 mm behind the Y sides' front ends and stop 52 mm short of the back (C300: 72 mm), clear of the AB blocks.
- The **belt chapter** now uses the MGN9H toolhead carriage with **M3×6** screws (the original said M3×10, which would bottom out).

Open questions for the owner are listed at the end of each edition's README-mgn9x (❓).

Model and renders: `cad/designs/duender-large/build_lego_mgn9.py` (from `extract_lego_lib.py`'s real-part library).

## Clean build manuals and PDFs (2026-10-14)

The printed manuals no longer carry build history (owner, 2026-10-14). Each edition's `README-mgn9x.md` lists clean chapters only: the 🧱 chapters were rewritten as plain build text, chapters 1, 3 and 10–12 got clean `-mgn9x` copies, chapter 2 is a complete parts list, chapter 8 is complete, a new **Chapter 0** shows every extrusion with its length, and Appendix A (`A-sources-mgn9x.md`) has the design notes, checks and credits. The owner questions, decisions and the "model vs original" table moved to [REVIEW-NOTES-mgn9x.md](REVIEW-NOTES-mgn9x.md). PDFs: [pdf/](pdf/README.md).
