import json
L=0.15
cap=[(0.25,1.76,"Nvidia's Jensen Huang"),(1.76,2.90,"just resigned."),(3.31,4.25,"The headlines say:"),(4.49,5.74,"a reported affair,"),
(6.03,7.90,"and a woman U.S. officials"),(8.06,9.24,"call a Chinese spy."),(9.73,10.43,"But rewind."),(10.87,12.20,"In 2022,"),
(12.56,14.70,"Washington banned his best AI chips"),(14.70,15.44,"from China."),(15.70,16.58,"So Huang built"),(16.58,18.09,"a weaker chip for China."),
(18.42,19.65,"In 2025,"),(19.90,20.88,"that was banned too."),(21.46,22.50,"So he went to Trump,"),(22.67,23.44,"and made a deal:"),
(23.83,24.65,"sell the chips,"),(24.65,26.31,"and give the government a cut."),(26.63,27.93,"First fifteen percent."),(28.24,29.16,"Then twenty-five."),
(29.56,31.05,"China hawks hated it."),(31.56,33.56,"Then, in October 2026,"),(33.73,34.55,"U.S. officials told"),(34.55,35.50,"the New York Times"),
(35.50,36.40,"about the relationship"),(36.40,37.42,"and the spy claim."),(37.96,39.50,"Beijing calls it fabrication."),(40.01,40.71,"Two weeks later,"),(40.87,41.57,"he was out."),
(42.03,43.50,"A real security risk?"),(43.50,45.03,"Or a dealmaker removed?"),(45.47,46.70,"The public has not seen"),(46.70,47.25,"the evidence."),(47.61,48.29,"What do you think?")]
caps=[{"start":round(a+L,3),"end":round(b+L,3),"text":t} for a,b,t in cap]
RED="#EC4338"; GOLD="#E8A317"; NAVY="#27408B"
shots=[]
def shot(s,e,layers):
    sp=e-s
    for l in layers:
        for k in l.get('keys',[]): k['t']=round(min(k['t'],sp-0.03),3)
        if 'from' in l: l['from']=round(l['from'],3)
    shots.append({"start":s,"end":e,"layers":layers})
def img(f,x=50,y=480,w=1180,**k): return dict(type="image",path=f"assets/cut/{f}.png",x=x,y=y,w=w,**k)
def T(t,y,size=120,color=None,x=70,**k):
    d=dict(type="text",text=t,x=x,y=y,size=size,bold=True,**k)
    if color: d['color']=color
    return d
