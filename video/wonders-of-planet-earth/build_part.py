# Build a B2 project for a range of chapters from per-scene narration + user images.
import json,re,sys,wave,os,subprocess
import numpy as np
from PIL import Image, ImageFont
CH=[int(c) for c in sys.argv[1].split(',')]; NAME=sys.argv[2]
SR=24000; LEAD=0.4; GAP=0.7; CHGAP=1.8
data=json.load(open('scenes.json')); chap=dict(data['chapters'])
scenes=[s for s in data['scenes'] if int(s['code'].split('.')[0]) in CH]
CAPF=ImageFont.truetype('/root/.claude/plugins/synced/6885484c-7413-48de-8948-b53451880e01_1ccae8e5-87c7-4a7f-b902-53f9d823848c/stickman-video-director/skills/directing-stickman-videos/assets/fonts/NotoSans.ttf',40)
def rd(p): w=wave.open(p); return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768
def pauses(x):
    hop=int(.02*SR); r=np.array([np.sqrt((x[i:i+hop]**2).mean()) for i in range(0,len(x)-hop,hop)])
    q=r<10**(-38/20); out=[]; i=0
    while i<len(q):
        if q[i]:
            j=i
            while j<len(q) and q[j]: j+=1
            if (j-i)*.02>=.18: out.append(((i+j)/2*.02,(j-i)*.02))
            i=j
        else: i+=1
    return out
LIM=820  # PIL regular-weight px; ~1.3x narrower than the renderer's 500-weight caption font (limit 1120)
SPLITW={'and','that','from','of','to','in','with','when','while','but','which','where','as','on','into','across','because','so','until','before','after','for','at','by'}
def fit(p): return CAPF.getlength(p)<=LIM
def split_sem(p):
    if fit(p): return [p]
    w=p.split(); mid=len(w)/2
    cands=[i for i in range(2,len(w)-1) if w[i].lower().strip(',') in SPLITW or w[i-1].endswith(',')]
    i=min(cands,key=lambda i:abs(i-mid)) if cands else len(w)//2
    return split_sem(' '.join(w[:i]))+split_sem(' '.join(w[i:]))
def phrases(text):
    parts=re.split(r'(?<=[.!?:;])\s+',text.strip()); out=[]
    for p in parts:
        bits=re.split(r'(?<=,)\s+',p); cur=''
        for b in bits:
            t=(cur+' '+b).strip()
            if cur and not fit(t): out+=split_sem(cur); cur=b
            else: cur=t
        if cur: out+=split_sem(cur)
    merged=[]
    for p in out:
        if merged and (len(p)<14 or len(merged[-1])<14) and fit(merged[-1]+' '+p) and not re.search(r'[.!?]$',merged[-1]): merged[-1]=merged[-1]+' '+p
        else: merged.append(p)
    return merged

from PIL import ImageDraw
HANDF='/root/.claude/plugins/synced/6885484c-7413-48de-8948-b53451880e01_1ccae8e5-87c7-4a7f-b902-53f9d823848c/stickman-video-director/skills/directing-stickman-videos/assets/fonts/Caveat.ttf'
def label(text,color,size):
    import hashlib
    key=hashlib.md5(f"{text}|{color}|{size}".encode()).hexdigest()[:10]; out=f'assets/labels/{key}.png'
    if os.path.exists(out): return out
    f=ImageFont.truetype(HANDF,size*2)
    try: f.set_variation_by_axes([700])
    except Exception: pass
    w=int(f.getlength(text))+size*2; h=int(size*2*1.45)
    im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((3,3,w-4,h-4),radius=size//2,fill=(249,246,235,240),outline=(90,70,50,200),width=3)
    d.text((size,h*0.08),text,font=f,fill=color)
    im.save(out); return out
NUM=re.compile(r"(\d[\d,.]*\s?(?:billion|million|thousand)?\s?(?:years|metres|kilometres|degrees Celsius|percent|tonnes|cubic kilometres|cubic metres|kilometres per hour|km)?|AD \d+|\b(?:1[0-9]{3}|20[0-9]{2})\b)")
audio=[]; t=LEAD; caps=[]; shots=[]; sfx=[]
chap_first={}
for idx,s in enumerate(scenes):
    c=int(s['code'].split('.')[0])
    if c not in chap_first:
        chap_first[c]=t
        if idx>0: t+=CHGAP-GAP
    x=rd('audio/scenes/'+s['code'].replace('.','-')+'.wav'); dur=len(x)/SR
    s['t0']=t; s['dur']=dur
    # caption timing: char-proportional boundaries snapped to nearest real pause
    ph=phrases(s['narration']); P=pauses(x); tot=sum(len(p) for p in ph); acc=0; b=[0.0]
    for p in ph[:-1]:
        acc+=len(p); est=dur*acc/tot
        prev_est=dur*(acc-len(p))/tot; seg=est-prev_est
        cand=[m for m,l in P if abs(m-est)<min(0.8,0.4*seg+0.2) and m>b[-1]+max(0.5,0.6*seg)]
        nb=min(cand,key=lambda m:abs(m-est)) if cand else est
        nb=max(nb,b[-1]+max(0.55,0.7*seg))
        b.append(nb)
    # keep room for the remaining phrases: rescale if boundaries overran the clip
    rem=[len(p) for p in ph]
    for k in range(len(b)-1,0,-1):
        need=dur*sum(rem[k:])/tot*0.6
        if b[k]>dur-need: b[k]=max(b[k-1]+0.3,dur-need)
    b.append(dur)
    for p,(a,e) in zip(ph,zip(b,b[1:])): caps.append({"start":round(t+a+0.03,3),"end":round(t+e-0.02,3),"text":p,"scene":s['code']})
    s['bounds']=b; s['phr']=ph
    audio.append((t,x)); t+=dur+GAP
total=t+1.5
N=int(total*SR); voice=np.zeros(N)
for t0,x in audio: s0=int(t0*SR); voice[s0:s0+len(x)]+=x
os.makedirs('audio/parts',exist_ok=True)
def wr(p,y):
    y=np.clip(y,-1,1); w=wave.open(p,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y*32767).astype(np.int16).tobytes()); w.close()
