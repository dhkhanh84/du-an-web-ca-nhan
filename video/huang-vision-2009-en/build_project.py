import json
L=0.15
segs=[(0.23,1.47,["In 1993,"]),(1.66,4.03,["investors told him","video games weren't a market."]),(4.51,6.74,["His mother asked why","he didn't just get a job."]),
(7.43,9.34,["Sixteen years later, at Stanford,"]),(9.55,11.73,["Jensen Huang explained","how he got past that."]),(12.20,12.86,["Lesson one:"]),
(13.18,14.70,["don't wait for a grand vision."]),(15.15,16.44,["Everyone has a perspective."]),(16.74,17.99,["That's all a vision really is."]),
(18.60,23.29,["His perspective in 1993:","take 3D graphics","off expensive workstations,","make them cheap,"]),
(23.55,27.01,["and let video games pull","the whole PC market forward."]),(27.59,28.33,["Lesson two:"]),(28.70,30.43,["sometimes you go","against your customers."]),
(30.86,34.30,["Dell, HP, IBM and Gateway","all said it cost too much."]),(34.59,38.16,["He still bet the company's","last few million on a chip","that was far too big,"]),
(38.50,40.39,["sure the technology","would get cheap fast."]),(41.02,43.47,["About two hundred companies","went after 3D graphics."]),
(43.77,46.19,["Money, talent and technology","were roughly equal."]),(46.51,50.31,["What decided who survived,","he said, was understanding","why your business works."]),
(50.91,51.54,["Lesson three:"]),(51.87,53.33,["get comfortable with ambiguity."]),(53.67,55.21,["Leaders don't have to be outgoing."]),
(55.46,57.75,["They do have to act","before the outcome is clear."]),(58.19,58.95,["Lesson four:"]),(59.17,60.60,["tear it down and rebuild."]),
(61.01,62.60,["Every success has to be rebuilt,"]),(62.79,63.80,["roughly once a decade."]),(64.21,66.78,["If you don't replace","your own product,","your competitors will."]),
(67.16,70.80,["Finally:","skill, intellect and training matter,","but they're not enough."]),(71.20,73.74,["You need passion","for the painful parts","of building a company."]),
(74.07,75.41,["Which lesson do you need most?"]),(75.75,76.69,["Tell me in the comments."])]
caps=[]
for a,b,ph in segs:
    tot=sum(len(p) for p in ph); t=a
    for p in ph:
        e=t+(b-a)*len(p)/tot; caps.append({"start":round(t+L,3),"end":round(e+L,3),"text":p}); t=e
# hold each cue into the following pause (max 0.35 s) for reading time
for c,n in zip(caps,caps[1:]):
    c['end']=round(min(n['start']-0.02,c['end']+0.35),3)
caps[-1]['end']=round(caps[-1]['end']+0.3,3)
RED="#EC4338"; GOLD="#E8A317"; GREEN="#5A9E1A"; NAVY="#27408B"
shots=[]
def img(f,x=50,y=480,w=1180,**k): return dict(type="image",path=f"assets/cut/{f}.png",x=x,y=y,w=w,**k)
def T(t,y,size=110,color=None,x=70,**k):
    d=dict(type="text",text=t,x=x,y=y,size=size,bold=True,**k)
    if color: d['color']=color
    return d
fr=lambda t:{"from":t}
def shot(s,e,layers):
    sp=e-s
    for l in layers:
        for k in l.get('keys',[]): k['t']=round(min(k['t'],sp-0.03),3)
    shots.append({"start":s,"end":e,"layers":layers})
shot(0,1.8,[T("1993",300,250,keys=[{"t":0,"alpha":0,"x":140},{"t":.25,"alpha":1,"x":70}]),
  img("v01_pc1993",keys=[{"t":0,"alpha":0},{"t":.35,"alpha":1},{"t":.9,"y":480},{"t":.95,"y":486},{"t":1.1,"y":480},{"t":1.8,"x":40,"w":1210}])])
shot(1.8,4.65,[T("VIDEO GAMES?",230,120),T("\"NO MARKET.\"",380,140,RED,**fr(1.2)),
  img("v02_investors",keys=[{"t":0,"x":110,"alpha":0},{"t":.3,"x":50,"alpha":1},{"t":1.2,"angle":0},{"t":1.35,"angle":.02},{"t":1.5,"angle":-.02},{"t":1.65,"angle":0},{"t":2.8,"w":1230,"x":25}])])
shot(4.65,7.55,[T("MOM:",230,120),T("WHY NOT GET A JOB?",380,110,RED,**fr(1.0)),
  img("v03_mom",keys=[{"t":0,"alpha":0,"y":520},{"t":.3,"alpha":1,"y":480},{"t":1.0,"angle":0},{"t":1.25,"angle":.025},{"t":1.5,"angle":0},{"t":2.9,"w":1230,"x":25}])])
