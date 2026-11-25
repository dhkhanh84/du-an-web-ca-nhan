# Writes the chapter list onto the empty right page of images_fixed/00-toc.png.
# make_toc(n) -> PNG with the title and the first n chapter lines (for line-by-line reveal).
import json, os
from PIL import Image, ImageDraw, ImageFont
HANDF = '/root/.claude/plugins/synced/6885484c-7413-48de-8948-b53451880e01_1ccae8e5-87c7-4a7f-b902-53f9d823848c/stickman-video-director/skills/directing-stickman-videos/assets/fonts/Caveat.ttf'
CH = json.load(open('scenes.json'))['chapters']
INK = (62, 44, 30); RED = (176, 72, 52)
def font(size, wght=700):
    f = ImageFont.truetype(HANDF, size)
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f
def make_toc(n=17, out=None):
    im = Image.open('images_fixed/00-toc.png').convert('RGBA')
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    X0, X1 = 690, 1170
    tf = font(52); title = 'Our Journey'
    tw = d.textlength(title, font=tf); d.text(((X0 + X1 - tw) / 2, 52), title, font=tf, fill=INK)
    d.line([((X0 + X1) / 2 - 90, 122), ((X0 + X1) / 2 + 90, 122)], fill=RED, width=3)
    colx = [X0 + 6, X0 + 250]; y0 = 152; lh = 46; NW = 40; RIGHT = 1172
    size = 30
    while size > 20:
        lf = font(size, 500)
        w2 = max(d.textlength(nm, font=lf) for _, nm in CH[9:]); w1 = max(d.textlength(nm, font=lf) for _, nm in CH[:9])
        if colx[1] + NW + w2 <= RIGHT and colx[0] + NW + w1 <= colx[1] - 12: break
        size -= 1
    nf = font(size, 700)
    for i, (num, name) in enumerate(CH[:n]):
        c = 0 if i < 9 else 1; r = i if i < 9 else i - 9
        x, y = colx[c], y0 + r * lh
        d.text((x + NW - 8 - d.textlength(num + '.', font=nf), y), num + '.', font=nf, fill=RED)
        d.text((x + NW, y), name, font=lf, fill=INK)
    im = Image.alpha_composite(im, ov).convert('RGB')
    if out: im.save(out)
    return im
if __name__ == '__main__':
    make_toc(17, '/tmp/claude-0/-home-user-du-an-web-ca-nhan/4caafea6-78f2-5e41-bf9f-ec456e90c622/scratchpad/toc_full.png')