wr(f'audio/parts/{NAME}_voice.wav',voice)
# shots
GOLD="#B8862B"; RUST="#B5543B"; SLATE="#3E5A73"
def T(text,x,y,size,color=None,**k):
    k.setdefault('w',1240-x); d=dict(type='text',text=text,x=x,y=y,size=size,bold=True,**k)
    if color: d['color']=color
    return d
for i,s in enumerate(scenes):
    c=int(s['code'].split('.')[0]); st=s['t0']-(0.35 if i>0 else s['t0'])
    if i>0 and chap_first[c]==s['t0']: st=s['t0']-(CHGAP-0.2)
    en=(scenes[i+1]['t0']-0.35) if i+1<len(scenes) and chap_first.get(int(scenes[i+1]['code'].split('.')[0]))!=scenes[i+1]['t0'] else (scenes[i+1]['t0']-(CHGAP-0.2) if i+1<len(scenes) else total)
    s['shot']=(round(st,3),round(en,3)); sp=en-st
    im=Image.open('images/'+s['file']); iw,ih=im.size
    if ih/iw>0.6: w0=int(720*0.97*iw/ih); x0=(1280-w0)//2; y0=10
    else: w0=1280; x0=0; y0=(720-int(1280*ih/iw))//2
    # camera tour: one keyframe per phrase, alternating gentle zoom targets
    keys=[{"t":0,"w":w0,"x":x0,"y":y0,"alpha":0 if i==0 else 1}]
    if i==0: keys.append({"t":.6,"alpha":1})
    targets=[(0.5,0.5),(0.35,0.4),(0.65,0.45),(0.4,0.6),(0.6,0.35),(0.5,0.55)]
    off=s['t0']-st
    for j,bb in enumerate(s['bounds'][1:]):
        z=1.0+0.06*((j%3)+1); cx,cy=targets[(j+i)%len(targets)]
        W=w0*z; H=W*ih/iw
        kx=x0-(W-w0)*cx; ky=y0-(H-w0*ih/iw)*cy
        tt=min(off+bb,sp-0.05)
        if tt>keys[-1]['t']+0.3: keys.append({"t":round(tt,2),"w":round(W),"x":round(kx),"y":round(ky)})
    L=[dict(type='image',path='images/'+s['file'],x=x0,y=y0,w=w0,keys=keys)]
    # scene heading + spoken key numbers as handwritten labels
    title=next(x for x in open('image-prompts.md').read().split('\n') if x.startswith('### '+s['code']+' ')).split(' — ',1)[1].split('  →')[0]
    lp=label(title.upper(),SLATE,34); lw=Image.open(lp).size[0]/2
    L.append(dict(type='image',path=lp,x=30,y=22,w=round(lw),keys=[{"t":0,"alpha":0},{"t":.4,"alpha":1},{"t":4.2,"alpha":1},{"t":4.8,"alpha":0}]))
    used=0
    for j,p in enumerate(s['phr']):
        m=NUM.search(p)
        if m and used<3:
            lab=m.group(0).strip().rstrip(',.').upper()
            if len(lab)<3: continue
            tt=off+s['bounds'][j]+0.2
            lp=label(lab,RUST,40); lw=round(Image.open(lp).size[0]/2); xx=1250-lw
            L.append(dict(type='image',path=lp,x=xx,y=22+used*62,w=lw,**{"from":round(tt,2)},keys=[{"t":round(tt,2),"alpha":0,"x":xx+20},{"t":round(tt+.3,2),"alpha":1,"x":xx}]))
            used+=1
    if chap_first[c]==s['t0']:
        L.append(dict(type='rect',x=0,y=0,w=1280,h=720,fill='#f4f0e5',to=round(min(sp,1.9+ (0 if i==0 else 0)),2)) if False else None)
    L=[l for l in L if l]
    shots.append({"start":s['shot'][0],"end":s['shot'][1],"layers":L})
