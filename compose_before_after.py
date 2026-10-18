"""Before/after composites for the upgrades manual: a 2x2 grid (before | after; front over back) + a header row.
python3 compose_before_after.py   (run from manual/images)"""
from PIL import Image, ImageDraw, ImageFont

FRAMES = [("c300", ""), ("c300", "-cr10"), ("c300", "-cr10v2"), ("c400", ""), ("c400", "-s4"), ("c500", ""), ("c500", "-s5")]
HEAD = 90
try:
    FONT = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
except OSError:
    FONT = ImageFont.load_default()

for size, tag in FRAMES:
    d = f"{size}/lego-mgn9x"
    cells = [[Image.open(f"{d}/step-{s}{tag}-purple{v}.png").convert("RGB") for s in ("pb", "pa")] for v in ("", "-back")]
    w, h = cells[0][0].size
    out = Image.new("RGB", (2 * w, HEAD + 2 * h), "white")
    draw = ImageDraw.Draw(out)
    for col, label in enumerate(("Before", "After (upgrade parts in purple)")):
        tw = draw.textlength(label, font=FONT)
        draw.text((col * w + (w - tw) / 2, (HEAD - 48) / 2), label, fill="black", font=FONT)
    for row in range(2):
        for col in range(2):
            out.paste(cells[row][col].resize((w, h)), (col * w, HEAD + row * h))
    out.save(f"{d}/before-after{tag}-purple.png", optimize=True)
    print(f"{d}/before-after{tag}-purple.png", out.size)
