import json
L=0.15
tools=[("ChatGPT","đã lên ý tưởng và viết hook.","Ý TƯỞNG + HOOK","i01_hook"),("Gemini","đã đặt tên sản phẩm chuẩn SEO.","TÊN SẢN PHẨM CHUẨN SEO","i02_seo"),
("Claude","đã đọc số liệu, phân tích KPI.","SỐ LIỆU + KPI","i03_kpi"),("NotebookLM","đã tổng hợp tài liệu.","TỔNG HỢP TÀI LIỆU","i04_docs"),
("Canva AI","đã thiết kế banner quảng cáo.","BANNER QUẢNG CÁO","i05_banner"),("CapCut AI","đã dựng video, làm phụ đề.","DỰNG VIDEO + PHỤ ĐỀ","i06_film"),
("DeepSeek","đã tìm insight khách hàng.","INSIGHT KHÁCH HÀNG","i07_insight"),("Google AI Studio","đã tạo video AI.","VIDEO AI","i08_camera"),
("ElevenLabs","đã lồng tiếng AI.","LỒNG TIẾNG AI","i09_mic"),("Gamma AI","đã làm slide báo cáo.","SLIDE BÁO CÁO","i10_slides")]
seg=[(3.07,5.46),(6.15,8.86),(9.41,11.80),(12.35,14.45),(14.98,17.64),(18.18,21.00),(21.54,23.62),(24.06,26.70),(27.16,29.30),(29.68,31.92)]
cap=[(0.20,2.30,"Gen Z ngành marketing đi làm kiểu gì?")]
for (a,b),(name,task,_,_) in zip(seg,tools):
    p1=f"Cảm ơn {name}"; tot=len(p1)+len(task); m=a+(b-a)*len(p1)/tot
    if name=="DeepSeek": m=22.19
    cap+=[(a,m,p1),(m,b,task)]
cap+=[(32.40,33.19,"Và cuối cùng,"),(33.51,34.45,"cảm ơn chính mình,"),(34.80,35.75,"vì vẫn sống sót qua"),(35.75,37.10,"bảy bảy bốn chín cái deadline."),
(37.63,37.97,"Còn bạn,"),(38.18,39.46,"đang cảm ơn AI nào nhiều nhất?"),(39.68,40.73,"Bình luận cho mình biết nhé.")]
caps=[{"start":round(a+L,3),"end":round(b+L,3),"text":t} for a,b,t in cap]
for c,n in zip(caps,caps[1:]): c['end']=round(min(n['start']-0.02,c['end']+0.35),3)
caps[-1]['end']=round(caps[-1]['end']+0.5,3)
RED="#EC4338"; GOLD="#E8A317"; GREEN="#5A9E1A"; NAVY="#27408B"; PURPLE="#7B4BC4"; TEAL="#1C8C8C"
shots=[]
def img(f,x=50,y=480,w=1180,**k): return dict(type="image",path=f"assets/cut/{f}.png",x=x,y=y,w=w,**k)
def T(t,y,size=110,color=None,x=70,**k):
    k.setdefault("w",1250-x)
    d=dict(type="text",text=t,x=x,y=y,size=round(size*1.2),bold=True,**k)
    if color: d['color']=color
    return d
fr=lambda t:{"from":t}
def shot(s,e,layers):
    sp=e-s
    for l in layers:
        for k in l.get('keys',[]): k['t']=round(min(k['t'],sp-0.03),3)
    shots.append({"start":s,"end":e,"layers":layers})
shot(0,3.22,[T("GEN Z MARKETING",230,110,keys=[{"t":0,"alpha":0,"x":140},{"t":.25,"alpha":1,"x":70}]),T("ĐI LÀM KIỂU GÌ?",380,120,RED,**fr(1.0)),
  img("g01_chill",keys=[{"t":0,"alpha":0,"y":520},{"t":.3,"alpha":1,"y":480},{"t":1.0,"angle":0},{"t":1.2,"angle":.02},{"t":1.4,"angle":0},{"t":2.2,"y":480},{"t":2.3,"y":470},{"t":2.45,"y":480}])])