fr=lambda t:{"from":t}
fadein=lambda t0=0,d=.3,**o:[dict(t=t0,alpha=0,**o),dict(t=t0+d,alpha=1)]
shots_def=[
 (0,3.35,[img("s01_resign",keys=[{"t":0,"x":50},{"t":.7,"x":50},{"t":.75,"y":488},{"t":.9,"y":480},{"t":1.9,"x":50},{"t":3.3,"x":10}]),
          T("NVIDIA'S CEO",250,110),T("RESIGNED.",390,150,RED,**fr(1.75))]),
 (3.35,9.80,[img("s02_news",keys=[{"t":0,"y":620,"angle":-.3,"alpha":0},{"t":.35,"y":480,"angle":0,"alpha":1},{"t":4.8,"angle":0},{"t":5.1,"angle":.03},{"t":5.4,"angle":0}]),
          T("THE HEADLINES:",250,110),T("A REPORTED AFFAIR.",390,100,**fr(1.3)),T("AN ALLEGED SPY.",1560,110,RED,**fr(2.85)),
          {"type":"underline","x":70,"y":1690,"w":640,"color":RED,"from":4.7,"keys":[{"t":4.7,"progress":0},{"t":5.1,"progress":1}]}]),
 (9.80,11.0,[img("s03_rewind",keys=[{"t":0,"angle":.06},{"t":.4,"angle":-.08},{"t":.8,"angle":.04},{"t":1.15,"angle":-.06}]),T("BUT REWIND.",280,150,NAVY)]),
 (11.0,15.75,[T("2022",330,200),img("s04_ban",**fr(1.6),keys=[{"t":1.6,"y":440,"alpha":0},{"t":1.85,"y":480,"alpha":1},{"t":2.35,"y":480},{"t":2.4,"y":492},{"t":2.55,"y":480},{"t":3.9,"x":50},{"t":4.0,"x":30},{"t":4.15,"x":50}]),
          T("BANNED.",350,140,RED,x=540,**fr(2.4)),T("NO TOP CHIPS FOR CHINA.",1570,88,**fr(3.85))]),
 (15.75,18.4,[img("s05_small",keys=[{"t":0,"x":120,"alpha":0},{"t":.3,"x":50,"alpha":1},{"t":1.0,"y":480},{"t":1.1,"y":466},{"t":1.3,"y":480}]),
          T("SO HE BUILT",250,110),T("A WEAKER CHIP.",390,120,GOLD,**fr(0.95))]),
 (18.4,21.5,[T("2025",330,200),img("s06_ban2",**fr(1.65),keys=[{"t":1.65,"alpha":0,"y":480},{"t":1.85,"alpha":1,"y":480},{"t":1.9,"y":494},{"t":2.1,"y":480}]),
          T("BANNED",250,130,RED,x=560,**fr(1.9)),T("AGAIN.",390,130,RED,x=560,**fr(2.3))]),
 (21.5,24.75,[img("s07_deal",keys=[{"t":0,"x":-60,"alpha":0},{"t":.35,"x":50,"alpha":1},{"t":1.5,"y":480},{"t":1.56,"y":490},{"t":1.7,"y":480},{"t":2.5,"w":1180,"x":50},{"t":3.2,"w":1230,"x":25}]),
          T("HE WENT TO TRUMP.",250,105),T("THE DEAL:",390,130,RED,**fr(1.35)),T("SELL THE CHIPS...",1570,100,**fr(2.5))]),
 (24.75,29.6,[img("s08_cut",keys=[{"t":0,"alpha":0,"y":520},{"t":.3,"alpha":1,"y":480},{"t":2.35,"y":480},{"t":2.42,"y":490},{"t":2.6,"y":480},{"t":3.95,"y":480},{"t":4.02,"y":492},{"t":4.2,"y":480}]),
          T("...AND WASHINGTON",250,100),T("TAKES A CUT.",390,120,GOLD,**fr(0.85)),T("15%",1500,170,**fr(2.35)),T("25%",1480,200,RED,x=600,**fr(3.95))]),
 (29.6,31.6,[img("s09_hawks",keys=[{"t":0,"alpha":.2,"y":500},{"t":.25,"alpha":1,"y":480},{"t":1.0,"angle":0},{"t":1.2,"angle":.015},{"t":1.4,"angle":-.015},{"t":1.6,"angle":0}]),
          T("CHINA HAWKS",250,120),T("HATED IT.",390,140,RED,**fr(0.9))]),
 (31.6,37.75,[T("OCTOBER 2026",300,140),img("s10_leak",**fr(2.2),keys=[{"t":2.2,"x":130,"alpha":0},{"t":2.55,"x":50,"alpha":1},{"t":4.2,"w":1180,"x":50},{"t":5.9,"w":1240,"x":20}]),
          T("OFFICIALS TALK TO THE PRESS.",440,78,**fr(3.0)),T("THE SPY CLAIM.",1560,120,RED,**fr(4.9))]),
 (37.75,39.9,[img("s11_deny",keys=[{"t":0,"alpha":.2},{"t":.25,"alpha":1,"angle":0},{"t":.7,"angle":.02},{"t":1.0,"angle":-.02},{"t":1.3,"angle":.02},{"t":1.6,"angle":0}]),
          T("BEIJING:",250,120),T('"FABRICATION."',390,130,RED,**fr(1.15))]),
 (39.9,42.1,[img("s12_out",keys=[{"t":0,"alpha":0},{"t":.4,"alpha":1},{"t":2.1,"y":470}]),T("TWO WEEKS LATER...",250,105),T("HE WAS OUT.",400,150,RED,**fr(1.1))]),
 (42.1,45.4,[img("s13_scale",keys=[{"t":0,"angle":0},{"t":.5,"angle":-.05},{"t":1.4,"angle":-.05},{"t":2.0,"angle":.05},{"t":2.8,"angle":.05},{"t":3.2,"angle":0}]),
          T("A SECURITY RISK?",250,115,NAVY),T("OR A DEALMAKER REMOVED?",1570,88,RED,**fr(1.5))]),
 (45.4,48.74,[img("s14_file",keys=[{"t":0,"alpha":0,"y":440},{"t":.3,"alpha":1,"y":480},{"t":.6,"y":480},{"t":.65,"y":490},{"t":.8,"y":480}]),
          T("NO PUBLIC EVIDENCE.",250,100,**fr(0.5)),T("YOU DECIDE.",400,150,RED,**fr(2.3)),
          img("p_bubble",x=760,y=1300,w=460,**fr(2.35),keys=[{"t":2.35,"w":300,"x":840,"alpha":0},{"t":2.6,"w":480,"x":750,"alpha":1},{"t":2.75,"w":460,"x":760}])]),
]
for s,e,l in shots_def: shot(s,e,l)
p={"version":1,"style":"B1","width":1080,"height":1560,"fps":30,"captionSize":60,
   "voice":{"path":"audio/master_mix.wav","lead":0,"tail":0,"contains_sfx":True},"captions":caps,"shots":shots,"sfx":[]}
json.dump(p,open('project.json','w'),indent=1)
