"""Generate the extension icon (icon.png) in the Purplish theme colors.

Renders at 4x and downsamples with LANCZOS for clean anti-aliasing.
Palette: purple #8345ff, coral #f78166, near-black #0d0d0d background.
"""
from PIL import Image, ImageDraw, ImageFilter, ImageChops

S = 4                      # supersample factor
W = 256 * S               # working size
PURPLE = (131, 69, 255)   # #8345ff
CORAL = (247, 129, 102)   # #f78166

def disc(cx, cy, r, color):
    layer = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    return layer

# --- dark rounded tile with a subtle top-down gradient -------------------
bg = Image.new("RGBA", (W, W))
bgd = ImageDraw.Draw(bg)
top, bot = (21, 16, 31), (8, 8, 8)          # #15101f -> #080808
for y in range(W):
    t = y / (W - 1)
    c = tuple(int(a * (1 - t) + b * t) for a, b in zip(top, bot)) + (255,)
    bgd.line([(0, y), (W, y)], fill=c)

mask = Image.new("L", (W, W), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 1, W - 1], radius=60 * S, fill=255)

tile = Image.new("RGBA", (W, W), (0, 0, 0, 0))
tile.paste(bg, (0, 0), mask)

# subtle inner border for definition on dark backgrounds
ImageDraw.Draw(tile).rounded_rectangle(
    [2 * S, 2 * S, W - 1 - 2 * S, W - 1 - 2 * S],
    radius=58 * S, outline=(60, 45, 90, 110), width=2 * S,
)

# --- color circles (palette motif) ---------------------------------------
content = Image.new("RGBA", (W, W), (0, 0, 0, 0))
# soft glow behind the purple circle
glow = disc(112 * S, 120 * S, 74 * S, PURPLE + (130,)).filter(ImageFilter.GaussianBlur(20 * S))
content = Image.alpha_composite(content, glow)
content = Image.alpha_composite(content, disc(112 * S, 120 * S, 72 * S, PURPLE + (255,)))
content = Image.alpha_composite(content, disc(162 * S, 152 * S, 52 * S, CORAL + (230,)))
# specular highlight on the purple circle
hl = disc(90 * S, 98 * S, 26 * S, (210, 185, 255, 95)).filter(ImageFilter.GaussianBlur(11 * S))
content = Image.alpha_composite(content, hl)

# clip everything to the rounded tile
out = Image.alpha_composite(tile, content)
out.putalpha(ImageChops.multiply(out.split()[3], mask))

out.resize((256, 256), Image.LANCZOS).save("icon.png")
print("icon.png written")
