import json
L=0.15
cap=[(0.35,1.48,"Mười thói quen nhỏ,"),(1.73,3.34,"giúp bạn khỏe hơn mỗi ngày."),(4.18,6.30,"Một, bớt xem tin tức tiêu cực."),(7.11,9.55,"Hai, đi ngủ trước mười một giờ đêm."),
(10.38,12.53,"Ba, để điện thoại xa giường ngủ."),(13.36,15.10,"Bốn, mỗi ngày dành vài phút"),(15.10,16.77,"hít thở sâu và chậm."),
(17.71,19.57,"Năm, đi bộ ba mươi phút,"),(19.88,21.09,"tốt nhất là ngoài trời."),(21.97,23.30,"Sáu, phơi nắng"),(23.30,24.46,"mười đến mười lăm phút."),
(25.32,26.89,"Bảy, ăn bớt đồ ngọt."),(27.84,29.81,"Tám, giữ nhà cửa gọn gàng."),(30.67,32.16,"Chín, không tranh cãi,"),(32.42,33.35,"nhất là trên mạng."),
(34.29,35.40,"Mười, trò chuyện"),(35.40,36.91,"với người thân và bạn bè."),(37.88,39.22,"Chỉ cần làm được vài điều,"),(39.52,41.14,"cơ thể cũng sẽ biết ơn bạn."),
(42.01,43.62,"Bạn đang làm được mấy điều rồi?"),(43.86,45.09,"Bình luận cho mình biết nhé.")]
caps=[{"start":round(a+L,3),"end":round(b+L,3),"text":t} for a,b,t in cap]
for c,n in zip(caps,caps[1:]): c['end']=round(min(n['start']-0.02,c['end']+0.35),3)
caps[-1]['end']=round(caps[-1]['end']+0.6,3)
RED="#EC4338"; GOLD="#E8A317"; GREEN="#5A9E1A"; NAVY="#27408B"
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
shot(0,4.33,[T("10 THÓI QUEN NHỎ",230,100),T("ĐỂ KHỎE HƠN MỖI NGÀY",380,84,GREEN,**fr(1.6)),
  img("k01_tired",keys=[{"t":0,"alpha":0,"y":520},{"t":.3,"alpha":1,"y":480},{"t":.4,"angle":0},{"t":.55,"angle":.015},{"t":.7,"angle":0},{"t":1.9,"y":480},{"t":2.0,"y":470},{"t":2.15,"y":480},{"t":4.3,"w":1240,"x":20}])])
H=[("BỚT TIN TIÊU CỰC","h01",None,None),("NGỦ TRƯỚC 11 GIỜ","h02",None,None),("ĐIỆN THOẠI XA GIƯỜNG","h03",None,None),("HÍT THỞ SÂU, CHẬM","h04",None,None),
   ("ĐI BỘ 30 PHÚT","h05","k03_walk","TỐT NHẤT LÀ NGOÀI TRỜI"),("PHƠI NẮNG 10-15 PHÚT","h06",None,None),("BỚT ĐỒ NGỌT","h07",None,None),
   ("NHÀ CỬA GỌN GÀNG","h08",None,None),("KHÔNG TRANH CÃI","h09",None,"NHẤT LÀ TRÊN MẠNG"),("TRÒ CHUYỆN VỚI NGƯỜI THÂN","h10","k05_chat",None)]