cols=[GREEN,NAVY,GOLD,PURPLE,TEAL,RED,NAVY,GREEN,PURPLE,GOLD]
bounds=[s+L for s,_ in seg]+[32.5]
for i,((name,task,label,icon),c) in enumerate(zip(tools,cols)):
    s0=0 if i==0 else 0; s,e=bounds[i],bounds[i+1]
    s=3.22 if i==0 else s; sp=e-s
    tl=round((seg[i][0]+L+(seg[i][1]-seg[i][0])*0.45)-s,2)
    char="g03_cheers" if i%2==0 else "g01_chill"
    shot(s,e,[T(f"CẢM ƠN #{i+1}",230,80,GOLD),T(name.upper(),360,120 if len(name)<12 else 100,c,**fr(.1)),
      img(icon,x=60,y=560,w=680,keys=[{"t":0,"w":440,"x":180,"y":680,"alpha":0},{"t":.18,"w":720,"x":40,"y":540,"alpha":1},{"t":.3,"w":680,"x":60,"y":560},
        {"t":tl,"angle":0},{"t":tl+.12,"angle":.06},{"t":tl+.24,"angle":-.05},{"t":tl+.36,"angle":0},{"t":sp-.05,"w":710,"x":45,"y":545}]),
      img(char,x=700,y=820,w=600,keys=[{"t":0,"alpha":0,"x":780},{"t":.3,"alpha":1,"x":700},{"t":1.6,"y":820},{"t":1.7,"y":806},{"t":1.85,"y":820}]),
      T(label,1520,72,**fr(tl))])
shot(32.5,37.75,[T("VÀ CUỐI CÙNG...",230,100),T("CẢM ƠN CHÍNH MÌNH!",380,100,RED,**fr(1.15)),
  T("SỐNG SÓT QUA",1480,80,**fr(2.5)),T("7749 DEADLINE",1590,110,GOLD,**fr(3.1)),
  img("g04_deadline",keys=[{"t":0,"alpha":0,"y":380},{"t":.35,"alpha":1,"y":480},{"t":.45,"y":472},{"t":.6,"y":480},{"t":1.15,"angle":0},{"t":1.3,"angle":.02},{"t":1.45,"angle":-.02},{"t":1.6,"angle":0},
    {"t":3.1,"w":1180,"x":50,"y":480},{"t":3.2,"w":1210,"x":35,"y":470},{"t":3.35,"w":1180,"x":50,"y":480},{"t":4.5,"angle":0},{"t":4.65,"angle":.02},{"t":4.8,"angle":0}])])
shot(37.75,42.88,[T("CÒN BẠN?",230,140),T("CẢM ƠN AI NÀO NHIỀU NHẤT?",400,80,RED,**fr(.58)),
  img("g05_point",x=90,y=520,w=900,keys=[{"t":0,"alpha":0,"x":160},{"t":.3,"alpha":1,"x":90},{"t":1.3,"y":520},{"t":1.4,"y":508},{"t":1.55,"y":520},{"t":3.4,"y":520},{"t":3.5,"y":508},{"t":3.65,"y":520},{"t":5.0,"w":940,"x":70}]),
  img("p_bubble",x=800,y=1150,w=400,**fr(2.05),keys=[{"t":2.05,"w":250,"x":880,"alpha":0},{"t":2.3,"w":420,"x":790,"alpha":1},{"t":2.45,"w":400,"x":800,"y":1150},{"t":4.2,"y":1150},{"t":4.3,"y":1132},{"t":4.45,"y":1150}])])
p={"version":1,"style":"B1","width":1080,"height":1560,"fps":30,"captionSize":56,"font":"fonts/PatrickHand_400Regular.ttf",
   "voice":{"path":"audio/master_mix_norm.wav","lead":0,"tail":0,"contains_sfx":True},"captions":caps,"shots":shots,"sfx":[]}
json.dump(p,open('project.json','w'),indent=1,ensure_ascii=False); print(len(caps),'captions',len(shots),'shots')
