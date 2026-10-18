# Plan: putting the upgrades into the C300 / C400 / C500 manuals (T-018)

**Not printed** (owner-facing, like `REVIEW-NOTES-mgn9x.md`). The upgrades themselves are in one manual-style chapter: [`editions/upgrades/U-frame-z-upgrades-mgn9x.md`](editions/upgrades/U-frame-z-upgrades-mgn9x.md) (PDF: `pdf/upgrades-mgn9x.pdf`). The numbers behind it: [`design/reviews/frame-improvements-mgn9x.md`](../design/reviews/frame-improvements-mgn9x.md) §11, `cad/designs/duender-large/out/upgrade-manual-set.md` (`python3 frame_stiffness.py d-manual`).
**Status:** plan only, waiting for the owner to pick the set (below). *Decision (proposed by Claude Code)* throughout.

## 1. Owner decisions first

**Changed 2026-10-15 (owner):** no long diagonals. The upgrade is now gusset brackets at every joint + horizontal bars (extra upper base sides, low front bar, two back bars) + optional panels; review §12. Rows below that mention diagonals, the back X or gussets plates are superseded: the questions now are **panels (none / base box / + back / all)**, the **gusset bracket** model (it must reach about 20 kN·m/rad: check with the push test), and the 🛏 items.


| # | Decision | Proposed | Why |
|---|---|---|---|
| 1 | The standard set (base-box diagonals, extra upper base sides, low front bar, side diagonals, back brace, top gussets, joints, rails at every hole) goes **into the main build**, not just the upgrade chapter | yes | no part changes, only extra extrusion and brackets; lowest mode 10 / 9 / 6 → 35 / 31 / 23 Hz |
| 2 | Extra upper base side in **2020** (not 2040 on edge) | 2020 | as stiff here (C300 42 vs 41 Hz), lighter, fits the outer half exactly; 2040 on edge also fine if that's the spare |
| 3 | Back brace: **X** or **panel** | panel on the C500 (it also shields the electronics), X on the C300/C400 | equal stiffness |
| 4 | Front corner gusset plates (FG) | after the MedusaHC dock layout is fixed | +3–5 Hz, but they sit where the docks hang |
| 5 | 🛏 2040 rear Z carriers + front-foot gussets | owner's call (bed support) | +8 / +7 / +4 Hz on top of the set; needs remixed Z rail and motor mounts |
| 6 | 🛏 aluminium spine under the middle mount | owner's call (bed support); the C500 manual already asks for a metal spine | front corner sag 0.33 / 0.58 / 0.98 mm → 2 / 10 / 34 µm |
| 7 | 2040 X beam, 9 mm belts | keep as optional | reopen earlier choices (weight; Duender parts are for 6 mm belts) |

## 2. Model and pictures (before any manual text)

**Done for the upgrade chapter (2026-10-15):** items 1, 2 and 4: `UPGRADES=1` in `build_lego_mgn9_v2.py` (STEP `out/c<size>-duender-3z-mgn9x-upg.step`, pictures `manual/images/c<size>/lego-mgn9x/step-u*-upg.png`, collision reports `out/c<size>-upgrades-collisions.md`: none). Still open: item 3 (bracket fit per angle), item 5 (re-run the stiffness numbers on the moved brace ends), and the pictures for the main manuals' frame chapters.

1. **New version of the model script**, original untouched: `build_lego_mgn9_v2.py` gets an `UPGRADES=1` switch (default output stays byte-identical), adding LD, LB, LF, XD1/XD2, FB, SD, BX (or the back panel), TG as real-size extrusions/plates at the positions in the cut list. Output: `out/c<size>-duender-3z-mgn9x-v3.step`.
2. **Collision check in the model**, with the bed at the bottom and top of its travel: XD vs the rear Z carriage and bed holder; SD (outside face) over XD; LD/LB vs the rear Z motor mounts (J2) and lead screws; LF vs the front Z motor and the front stub holder; FB vs the bed at its lowest; BX vs the A/B motor blocks and electronics plate; TG vs the toolhead path; FG vs the MedusaHC docks. Fix positions (heights are flexible within the bands in §11) and record them.
3. **Hinge-bracket and corner-bracket fit:** confirm the brackets for each diagonal angle (they differ per size) and the bracket positions at the carrier (front/back faces only, never the rail face).
4. **Lego pictures** in the existing style (`manual/images/c<size>/lego-mgn9x/`): one per new step (base box, extra upper base sides + front bar, upper braces, gussets) plus detail views of the carrier joint (XD at the carrier) and the front column (FB). Look at every picture before using it.
5. Re-run `extract_stiffness_inputs.py` on the v3 model and `frame_stiffness.py d-manual`: the numbers in the chapter must match the built geometry.

## 3. Manual changes per chapter (each edition: c300-v3, c400-s4, c500-s5)

| Chapter (`-mgn9x`) | Change |
|---|---|
| `00-extrusions` | add the new pieces to the cut list and the "salvaged vs buy" table (2020 for LD, LB, LF, SD, BX, XD, FB; per size from the upgrade chapter's cut list) |
| `02-parts-list` | add 22 hinge brackets, 24 corner brackets, 108 M5×8 + 108 T-nuts, 4 (+2) gusset plates, extra M3 screws/T-nuts for the rails; for a new build most T-nuts are ordinary ones loaded in Chapter 4 (only a few drop-ins) |
| `04-frame` | Step 4.6: load the extra T-nuts into the uprights (XD, FB, diagonal brackets) while the ends are open. New steps after 4.10: extra upper base sides (XD) and low front bar (FB). New steps after 4.13 (frame square): base-box diagonals, side diagonals, back brace, top gussets. Blind joints become the standard joint where the model allows |
| `05-z-axis-bed` | Z rails bolted at **every** hole (was every other); new check: bed carriage clears XD at full travel, bed clears FB at the bottom |
| `07-x-axis` | X rail bolted at every hole (18 screws, was 9) |
| `11-first-start-klipper` | push test (before/after values) and the expected `SHAPER_CALIBRATE` range per size; the full procedure goes in the testing book (T-017) |
| `12-medusahc-ready` | front corner gussets only if the dock layout leaves room |
| `A-sources` | add the stiffness study as a source |
| `README` | frame line: "braced" + the new lowest-mode estimate |

Rules (owner): no build history in the printed chapters; owner notes stay in `REVIEW-NOTES-mgn9x.md`; originals untouched (the `-mgn9x` files are the working drafts and change in place); full absolute paths in reports.

## 4. Build and check

1. `manual/build_pdf.py` for the three editions and `upgrades` (add `upgrades` to `EDITIONS` once its pictures exist): history words none, dead links 0.
2. Hand the text work to the local AI where it can do it (owner's rule): `cad/designs/duender-large/local_ai.py prompt …` drafts each changed step from a facts sheet; `local_ai.py check …` cross-checks numbers; Claude Code verifies every number against the model output before commit.
3. Test-build check list for the first printer: push test before and after, `SHAPER_CALIBRATE` peaks vs the table, then feed the measured joint stiffness back into `frame_stiffness.py` (`KJ_CASES`).

## 5. Order of work

Owner decisions (§1) → model `UPGRADES=1` + collision check (§2.1–2.3) → re-run the numbers (§2.5) → pictures (§2.4) → upgrade chapter pictures + PDF → the three manuals (§3) → PDFs (§4.1) → copy to `D:\Toolchanger-Research` on mastercomputerb.
