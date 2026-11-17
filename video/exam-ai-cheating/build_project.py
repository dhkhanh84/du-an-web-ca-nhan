import json
L=0.15
cap=[(0.0,1.34,"One wrong answer."),(1.70,2.95,"Out of one hundred sixty."),(3.25,4.6,"That was the first-round score"),(4.6,6.05,"of this year's top candidate"),
(6.05,7.3,"on South Korea's"),(7.3,9.01,"tax accountant exam."),(9.39,10.3,"When people suspected"),(10.3,11.2,"AI glasses,"),(11.2,12.48,"he denied it."),(12.84,14.32,"Days later, he confessed."),
(15.10,16.4,"According to his confession,"),(16.4,17.6,"a tiny camera"),(17.6,19.01,"photographed the questions,"),(19.25,20.9,"an AI app solved them,"),(20.9,22.0,"and he read the answers"),
(22.0,23.2,"on a hidden device,"),(23.2,24.11,"during the exam."),(24.51,25.9,"He says he did the same"),(25.9,27.78,"in both rounds of the tax exam,"),
(27.98,28.9,"and in the first round"),(28.9,29.99,"of the CPA exam."),(30.77,32.3,"Police have seized the camera,"),(32.3,33.9,"and the government is reviewing"),
(33.9,34.7,"this year's national"),(34.7,35.88,"certification exams."),(36.51,37.75,"The camera reportedly cost"),(37.75,39.0,"about eighty dollars."),
(39.36,40.9,"So when AI can answer"),(40.9,41.9,"almost any question,"),(41.9,44.03,"how should exams change?"),(44.45,45.53,"Tell us in the comments.")]
caps=[{"start":round(a+L,3),"end":round(b+L,3),"text":t} for a,b,t in cap]
for c,n in zip(caps,caps[1:]): c['end']=round(min(n['start']-0.02,c['end']+0.35),3)
caps[-1]['end']=round(caps[-1]['end']+0.4,3)
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
tick=lambda x,y,t,c=RED:{"type":"line","points":[[x,y],[x+30,y+35],[x+85,y-40]],"color":c,"lineWidth":10,"from":t,"keys":[{"t":t,"progress":0},{"t":t+.25,"progress":1}]}
shot(0,3.38,[T("1 WRONG.",230,170,RED,keys=[{"t":0,"alpha":0,"x":140},{"t":.25,"alpha":1,"x":70}]),T("OUT OF 160.",420,130,**fr(1.85)),
  img("x01_score",x=290,y=560,w=700,keys=[{"t":0,"alpha":0,"y":600},{"t":.3,"alpha":1,"y":560,"w":700,"x":290},{"t":1.8,"w":700,"x":290,"y":560},{"t":3.3,"w":880,"x":200,"y":520}])])
shot(3.38,9.52,[T("THE TOP SCORER",230,120,GOLD),T("SOUTH KOREA",1530,100,**fr(2.6)),T("TAX ACCOUNTANT EXAM",1640,92,NAVY,**fr(3.2)),
  img("x02_top",x=170,w=940,keys=[{"t":0,"alpha":0,"y":520},{"t":.3,"alpha":1,"y":480},{"t":1.3,"y":480},{"t":1.4,"y":468},{"t":1.6,"y":480},{"t":3.2,"w":940,"x":170},{"t":6.1,"w":980,"x":150}])])
shot(9.52,12.98,[T("AI GLASSES?",230,140,keys=[{"t":0,"alpha":0},{"t":.2,"alpha":1}]),T("\"NO.\"",380,170,RED,x=760,w=480,**fr(1.85)),
  img("x03_deny",keys=[{"t":0,"alpha":0},{"t":.3,"alpha":1},{"t":1.85,"angle":0},{"t":2.0,"angle":.03},{"t":2.15,"angle":-.03},{"t":2.3,"angle":.02},{"t":2.45,"angle":0},{"t":3.4,"w":1220,"x":30}])])
shot(12.98,15.22,[T("DAYS LATER...",230,120),T("HE CONFESSED.",400,140,RED,**fr(.6)),
  img("x04_confess",keys=[{"t":0,"alpha":0,"x":110},{"t":.3,"alpha":1,"x":50},{"t":.6,"y":480},{"t":.7,"y":488},{"t":.85,"y":480},{"t":2.2,"w":1230,"x":25}])])