shot(7.55,12.32,[T("16 YEARS LATER...",230,110),T("STANFORD, 2009",380,130,NAVY,**fr(1.0)),
  img("v04_stage",keys=[{"t":0,"alpha":0},{"t":.4,"alpha":1},{"t":2.0,"w":1180,"x":50},{"t":2.05,"y":486},{"t":2.2,"y":480},{"t":4.7,"w":1260,"x":10}])])
shot(12.32,18.72,[T("LESSON #1",210,110,GOLD),T("VISION",350,120,**fr(1.0)),
  {"type":"line","points":[[60,395],[330,388]],"color":RED,"lineWidth":12,"from":1.8,"keys":[{"t":1.8,"progress":0},{"t":2.2,"progress":1}]},
  T("PERSPECTIVE",350,120,GREEN,x=460,w=800,**fr(3.0)),
  img("v05_lens",**fr(3.0),keys=[{"t":3.0,"alpha":0,"y":520},{"t":3.35,"alpha":1,"y":480},{"t":4.5,"w":1180,"x":50},{"t":6.3,"w":1240,"x":20}])])
shot(18.72,23.62,[T("3D GRAPHICS",230,130),T("EXPENSIVE",380,120,RED,**fr(2.0)),T("CHEAP",380,120,GREEN,x=760,w=500,**fr(3.85)),
  {"type":"arrow","x":560,"y":440,"w":180,"from":3.7,"keys":[{"t":3.7,"progress":0},{"t":3.9,"progress":1}]},
  img("v06_workstation",keys=[{"t":0,"alpha":0},{"t":.35,"alpha":1},{"t":2.0,"x":50},{"t":2.2,"x":40},{"t":2.4,"x":50},{"t":4.9,"y":470}])])
shot(23.62,27.72,[T("GAMES",230,150,GOLD),T("= THE ENGINE",400,120,**fr(1.2)),
  img("v07_gamepad",keys=[{"t":0,"alpha":0,"y":520},{"t":.3,"alpha":1,"y":480},{"t":1.4,"y":480},{"t":1.45,"y":470},{"t":1.6,"y":480},{"t":2.6,"y":480},{"t":2.65,"y":472},{"t":2.8,"y":480},{"t":4.0,"w":1220,"x":30}])])
shot(27.72,34.72,[T("LESSON #2",210,110,GOLD),T("GO AGAINST",340,110,**fr(1.0)),T("YOUR CUSTOMERS",450,110,**fr(1.4)),
  img("v08_boxes",x=50,y=560,w=1180,**fr(3.0),keys=[{"t":3.0,"alpha":0},{"t":3.2,"alpha":1}]),
  T("DELL",780,80,x=140,**fr(3.3)),T("HP",780,80,x=470,**fr(3.7)),T("IBM",780,80,x=745,**fr(4.1)),T("GATEWAY",780,64,x=960,w=300,**fr(4.6)),
  img("stamp",x=300,y=1080,w=700,**fr(5.9),keys=[{"t":5.9,"w":900,"x":200,"alpha":0},{"t":6.05,"w":700,"x":300,"alpha":1}]),
  T("TOO EXPENSIVE!",1160,110,RED,x=360,**fr(5.95))])
shot(34.72,40.85,[T("THE LAST",230,120),T("FEW MILLION",380,140,RED,**fr(1.0)),T("BET: CHIPS GET CHEAP",1580,96,GREEN,**fr(3.95)),
  img("v10_bigchip",keys=[{"t":0,"x":-120,"alpha":0},{"t":.4,"x":50,"alpha":1},{"t":1.5,"x":40},{"t":2.3,"x":50},{"t":3.1,"x":40},{"t":4.0,"x":50},{"t":5.0,"x":40},{"t":6.1,"x":50}])])
shot(40.85,48.0,[T("~200 COMPETITORS",230,120),T("ALL ROUGHLY EQUAL",380,100,**fr(3.0)),
  img("dots200",x=140,y=560,w=1000,to=4.0,keys=[{"t":0,"alpha":0},{"t":.4,"alpha":1},{"t":2.0,"w":1000,"x":140},{"t":2.1,"w":1010,"x":135},{"t":2.25,"w":1000,"x":140}]),
  img("dots60",x=140,y=560,w=1000,**fr(4.0),to=4.7),img("dots12",x=140,y=560,w=1000,**fr(4.7),to=5.4),
  img("dots1",x=140,y=560,w=1000,**fr(5.4)),T("1 LEFT.",1600,160,GREEN,x=420,**fr(5.6))])
