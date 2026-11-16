import json
L=0.15
segs=[(0.26,1.08,["2009."]),(1.48,3.05,["AI hasn't taken off yet."]),(3.35,5.24,["Jensen Huang's message","at Stanford:"]),
(5.64,8.52,["don't just listen to customers.","Listen to Moore's Law."]),(9.03,13.03,["Moore's Law:","the number of transistors","on a chip","doubles about every two years."]),
(13.35,15.68,["Most companies used it","to forecast technology."]),(16.02,17.95,["Jensen used it","to forecast the future."]),
(18.43,19.62,["The 1990s."]),(19.90,21.67,["Gamers just wanted","prettier graphics."]),(21.94,25.25,["NVIDIA built GPUs","far more powerful","than anyone asked for."]),
(25.54,27.11,["Customers said it cost too much."]),(27.38,28.41,["Jensen saw it differently:"]),(28.67,32.13,["Give the world","enough computing power,","and new applications will appear."]),
(32.53,33.88,["He bet on the GPU."]),(34.17,34.76,["Then CUDA."]),(35.05,35.81,["Then AI."]),
(36.11,40.11,["Fifteen years later,","the world is racing to build AI","on NVIDIA chips."]),(40.50,41.69,["Jensen's big lesson:"]),
(42.09,43.37,["Customers talk","about the present."]),(43.64,45.11,["Technology talks","about the future."]),
(45.39,47.44,["Great companies","don't just predict demand."]),(47.66,49.64,["They predict where technology","takes us next."])]
caps=[]
for a,b,ph in segs:
    tot=sum(len(p) for p in ph); t=a
    for p in ph:
        e=t+(b-a)*len(p)/tot; caps.append({"start":round(t+L,3),"end":round(e+L,3),"text":p}); t=e
for c,n in zip(caps,caps[1:]): c['end']=round(min(n['start']-0.02,c['end']+0.35),3)
RED="#EC4338"; GOLD="#E8A317"; GREEN="#5A9E1A"; NAVY="#27408B"
shots=[]
def img(f,x=50,y=480,w=1180,**k): return dict(type="image",path=f"assets/cut/{f}.png",x=x,y=y,w=w,**k)
def T(t,y,size=110,color=None,x=70,**k):
    k.setdefault("w",1250-x)
    d=dict(type="text",text=t,x=x,y=y,size=size,bold=True,**k)
    if color: d['color']=color
    return d
fr=lambda t:{"from":t}
def shot(s,e,layers):
    sp=e-s
    for l in layers:
        for k in l.get('keys',[]): k['t']=round(min(k['t'],sp-0.03),3)
    shots.append({"start":s,"end":e,"layers":layers})
shot(0,3.5,[T("2009",300,250,keys=[{"t":0,"alpha":0,"x":140},{"t":.25,"alpha":1,"x":70}]),T("AI? NOT YET.",300,110,GOLD,x=620,w=640,**fr(1.55)),
  img("v04_stage",keys=[{"t":0,"alpha":0},{"t":.35,"alpha":1},{"t":1.55,"y":480},{"t":1.6,"y":487},{"t":1.75,"y":480},{"t":3.5,"w":1240,"x":20}])])
shot(3.5,9.18,[T("THE STANFORD MESSAGE:",230,96),T("NOT JUST CUSTOMERS.",380,110,RED,**fr(2.3)),
  T("LISTEN TO MOORE’S LAW.",1580,100,GREEN,**fr(3.95)),
  img("n01_listen",keys=[{"t":0,"alpha":0,"x":110},{"t":.35,"alpha":1,"x":50},{"t":2.3,"angle":0},{"t":2.45,"angle":-.015},{"t":2.6,"angle":0},{"t":3.95,"w":1180,"x":50},{"t":5.6,"w":1240,"x":20}])])
chips=[1,2,4,8,16,32,64]
cl=[]
for i,n in enumerate(chips):
    t0=.5+i*.55; last=i==len(chips)-1
    d=img(f"chip{n}",x=190,y=560,w=900,**fr(t0)); 
    if not last: d['to']=round(t0+.55,2)
    d['keys']=[{"t":t0,"w":930,"x":175},{"t":t0+.12,"w":900,"x":190}]
    cl.append(d)
shot(9.18,13.48,[T("MOORE'S LAW",230,140),T("TRANSISTORS x2",400,120,GREEN,**fr(2.0)),T("EVERY ~2 YEARS",1580,110,**fr(2.6))]+cl)
shot(13.48,18.58,[T("OTHERS: FORECAST TECH.",230,96),T("JENSEN: THE FUTURE.",380,120,GREEN,**fr(2.7)),
  img("v05_lens",**fr(2.6),keys=[{"t":2.6,"alpha":0,"y":520},{"t":2.95,"alpha":1,"y":480},{"t":5.0,"w":1230,"x":25}]),
  img("v12_why",to=2.6,keys=[{"t":0,"alpha":0},{"t":.3,"alpha":1},{"t":1.3,"angle":0},{"t":1.45,"angle":-.015},{"t":1.6,"angle":0},{"t":2.55,"alpha":.2}])])