nums=[4.33,7.26,10.53,13.51,17.86,22.12,25.47,27.99,30.82,34.44,38.0]
phr=[4.85,7.81,10.92,14.05,18.38,22.73,26.02,28.44,31.31,34.98]
subt=[None,None,None,None,19.88,None,None,None,32.42,None]
cols=[RED,NAVY,GREEN,GREEN,GOLD,GOLD,RED,GREEN,RED,GREEN]
for i,(label,icon,char,sub) in enumerate(H):
    s,e=nums[i],nums[i+1]; sp=e-s; tp=round(phr[i]+L-s,2)
    L1=[T(f"{i+1}",200,230,cols[i],keys=[{"t":0,"alpha":0,"x":120},{"t":.2,"alpha":1,"x":70}]),T(label,300,88 if len(label)<20 else (74 if len(label)<23 else 62),x=330 if i<9 else 380,w=930 if i<9 else 880,**fr(tp))]
    if char:
        L1+=[img(char,x=140,y=440,w=1000,**fr(.0),keys=[{"t":0,"alpha":0,"y":480},{"t":.3,"alpha":1,"y":440},{"t":tp+.6,"y":440},{"t":tp+.7,"y":430},{"t":tp+.85,"y":440},{"t":sp-.05,"w":1040,"x":120}]),
             img(icon,x=880,y=1290,w=320,**fr(tp),keys=[{"t":tp,"w":200,"x":940,"alpha":0},{"t":tp+.2,"w":340,"x":870,"alpha":1},{"t":tp+.3,"w":320,"x":880}])]
    else:
        wide=icon in("h03","h08"); w=1100 if wide else 840; x=(1280-w)//2
        L1+=[img(icon,x=x,y=560,w=w,keys=[{"t":0,"w":w*.6,"x":x+w*.2,"y":700,"alpha":0},{"t":.2,"w":w*1.05,"x":x-w*.025,"y":540,"alpha":1},{"t":.32,"w":w,"x":x,"y":560},
             {"t":tp,"angle":0},{"t":tp+.12,"angle":.05},{"t":tp+.24,"angle":-.04},{"t":tp+.36,"angle":0},{"t":sp-.05,"w":w*1.04,"x":x-w*.02,"y":550}])]
    if sub: L1+=[T(sub,1560 if not char else 1560,80,GREEN if i==4 else RED,**fr(round(subt[i]+L-s,2)))]
    shot(s,e,L1)
shot(38.0,42.16,[T("CƠ THỂ SẼ",230,110),T("BIẾT ƠN BẠN!",380,130,GREEN,**fr(1.65)),
  img("k04_happy",keys=[{"t":0,"alpha":0,"y":520},{"t":.35,"alpha":1,"y":480},{"t":1.65,"y":480},{"t":1.75,"y":468},{"t":1.9,"y":480},{"t":4.1,"w":1240,"x":20}])])
grid=[]
for k in range(10):
    cx=150+(k%5)*220; cy=700+(k//5)*240; t=.35+k*.1
    bt=2.0+k*.32
    grid+=[img(f"h{k+1:02d}",x=cx-10,y=cy-110,w=170,**fr(t),keys=[{"t":t,"alpha":0,"y":cy-110},{"t":t+.15,"alpha":1},{"t":bt,"y":cy-110},{"t":bt+.1,"y":cy-135},{"t":bt+.25,"y":cy-110}])]
shot(42.16,47.52,[T("BẠN LÀM ĐƯỢC",230,110),T("MẤY ĐIỀU RỒI?",380,120,RED,**fr(.4),keys=[{"t":.4,"x":70},{"t":4.6,"x":70},{"t":4.7,"x":84},{"t":4.85,"x":70}])]+grid+[
  img("p_bubble",x=420,y=1200,w=420,**fr(1.85),keys=[{"t":1.85,"w":260,"x":500,"alpha":0},{"t":2.1,"w":440,"x":410,"alpha":1},{"t":2.25,"w":420,"x":420,"y":1200},{"t":3.3,"y":1200},{"t":3.4,"y":1182},{"t":3.55,"y":1200},{"t":4.6,"y":1200},{"t":4.7,"y":1182},{"t":4.85,"y":1200}])])
p={"version":1,"style":"B1","width":1080,"height":1560,"fps":30,"captionSize":56,"font":"fonts/PatrickHand_400Regular.ttf",
   "voice":{"path":"audio/master_mix_norm.wav","lead":0,"tail":0,"contains_sfx":True},"captions":caps,"shots":shots,"sfx":[]}
json.dump(p,open('project.json','w'),indent=1,ensure_ascii=False); print(len(caps),'captions',len(shots),'shots')
