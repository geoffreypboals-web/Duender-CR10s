# Combined PDF manuals (Lego edition, MGN9 X)

One PDF per printer, made from the 🧱 `-mgn9x` chapters (T-015, owner 2026-10-14):

- [C300-V3](c300-v3-mgn9x.pdf): from `manual/editions/c300-v3/`
- [C400-S4](c400-s4-mgn9x.pdf): from `manual/editions/c400-s4/`
- [C500-S5](c500-s5-mgn9x.pdf): from `manual/editions/c500-s5/`
- [Upgrades](upgrades-mgn9x.pdf) (all sizes): from `manual/editions/upgrades/`

Each PDF has a cover, a contents page with page numbers, the edition's `README-mgn9x.md`, then every chapter in the
order of its contents table (Chapter 0 extrusions, 1–12, Appendix A), all clean `-mgn9x` files. Build history and owner
questions are not printed: they're in [`../REVIEW-NOTES-mgn9x.md`](../REVIEW-NOTES-mgn9x.md). The build prints any history wording it finds (`history words in the text`) and any link without a target. Links between chapters jump inside the PDF. Links to files outside the PDF go
to GitHub (default branch).

**The PDFs are snapshots.** Rebuild them after editing any chapter (about 15 s per edition):

```bash
python3 -m venv /tmp/pdfenv && /tmp/pdfenv/bin/pip install weasyprint markdown beautifulsoup4
cd /home/gboals/Toolchanger-Research && /tmp/pdfenv/bin/python manual/build_pdf.py   # or: ... build_pdf.py c300-v3
```