shot(18.58,21.85,[T("THE 1990s",230,140,NAVY),T("GAMERS WANTED",390,110,**fr(1.45)),T("PRETTIER GRAPHICS!",1580,110,GOLD,**fr(1.9)),
  img("n02_gamers",keys=[{"t":0,"alpha":0},{"t":.3,"alpha":1},{"t":1.45,"y":480},{"t":1.5,"y":472},{"t":1.65,"y":480},{"t":3.2,"w":1230,"x":25}])])
shot(21.85,25.65,[T("FAR MORE POWER",230,130,GREEN),T("THAN ANYONE ASKED FOR",400,96,**fr(2.0)),
  img("n03_overpowered",keys=[{"t":0,"alpha":0,"x":-80},{"t":.4,"alpha":1,"x":50},{"t":2.0,"y":480},{"t":2.06,"y":490},{"t":2.2,"y":480},{"t":3.7,"w":1230,"x":25}])])
shot(25.65,28.6,[T("CUSTOMERS:",230,110),T("\"TOO EXPENSIVE.\"",380,130,RED,**fr(.3)),T("JENSEN SAW IT DIFFERENTLY.",1570,84,GREEN,**fr(1.9)),
  img("v02_investors",keys=[{"t":0,"alpha":0},{"t":.3,"alpha":1},{"t":.6,"angle":0},{"t":.75,"angle":.02},{"t":.9,"angle":-.02},{"t":1.05,"angle":0},{"t":2.9,"w":1220,"x":30}])])
shot(28.6,32.6,[T("MORE COMPUTING POWER",230,100),T("= NEW APPLICATIONS",380,110,GREEN,**fr(2.4)),
  img("n05_apps",x=-200,y=330,w=1680,keys=[{"t":0,"alpha":0,"w":1500,"x":-110,"y":420},{"t":.5,"alpha":1,"w":1680,"x":-200,"y":330},{"t":2.4,"w":1680,"x":-200},{"t":2.5,"w":1710,"x":-215},{"t":2.65,"w":1680,"x":-200},{"t":4.0,"w":1760,"x":-240}])])
bx=lambda y,t:img("box",x=430,y=y,w=420,**fr(t),keys=[{"t":t,"alpha":0,"w":470,"x":405},{"t":t+.15,"alpha":1,"w":420,"x":430}])
lab=lambda s,y,t,c=None:T(s,y,120,c,x=0,w=1280,**fr(t+.05))
dn=lambda y,t:{"type":"line","points":[[640,y],[640,y+70]],"color":"#444444","lineWidth":7,"from":t,"keys":[{"t":t,"progress":0},{"t":t+.2,"progress":1}]}
shot(32.6,36.25,[T("THE BETS",230,140,GOLD),bx(600,.8),T("GPU",680,120,x=545,**fr(.85)),dn(860,1.5),bx(950,1.7),T("CUDA",1030,120,x=520,**fr(1.75)),
  dn(1210,2.4),bx(1300,2.6),T("AI",1380,130,GREEN,x=595,**fr(2.65))])
shot(36.25,40.6,[T("15 YEARS LATER",230,120),T("THE AI RACE",380,140,GREEN,**fr(1.3)),T("RUNS ON NVIDIA CHIPS.",1580,96,**fr(3.0)),
  img("n04_datacenter",keys=[{"t":0,"alpha":0},{"t":.4,"alpha":1,"w":1180,"x":50},{"t":1.3,"y":480},{"t":1.35,"y":488},{"t":1.5,"y":480},{"t":4.3,"w":1260,"x":10}])])
shot(40.6,45.48,[T("THE LESSON:",230,140,GOLD),T("CUSTOMERS = THE PRESENT",1480,92,**fr(1.6)),T("TECHNOLOGY = THE FUTURE",1600,92,GREEN,**fr(3.15)),
  img("n01_listen",x=140,y=420,w=1000,keys=[{"t":0,"alpha":0},{"t":.3,"alpha":1},{"t":1.6,"angle":0},{"t":1.75,"angle":.015},{"t":1.9,"angle":0},{"t":3.15,"y":420},{"t":3.2,"y":428},{"t":3.35,"y":420},{"t":4.8,"w":1040,"x":120}])])
shot(45.48,49.98,[T("NOT JUST DEMAND.",230,120),T("WHERE TECH GOES NEXT.",380,100,GREEN,**fr(2.3)),
  img("v10_bigchip",keys=[{"t":0,"alpha":0,"x":-100},{"t":.4,"alpha":1,"x":50},{"t":1.4,"x":40},{"t":2.3,"x":50},{"t":2.35,"y":490},{"t":2.5,"y":480},{"t":3.4,"x":40},{"t":4.4,"x":50}])])
shot(49.98,52.4,[T("WHAT STAGE OF THE",300,110),T("\"MOORE MOMENT\"",450,140,GREEN,**fr(.3)),T("IS AI IN TODAY?",620,120,**fr(.7)),
  img("p_bubble",x=420,y=900,w=440,**fr(1.4),keys=[{"t":1.4,"w":280,"x":500,"alpha":0},{"t":1.65,"w":460,"x":410,"alpha":1},{"t":1.8,"w":440,"x":420}])])
p={"version":1,"style":"B1","width":1080,"height":1560,"fps":30,"captionSize":56,
   "voice":{"path":"audio/master_mix_norm.wav","lead":0,"tail":0,"contains_sfx":True},"captions":caps,"shots":shots,"sfx":[]}
json.dump(p,open('project.json','w'),indent=1); print(len(caps),'captions')
