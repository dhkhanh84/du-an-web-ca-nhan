import sys; from PIL import Image, ImageDraw, ImageFont
F=sys.argv[1]; W,H=1280,720
c=Image.new('RGBA',(W,H),(253,253,252,255)); g=Image.new('RGBA',(W,H),(0,0,0,0)); gd=ImageDraw.Draw(g)
for x in range(0,W,64): gd.line([(x,0),(x,H)],fill=(76,90,105,12))
for y in range(0,H,64): gd.line([(0,y),(W,y)],fill=(76,90,105,12))
c.alpha_composite(g)
ring=Image.open('assets/cut/s18_ring6.png').crop((230,270,1360,660)); ring=ring.resize((int(ring.width*.63),int(ring.height*.63)))
c.alpha_composite(ring,(W-ring.width-15,H-ring.height-25))
hero=Image.open('assets/cut/s17_hero.png'); hero=hero.crop(hero.getchannel('A').point(lambda v:255 if v>60 else 0).getbbox())
hero=hero.resize((int(hero.width*360/hero.height),360)); c.alpha_composite(hero,(860,15))
d=ImageDraw.Draw(c)
def txt(xy,t,fill,size):
    fo=ImageFont.truetype(F,size)
    try: fo.set_variation_by_name('Bold')
    except Exception: pass
    d.text(xy,t,font=fo,fill=fill,stroke_width=2,stroke_fill=fill)
txt((50,30),"NOT ONE",(28,28,28),140); txt((50,170),"HERO.",(236,67,56),170)
d.line([(820,120),(1180,330)],fill=(236,67,56),width=12); d.line([(1180,120),(820,330)],fill=(236,67,56),width=12)
txt((50,400),"6 PARTIES.",(28,28,28),84); txt((50,500),"1 PROMISE.",(232,163,23),84)
c.convert('RGB').save('publishing/thumbnail.png'); c.convert('RGB').resize((320,180)).save('/tmp/claude-0/thumb_small.png')