lab=lambda s,y,t,c=None,size=84:T(s,y,size,c,x=600,w=660,**fr(t))
shot(15.22,24.42,[T("HIS CONFESSION:",230,120,GOLD),
  img("x05_pipeline",x=-120,y=380,w=1100,keys=[{"t": 0, "alpha": 0, "y": 380}, {"t": 0.4, "alpha": 1, "y": 380}, {"t": 1.5, "y": 380}, {"t": 1.58, "y": 392}, {"t": 1.75, "y": 380}, {"t": 2.9, "y": 380}, {"t": 2.98, "y": 392}, {"t": 3.15, "y": 380}, {"t": 4.2, "y": 380}, {"t": 4.28, "y": 392}, {"t": 4.45, "y": 380}, {"t": 5.4, "y": 380}, {"t": 5.48, "y": 392}, {"t": 5.65, "y": 380}, {"t": 6.8, "y": 380}, {"t": 6.88, "y": 392}, {"t": 7.05, "y": 380}, {"t": 8.0, "y": 380}, {"t": 8.08, "y": 392}, {"t": 8.25, "y": 380}]),
  {"type":"arrow","x":440,"y":580,"w":130,"from":1.5,"to":2.9,"keys":[{"t":1.5,"progress":0},{"t":1.75,"progress":1}]},
  {"type":"arrow","x":440,"y":830,"w":130,"from":2.9,"to":4.2,"keys":[{"t":2.9,"progress":0},{"t":3.15,"progress":1}]},
  {"type":"arrow","x":440,"y":1100,"w":130,"from":4.2,"to":6.8,"keys":[{"t":4.2,"progress":0},{"t":4.45,"progress":1},{"t":5.3,"x":440},{"t":5.45,"x":460},{"t":5.6,"x":440}]},
  {"type":"arrow","x":440,"y":1330,"w":130,"from":6.8,"keys":[{"t":6.8,"progress":0},{"t":7.05,"progress":1}]},
  lab("TINY CAMERA",560,1.5),lab("PHOTOS OF",790,2.9),lab("THE QUESTIONS",880,3.0),lab("AI APP SOLVES",1080,4.2,GREEN),
  lab("ANSWERS ON A",1300,6.8),lab("HIDDEN SCREEN",1390,6.9,RED),T("DURING THE EXAM.",1600,100,RED,**fr(8.0))])
rows=[("TAX EXAM, ROUND 1",620,1.6),("TAX EXAM, ROUND 2",820,2.2),("CPA EXAM, ROUND 1",1020,4.1)]
L2=[T("SAME METHOD IN:",230,120,GOLD)]
for s,y,t in rows: L2+= [T(s,y,100,x=220,**fr(t)),tick(110,y+60,t+.05)]
L2+= [img("x04_confess",x=340,y=1180,w=600,keys=[{"t":0,"alpha":0},{"t":.4,"alpha":.9},{"t":5.9,"w":640,"x":320}])]
shot(24.42,30.42,L2)
shot(30.42,36.38,[T("POLICE SEIZED",230,120),T("THE CAMERA.",380,130,RED,**fr(.5)),
  img("x06_evidence",to=2.1,keys=[{"t":0,"alpha":0},{"t":.3,"alpha":1},{"t":.9,"angle":0},{"t":1.05,"angle":.015},{"t":1.2,"angle":0},{"t":2.0,"alpha":.3}]),
  img("x07_review",x=170,w=940,**fr(2.05),keys=[{"t":2.05,"alpha":0,"y":520},{"t":2.4,"alpha":1,"y":480},{"t":3.5,"w":940,"x":170},{"t":5.9,"w":980,"x":150}]),
  T("THIS YEAR'S EXAMS:",1530,92,**fr(3.5)),T("UNDER REVIEW.",1640,100,NAVY,**fr(4.3))])
shot(36.38,39.5,[T("THE CAMERA COST",230,120),T("~$80",380,190,RED,**fr(1.6)),
  img("x08_price",x=140,y=600,w=1000,keys=[{"t":0,"alpha":0},{"t":.3,"alpha":1},{"t":1.6,"y":600},{"t":1.66,"y":610},{"t":1.8,"y":600},{"t":3.1,"w":1060,"x":110}])])
shot(39.5,44.58,[T("WHEN AI CAN ANSWER",230,100),T("ALMOST ANYTHING...",380,110,**fr(1.2)),T("HOW SHOULD EXAMS CHANGE?",1590,86,RED,**fr(2.6)),
  img("x09_hall",keys=[{"t":0,"alpha":0},{"t":.4,"alpha":1,"w":1180,"x":50},{"t":2.6,"y":480},{"t":2.66,"y":470},{"t":2.8,"y":480},{"t":5.0,"w":1240,"x":20}])])
shot(44.58,47.98,[T("TELL US",360,150,keys=[{"t":0,"x":70},{"t":1.9,"x":70},{"t":2.0,"x":82},{"t":2.15,"x":70},{"t":3.0,"x":70},{"t":3.1,"x":82},{"t":3.25,"x":70}]),T("IN THE COMMENTS.",540,120,GREEN,**fr(.3),keys=[{"t":.3,"x":70},{"t":2.4,"x":70},{"t":2.5,"x":58},{"t":2.65,"x":70}]),
  img("p_bubble",x=420,y=850,w=440,**fr(.9),keys=[{"t":.9,"w":280,"x":500,"alpha":0},{"t":1.15,"w":460,"x":410,"alpha":1},{"t":1.3,"w":440,"x":420,"y":850},{"t":1.9,"y":850},{"t":2.0,"y":830},{"t":2.15,"y":850},{"t":2.6,"y":850},{"t":2.7,"y":830},{"t":2.85,"y":850},{"t":3.2,"y":850},{"t":3.3,"y":835},{"t":3.4,"y":850}])])
p={"version":1,"style":"B1","width":1080,"height":1560,"fps":30,"captionSize":56,
   "voice":{"path":"audio/master_mix_norm.wav","lead":0,"tail":0,"contains_sfx":True},"captions":caps,"shots":shots,"sfx":[]}
json.dump(p,open('project.json','w'),indent=1); print(len(caps),'captions')
