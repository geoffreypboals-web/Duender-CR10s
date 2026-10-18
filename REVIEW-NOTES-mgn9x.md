# Review notes for the MGN9 X manuals (not printed)

Owner-facing notes that were taken out of the printed manuals on 2026-10-14 (owner: "references to the iterations should not be included; if information is important add it in or add to the appendix"). The build manuals are `editions/<edition>/README-mgn9x.md` and the chapters it lists; the PDFs are built from those by `build_pdf.py` (`pdf/`). This file and [MGN9X-UPDATE.md](MGN9X-UPDATE.md) keep the history.

## Owner decisions (confirmed)

- 2026-10-12: triple Z (Andizzle) for all sizes.
- 2026-10-13: **X only on MGN9** (designer: MGN12 too heavy on the moving gantry); Y and Z stay MGN12H.
- 2026-10-13: **2020 X beam** on all sizes (2040 + MGN9 is the fallback if it rings).
- 2026-10-14: C300 Step 3.5 corrected: base sides one above the other (z 0–20 and 134.9–154.9, measured in `duocr10-full.step`), not "20 mm apart".
- 2026-10-15: **no printed stand-ins for extrusion.** Leave off `20mm-sapcer-cr10-duo`; designs use correct-length extrusion, never a printed part in its place. Andizzle's `front-stabilzer` is his printed front Z stub (in `duocr10-full.step`: 20 × 20 × 154 at the front centre, about 49,000 mm³ against about 27,000 for aluminium 2020), so it's dropped too: the stub is a real 2020 × 150, and the front carrier top is held by a T-bracket on the front face (T-brackets: C300/C500 7, C400 5).
- 2026-10-14: belts drawn in 4 colours (teeth brown, back purple/green) and stretched with the carriage; extra close-ups F4/Z2/B1; inline code printed in the paragraph font; extrusion overview page (Chapter 0).

## Open questions for the owner

- ❓ **Y plate (C400/C500).** The Z3 pictures show Andizzle's stack with a Y plate under the bed; the C400/C500 text keeps it optional (C500: bed straight on the 4 support points). The printed text follows the text and says the picture shows it fitted. Decide: Y plate or not (bed supports: owner's call).
- ❓ **Frame order (C300).** The printed C300 frame chapter builds in the picture order (ring, uprights, upper sides…); the original chapter follows the Ender manual (U-shaped side frames first). Keep only the picture order?
- ❓ **T-brackets.** Andizzle's model has 5 printed T-brackets on the outside faces (foot and top of each rear carrier, front column top). The C300/C500 chapters fit **7** (2 feet + 4 tops + 1 front carrier top); the C400 chapter fits **5** (4 at the tops, one of them optionally moved to the foot, + 1 front). Make the three editions the same?
- ✅ **`20mm-sapcer-cr10-duo`**: left off (owner, 2026-10-15).
- ❓ **Sherpa Mini licence** is non-commercial (Annex). Fine for this personal project; it conflicts with the "commercial use allowed" rule used for software tools, if that rule should also cover printed parts.
- ❓ **MGN15 X option (C500).** Removed from the C500 parts list: it contradicts the light-gantry decision. Restore only if the 2020 + MGN9 gantry rings badly.

- ❓ **Frame braces (stiffness check, 2026-10-15).** Plain frames sway 45–95 µm against the bed at 10 m/s² and their lowest modes are 8–13 Hz (cautious joint estimate). Side diagonals + back X + top corner gussets bring that to 3–9 µm. Add them to the model and manuals (T-018)? All improvements by area (incl. rails, X beam, belts, bed supports): [design/reviews/frame-improvements-mgn9x.md](../design/reviews/frame-improvements-mgn9x.md).
- ❓ **Bed supports (stiffness check).** 2040 Z carriers + front-foot gussets (C300/C400 bed modes to 31–41 Hz; C500 about 22 Hz), and a metal spine on the C400 middle mount (Andizzle's arms sag 0.6–1.5 mm at 400 size, 1.0–2.5 mm at 500). Owner's call.

## Upgrades (2026-10-15): decisions for the owner

Upgrade chapter draft: [`editions/upgrades/U-frame-z-upgrades-mgn9x.md`](editions/upgrades/U-frame-z-upgrades-mgn9x.md); plan for the three manuals and the decision table: [`UPGRADES-PLAN-mgn9x.md`](UPGRADES-PLAN-mgn9x.md) §1. In short: put the standard set into the main build? extra upper base side in 2020 or 2040? back X or panel? front corner gussets vs the docks? 🛏 2040 rear Z carriers and the middle-mount spine? The chapter was drafted by the local AI (qwen3.6:27b) from a facts sheet and checked by Claude Code; no pictures yet.

## Where the printed text now follows the model (the original chapters said otherwise)

| Item | Original text | Printed manual (from the real-part model) |
|---|---|---|
| Side Z motor mounts | on the carrier ends / upper base side | on the **lower base sides**, 336 / 436 / 536 mm from the front; motors end ~2 mm above the table, so the frame needs feet |
| Upper-base-side spacer blocks (C400/C500) | 135 mm | **115 mm** (they stand on the lower base side) |
| C300 Z rails | 3 × same length, 25 mm above the carrier bottom (photo) | **2 × 400 + 1 × 385**, 7 mm above the carrier bottom / stub joint, 8 mm below the top |
| C300 front Z stub | 154 | **150** (154 also works) |
| Y rail ends | centred, ~20 mm each end | front end 7 mm behind the Y side front; back end 52 mm (C300: 72) short of the frame back |
| Toolhead carriage screws | M3×10 | **M3×6** (MGN9H threads ~3 mm deep) |
| Fastener totals (C300 BOM) | 28 brackets, 92 M5×8, 79 M5 T-nuts | 38, 111, 123 *(est.)*: the picture-order frame brackets every joint |
| C300 printed T-brackets | 1 | 6 |
| Chapter 8 | Step 8.1 only (rest "as the original") | complete chapter (Steps 8.2–8.9 merged from the original) |

## Proposed by Claude Code (not confirmed)

- Close-up framing: F4 and Z2 close-ups show the left rear corner only.
- Belt colours: A (lower) dark brown teeth / purple back; B (upper) light brown teeth / green back.
- Where the model and an original text disagree on a position, the printed manual follows the model (table above).
