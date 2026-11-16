import json
L=0.15
segs=[(0.29,1.33,["Năm 2009,"]),(1.60,3.21,["khi AI còn chưa bùng nổ,"]),(3.56,5.65,["thông điệp của Jensen Huang","ở Stanford là:"]),
(5.95,7.03,["đừng chỉ nghe khách hàng."]),(7.47,8.69,["Hãy nghe Định luật Moore."]),
(9.66,13.88,["Định luật Moore dự đoán","số transistor trên chip","sẽ tăng gấp đôi","sau mỗi khoảng hai năm."]),
(14.54,16.98,["Hầu hết công ty dùng quy luật này","để dự báo kỹ thuật."]),(17.52,19.55,["Jensen dùng nó","để dự báo tương lai."]),
(20.49,21.23,["Thập niên 90,"]),(21.54,23.08,["khách hàng chỉ muốn game đẹp hơn."]),
(23.65,27.12,["Nhưng NVIDIA liên tục làm GPU","mạnh gấp nhiều lần","nhu cầu thực tế."]),(27.74,28.83,["Khách hàng chê quá đắt."]),
(29.30,30.24,["Jensen thì nghĩ:"]),(30.82,32.53,["Khi sức mạnh tính toán","tăng đủ nhanh,"]),(32.91,34.62,["những ứng dụng hoàn toàn mới","sẽ xuất hiện."]),
(35.40,36.74,["Ông đặt cược vào GPU."]),(37.19,38.30,["Sau đó là CUDA."]),(38.71,39.77,["Sau đó là AI."]),(40.36,41.14,["15 năm sau,"]),
(41.43,44.50,["cả thế giới chạy đua xây AI","bằng chính con chip NVIDIA."]),(45.46,46.92,["Bài học lớn nhất từ Jensen Huang:"]),
(47.52,48.81,["Khách hàng nói về hiện tại."]),(49.32,50.60,["Công nghệ nói về tương lai."]),(51.21,52.08,["Những công ty vĩ đại"]),
(52.36,53.60,["không chỉ dự đoán nhu cầu."]),(54.00,56.89,["Họ dự đoán nơi mà công nghệ","sẽ đưa nhân loại đến tiếp theo."])]
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
    d=dict(type="text",text=t,x=x,y=y,size=round(size*1.2),bold=True,**k)
    if color: d['color']=color
    return d
fr=lambda t:{"from":t}
def shot(s,e,layers):
    sp=e-s
    for l in layers:
        for k in l.get('keys',[]): k['t']=round(min(k['t'],sp-0.03),3)
    shots.append({"start":s,"end":e,"layers":layers})
shot(0,3.7,[T("2009",300,210,keys=[{"t":0,"alpha":0,"x":140},{"t":.25,"alpha":1,"x":70}]),T("AI CHƯA BÙNG NỔ",300,72,GOLD,x=560,w=700,**fr(1.6)),
  img("v04_stage",keys=[{"t":0,"alpha":0},{"t":.35,"alpha":1},{"t":1.6,"y":480},{"t":1.65,"y":487},{"t":1.8,"y":480},{"t":3.7,"w":1240,"x":20}])])
shot(3.7,9.6,[T("THÔNG ĐIỆP Ở STANFORD:",230,80),T("KHÔNG CHỈ KHÁCH HÀNG.",380,86,RED,**fr(2.4)),
  T("HÃY NGHE ĐỊNH LUẬT MOORE.",1580,80,GREEN,**fr(3.9)),
  img("n01_listen",keys=[{"t":0,"alpha":0,"x":110},{"t":.35,"alpha":1,"x":50},{"t":2.4,"angle":0},{"t":2.55,"angle":-.015},{"t":2.7,"angle":0},{"t":3.9,"w":1180,"x":50},{"t":5.9,"w":1240,"x":20}])])
cl=[]
for i,n in enumerate([1,2,4,8,16,32,64]):
    t0=.5+i*.6; d=img(f"chip{n}",x=190,y=560,w=900,**fr(t0))
    if i<6: d['to']=round(t0+.6,2)
    d['keys']=[{"t":t0,"w":930,"x":175},{"t":t0+.12,"w":900,"x":190}]; cl.append(d)
shot(9.6,14.6,[T("ĐỊNH LUẬT MOORE",230,110),T("TRANSISTOR x2",400,100,GREEN,**fr(2.3)),T("~2 NĂM MỘT LẦN",1580,92,**fr(3.4))]+cl)
shot(14.6,20.5,[T("NGƯỜI KHÁC: DỰ BÁO KỸ THUẬT",230,72),T("JENSEN: DỰ BÁO TƯƠNG LAI",380,80,GREEN,**fr(3.05)),
  img("v12_why",to=3.0,keys=[{"t":0,"alpha":0},{"t":.3,"alpha":1},{"t":1.4,"angle":0},{"t":1.55,"angle":-.015},{"t":1.7,"angle":0},{"t":2.95,"alpha":.2}]),
  img("v05_lens",**fr(3.0),keys=[{"t":3.0,"alpha":0,"y":520},{"t":3.35,"alpha":1,"y":480,"w":1180,"x":50},{"t":4.3,"y":480,"angle":0},{"t":4.45,"y":470,"angle":.015},{"t":4.6,"y":480,"angle":0},{"t":5.9,"w":1260,"x":10}])])
shot(20.5,23.7,[T("THẬP NIÊN 90",230,120,NAVY),T("KHÁCH HÀNG MUỐN",390,90,**fr(1.15)),T("GAME ĐẸP HƠN!",1580,100,GOLD,**fr(1.6)),
  img("n02_gamers",keys=[{"t":0,"alpha":0},{"t":.3,"alpha":1},{"t":1.15,"y":480},{"t":1.2,"y":472},{"t":1.35,"y":480},{"t":3.2,"w":1230,"x":25}])])