shot(48.0,51.05,[T("KNOW WHY",230,140),T("YOU WIN",400,150,GREEN,**fr(1.1)),
  img("v12_why",keys=[{"t":0,"alpha":0},{"t":.3,"alpha":1},{"t":1.1,"angle":0},{"t":1.3,"angle":-.015},{"t":1.5,"angle":0},{"t":3.0,"w":1230,"x":25}])])
shot(51.05,58.32,[T("LESSON #3",210,110,GOLD),T("GET COMFORTABLE",340,110,**fr(.95)),T("WITH AMBIGUITY",450,110,**fr(1.4)),
  T("YOU DON'T NEED TO BE OUTGOING",1500,72,**fr(2.75)),T("BUT ACT BEFORE IT'S CLEAR",1610,80,RED,**fr(4.55)),
  img("v13_fog",x=190,y=560,w=900,keys=[{"t":0,"alpha":0},{"t":.5,"alpha":1,"w":900,"x":190,"y":560},{"t":5.8,"w":930,"x":175,"y":548},{"t":6.0,"w":930,"x":175,"y":558},{"t":6.2,"w":930,"x":175,"y":548},{"t":7.2,"w":950,"x":165,"y":540}])])
shot(58.32,61.15,[T("LESSON #4",210,110,GOLD),T("TEAR IT DOWN.",350,130,RED,**fr(.95)),T("REBUILD.",1560,150,GREEN,**fr(2.05)),
  img("v14_collapse",x=160,w=960,keys=[{"t":0,"alpha":0},{"t":.2,"alpha":1,"angle":0},{"t":.3,"angle":.02},{"t":.4,"angle":-.02},{"t":.5,"angle":.015},{"t":.6,"angle":0},{"t":1.0,"angle":0,"y":480},{"t":1.1,"angle":.02,"y":490},{"t":1.25,"angle":-.015},{"t":1.4,"angle":0,"y":480},{"t":2.8,"w":1000,"x":140}])])
shot(61.15,67.31,[T("EVERY SUCCESS",230,120),T("~ONCE A DECADE",380,120,GOLD,**fr(1.75)),
  {"type":"underline","x":70,"y":480,"w":600,"color":GOLD,"from":2.1,"keys":[{"t":2.1,"progress":0},{"t":2.5,"progress":1}]},
  T("BEFORE YOUR COMPETITORS",1530,90,RED,**fr(3.2)),T("DO IT FOR YOU.",1640,90,RED,**fr(4.4)),
  img("v15_rebuild",y=420,keys=[{"t":0,"alpha":0,"y":520},{"t":.35,"alpha":1,"y":420},{"t":.45,"y":426},{"t":.6,"y":420},{"t":1.7,"w":1180,"x":50},{"t":3.0,"w":1240,"x":20},{"t":6.1,"w":1180,"x":50}])])
chk=lambda x,y,t:{"type":"line","points":[[x,y],[x+30,y+35],[x+85,y-40]],"color":GREEN,"lineWidth":10,"from":t,"keys":[{"t":t,"progress":0},{"t":t+.25,"progress":1}]}
shot(67.31,71.35,[T("SKILL",560,140,x=220,**fr(.75)),chk(110,640,.85),T("INTELLECT",760,140,x=220,**fr(1.35)),chk(110,840,1.45),
  T("TRAINING",960,140,x=220,**fr(2.0)),chk(110,1040,2.1),T("NOT ENOUGH.",1260,160,RED,x=180,**fr(3.0))])
shot(71.35,74.22,[T("PASSION",230,190,RED),T("FOR THE PAINFUL PARTS",430,96,**fr(.9)),
  img("v17_passion",keys=[{"t":0,"alpha":0,"x":110},{"t":.3,"alpha":1,"x":50},{"t":1.5,"y":480},{"t":1.55,"y":470},{"t":1.7,"y":480},{"t":2.8,"x":10,"y":460}])])
shot(74.22,77.14,[T("WHICH LESSON",230,130),T("DO YOU NEED?",380,140,RED,**fr(.5)),
  T("#1 PERSPECTIVE",640,100,**fr(.7)),T("#2 GO AGAINST",800,100,**fr(.9)),T("#3 AMBIGUITY",960,100,**fr(1.1)),T("#4 REBUILD",1120,100,**fr(1.3)),
  img("p_bubble",x=760,y=1240,w=440,**fr(1.65),keys=[{"t":1.65,"w":280,"x":840,"alpha":0},{"t":1.9,"w":460,"x":750,"alpha":1},{"t":2.05,"w":440,"x":760}])])
p={"version":1,"style":"B1","width":1080,"height":1560,"fps":30,"captionSize":56,
   "voice":{"path":"audio/master_mix.wav","lead":0,"tail":0,"contains_sfx":True},"captions":caps,"shots":shots,"sfx":[]}
json.dump(p,open('project.json','w'),indent=1)
print(len(caps),'captions')