# chapter cards overlay: separate short shots replacing the first 1.6s before each chapter's first scene
cards=[]
for c,t0 in chap_first.items():
    cs=max(0,t0-1.6) if t0>LEAD else 0; ce=t0+0.9
    cards.append((c,cs,ce))
# split shots at card windows: simplest is to prepend card layers into the first shot of each chapter
for c,cs,ce in cards:
    for sh in shots:
        if sh['start']<=cs+0.01<sh['end'] or abs(sh['start']-cs)<0.4:
            rel0=cs-sh['start']; rel1=ce-sh['start']
            sh['layers']+= [dict(type='image',path='assets/paper.png',x=0,y=0,w=1280,**{"from":round(max(rel0,0),2),"to":round(rel1,2)},keys=[{"t":round(max(rel0,0),2),"alpha":1},{"t":round(rel1-0.5,2),"alpha":1},{"t":round(rel1,2),"alpha":0}]),
               dict(type='image',path=label(f"CHAPTER {c}",RUST,44),x=round(640-Image.open(label(f"CHAPTER {c}",RUST,44)).size[0]/4),y=230,w=round(Image.open(label(f"CHAPTER {c}",RUST,44)).size[0]/2),**{"from":round(max(rel0,0),2),"to":round(rel1,2)}),
               T(chap[str(c)].upper(),max(20,round(640-ImageFont.truetype(HANDF,84).getlength(chap[str(c)].upper())*0.53)),330,84,SLATE,w=1240,**{"from":round(max(rel0,0)+.2,2),"to":round(rel1,2)},keys=[{"t":round(max(rel0,0)+.2,2),"alpha":0,"y":345},{"t":round(max(rel0,0)+.6,2),"alpha":1,"y":330}])]
            break
# make shots contiguous
shots.sort(key=lambda s:s['start']); shots[0]['start']=0
for a,bb in zip(shots,shots[1:]): a['end']=bb['start']
shots[-1]['end']=round(total,3)
for sh in shots:
    sp=sh['end']-sh['start']
    for l in sh['layers']:
        for k in l.get('keys',[]): k['t']=round(max(0,min(k['t'],sp-0.03)),3)
        if 'from' in l: l['from']=round(max(0,min(l['from'],sp-0.05)),3)
        if 'to' in l: l['to']=round(max(l.get('from',0)+0.05,min(l['to'],sp-0.005)),3)
        if 'keys' in l:
            ks=[];last=-1
            for k in sorted(l['keys'],key=lambda k:k['t']):
                if k['t']>last: ks.append(k); last=k['t']
            l['keys']=ks
for cpt in caps: cpt.pop('scene',None)
caps.sort(key=lambda c:c['start'])
for c1,c2 in zip(caps,caps[1:]):
    if c1['end']>c2['start']-0.01: c1['end']=round(c2['start']-0.02,3)
for c1 in caps:
    if c1['end']<c1['start']+0.25: c1['end']=round(c1['start']+0.25,3)
for c1,c2 in zip(caps,caps[1:]):
    if c2['start']<c1['end']+0.01: c2['start']=round(c1['end']+0.02,3)
caps=[c1 for c1 in caps if c1['end']>c1['start']]
json.dump({"scene_times":[{"code":s['code'],"t0":round(s['t0'],3),"dur":round(s['dur'],3)} for s in scenes],"chapters":{str(c):round(t,3) for c,t in chap_first.items()},"total":round(total,3)},open(f'audio/parts/{NAME}_timing.json','w'),indent=1)
p={"version":1,"style":"B2","width":1280,"height":720,"fps":30,"voice":{"path":f"audio/parts/{NAME}_mix.wav","lead":0,"tail":0,"contains_sfx":True},"captions":caps,"shots":shots,"sfx":[]}
json.dump(p,open(f'project_{NAME}.json','w'),indent=1)
print(len(scenes),'scenes',len(caps),'captions',len(shots),'shots',round(total/60,2),'min')
