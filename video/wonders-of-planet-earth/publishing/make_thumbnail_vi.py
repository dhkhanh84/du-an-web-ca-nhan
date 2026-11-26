# Vietnamese thumbnail: same art, Vietnamese headline (Patrick Hand has Vietnamese glyphs). python3 publishing/make_thumbnail_vi.py
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
CAVEAT = 'assets/fonts/PatrickHand_400Regular.ttf'
im = Image.open('publishing/thumb_art-en.webp').convert('RGB')
a = np.array(im).astype(float)
# remove the image model's sparkle mark (bottom right, on plain background)
x0, y0, x1, y1 = 1226, 618, 1288, 678
ring = np.concatenate([a[y0 - 6:y0, x0:x1].reshape(-1, 3), a[y1:y1 + 6, x0:x1].reshape(-1, 3)])
rng = np.random.default_rng(0)
a[y0:y1, x0:x1] = np.median(ring, 0) + rng.normal(0, 1, (y1 - y0, x1 - x0, 3)) * ring.std(0) * 0.6
im = Image.fromarray(a.clip(0, 255).astype(np.uint8))
# 16:9 crop (1376x768 -> 1365x768) and resize to 1280x720
im = im.crop((0, 0, 1365, 768)).resize((1280, 720), Image.LANCZOS)
def font(size):
    f = ImageFont.truetype(CAVEAT, size)
    try: f.set_variation_by_axes([700])
    except Exception: pass
    return f
lines = [("TRÁI ĐẤT", (246, 239, 222), 190), ("KHÔNG YÊN BÌNH", (238, 122, 74), 190)]
MAXW = 540
layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
shadow = Image.new('RGBA', im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(shadow)
y = 110
for text, col, size in lines:
    while font(size).getlength(text) > MAXW: size -= 2
    f = font(size); x = 44
    ds.text((x + 6, y + 8), text, font=f, fill=(20, 28, 38, 200))
    d.text((x, y), text, font=f, fill=col + (255,), stroke_width=8, stroke_fill=(45, 36, 30, 255))
    y += int(size * 0.95)
shadow = shadow.filter(ImageFilter.GaussianBlur(5))
out = Image.alpha_composite(Image.alpha_composite(im.convert('RGBA'), shadow), layer).convert('RGB')
out.save('publishing/thumbnail-vi.png')
out.resize((320, 180), Image.LANCZOS).save('publishing/thumbnail-vi_320.png')
print(out.size)