shot(23.7,27.75,[T("MẠNH GẤP NHIỀU LẦN",230,100,GREEN),T("NHU CẦU THỰC TẾ",390,100,**fr(2.0)),
  img("n03_overpowered",keys=[{"t":0,"alpha":0,"x":-80},{"t":.4,"alpha":1,"x":50},{"t":2.0,"y":480},{"t":2.06,"y":490},{"t":2.2,"y":480},{"t":4.0,"w":1230,"x":25}])])
shot(27.75,30.85,[T("KHÁCH HÀNG:",230,100),T("\"QUÁ ĐẮT!\"",380,120,RED,**fr(.25)),T("JENSEN THÌ NGHĨ KHÁC.",1570,80,GREEN,**fr(1.65)),
  img("v02_investors",keys=[{"t":0,"alpha":0},{"t":.3,"alpha":1},{"t":.6,"angle":0},{"t":.75,"angle":.02},{"t":.9,"angle":-.02},{"t":1.05,"angle":0},{"t":3.1,"w":1220,"x":30}])])
shot(30.85,35.45,[T("SỨC MẠNH TÍNH TOÁN TĂNG",230,80),T("= ỨNG DỤNG MỚI",380,100,GREEN,**fr(2.2)),
  img("n05_apps",x=-200,y=330,w=1680,keys=[{"t":0,"alpha":0,"w":1500,"x":-110,"y":420},{"t":.5,"alpha":1,"w":1680,"x":-200,"y":330},{"t":2.2,"w":1680,"x":-200},{"t":2.3,"w":1710,"x":-215},{"t":2.45,"w":1680,"x":-200},{"t":4.6,"w":1760,"x":-240}])])
bx=lambda y,t:img("box",x=430,y=y,w=420,**fr(t),keys=[{"t":t,"alpha":0,"w":470,"x":405},{"t":t+.15,"alpha":1,"w":420,"x":430}])
dn=lambda y,t:{"type":"line","points":[[640,y],[640,y+70]],"color":"#444444","lineWidth":7,"from":t,"keys":[{"t":t,"progress":0},{"t":t+.2,"progress":1}]}
shot(35.45,40.42,[T("NHỮNG CANH BẠC",230,110,GOLD),bx(600,1.0),T("GPU",680,100,x=545,**fr(1.05)),dn(860,2.1),bx(950,2.3),T("CUDA",1030,100,x=520,**fr(2.35)),
  dn(1210,3.6),bx(1300,3.8),T("AI",1380,110,GREEN,x=595,**fr(3.85))])
shot(40.42,45.55,[T("15 NĂM SAU",230,110),T("CUỘC ĐUA AI",380,120,GREEN,**fr(1.2)),T("CHẠY BẰNG CHIP NVIDIA.",1580,84,**fr(3.0)),
  img("n04_datacenter",keys=[{"t":0,"alpha":0},{"t":.4,"alpha":1,"w":1180,"x":50},{"t":1.2,"y":480},{"t":1.25,"y":488},{"t":1.4,"y":480},{"t":5.1,"w":1260,"x":10}])])
shot(45.55,51.3,[T("BÀI HỌC LỚN NHẤT",230,110,GOLD),T("KHÁCH HÀNG = HIỆN TẠI",1480,80,**fr(2.1)),T("CÔNG NGHỆ = TƯƠNG LAI",1600,80,GREEN,**fr(3.9)),
  img("n01_listen",x=140,y=420,w=1000,keys=[{"t":0,"alpha":0},{"t":.3,"alpha":1},{"t":2.1,"angle":0},{"t":2.25,"angle":.015},{"t":2.4,"angle":0},{"t":3.9,"y":420},{"t":3.95,"y":428},{"t":4.1,"y":420},{"t":5.7,"w":1040,"x":120}])])
shot(51.3,57.04,[T("KHÔNG CHỈ ĐOÁN NHU CẦU.",230,84,**fr(1.2)),T("MÀ ĐOÁN HƯỚNG CÔNG NGHỆ.",380,84,GREEN,**fr(2.85)),
  img("v10_bigchip",keys=[{"t":0,"alpha":0,"x":-100},{"t":.4,"alpha":1,"x":50},{"t":1.2,"x":40},{"t":2.0,"x":50},{"t":2.85,"y":490},{"t":3.0,"y":480},{"t":3.9,"x":40},{"t":4.8,"x":50},{"t":5.7,"x":40}])])
shot(57.04,59.44,[T("THEO BẠN,",260,100),T("AI ĐANG Ở GIAI ĐOẠN NÀO",420,80,**fr(.2)),T("CỦA \"MOORE MOMENT\"?",560,100,GREEN,**fr(.55)),
  img("p_bubble",x=420,y=900,w=440,**fr(1.2),keys=[{"t":1.2,"w":280,"x":500,"alpha":0},{"t":1.45,"w":460,"x":410,"alpha":1},{"t":1.6,"w":440,"x":420}])])
p={"version":1,"style":"B1","width":1080,"height":1560,"fps":30,"captionSize":56,"font":"fonts/PatrickHand_400Regular.ttf",
   "voice":{"path":"audio/master_mix_norm.wav","lead":0,"tail":0,"contains_sfx":True},"captions":caps,"shots":shots,"sfx":[]}
json.dump(p,open('project.json','w'),indent=1,ensure_ascii=False); print(len(caps),'captions')
