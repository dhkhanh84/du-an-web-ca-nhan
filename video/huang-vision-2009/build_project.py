import json
L=0.15
cap=[(0.35,1.70,"Năm 1993,"),(1.92,2.95,"giới đầu tư bảo ông:"),(3.11,4.45,"thị trường game không tồn tại."),(4.73,5.60,"Mẹ ông thì hỏi:"),(5.77,7.10,"sao không đi làm thuê?"),
(7.33,9.10,"Mười sáu năm sau, ở Stanford,"),(9.27,10.30,"Jensen Huang chia sẻ cách ông"),(10.30,11.60,"vượt qua điều đó."),
(11.76,12.70,"Bài học đầu tiên:"),(12.82,14.40,"đừng chờ tầm nhìn vĩ đại."),(14.58,15.95,"Ai cũng có một góc nhìn riêng,"),(16.05,17.50,"và tầm nhìn chỉ là vậy."),
(17.85,20.05,"Góc nhìn của ông năm 1993:"),(20.11,21.20,"lấy đồ họa ba chiều"),(21.20,22.30,"từ những máy trạm đắt tiền,"),(22.39,23.40,"làm cho thật rẻ,"),
(23.47,24.40,"và để trò chơi điện tử"),(24.40,25.90,"kéo cả thị trường đi lên."),
(26.27,27.05,"Bài học thứ hai:"),(27.05,28.75,"có lúc phải đi ngược khách hàng."),(28.94,30.60,"Dell, HP, IBM,"),(30.71,32.80,"Gateway đều chê sản phẩm quá đắt."),
(32.94,34.55,"Ông vẫn dồn mấy triệu đô cuối cùng"),(34.55,35.70,"vào một con chip quá lớn,"),(35.78,37.70,"vì tin công nghệ sẽ rẻ đi rất nhanh."),
(38.12,39.48,"Từng có khoảng hai trăm công ty"),(39.48,40.45,"làm đồ họa ba chiều."),(40.57,41.66,"Tiền, người, công nghệ"),(41.66,42.85,"gần như ngang nhau."),
(42.99,43.60,"Theo ông,"),(43.67,44.71,"ai sống sót là nhờ hiểu"),(44.71,45.76,"vì sao việc kinh doanh"),(45.76,46.70,"của mình chạy được."),
(46.95,47.75,"Bài học thứ ba:"),(47.75,49.45,"tập quen với sự mơ hồ."),(49.67,51.15,"Người lãnh đạo không cần hướng ngoại,"),(51.22,51.94,"nhưng phải dám làm"),(51.94,53.40,"khi chưa thấy hết kết quả."),
(53.63,54.55,"Bài học thứ tư:"),(54.72,55.90,"tự đập đi xây lại."),(56.09,56.94,"Thứ gì thành công rồi"),(56.94,57.80,"cũng phải làm lại,"),(57.91,59.20,"khoảng mười năm một lần."),
(59.45,60.41,"Nếu bạn không tự thay thế"),(60.41,61.20,"sản phẩm của mình,"),(61.33,62.70,"đối thủ sẽ làm thay."),
(62.95,63.50,"Cuối cùng:"),(63.64,64.65,"kỹ năng, trí tuệ, đào tạo"),(64.75,66.70,"đều quan trọng, nhưng chưa đủ."),
(66.87,68.06,"Phải đam mê cả phần đau đớn"),(68.06,69.20,"của việc xây công ty."),(69.39,70.60,"Bạn đang thiếu bài học nào?"),(70.73,72.10,"Bình luận cho mình biết nhé.")]
caps=[{"start":round(a+L,3),"end":round(b+L,3),"text":t} for a,b,t in cap]
RED="#EC4338"; GOLD="#E8A317"; GREEN="#5A9E1A"; NAVY="#27408B"
shots=[]
def img(f,x=50,y=480,w=1180,**k): return dict(type="image",path=f"assets/cut/{f}.png",x=x,y=y,w=w,**k)
def T(t,y,size=110,color=None,x=70,**k):
    d=dict(type="text",text=t,x=x,y=y,size=round(size*1.2),bold=True,**k)
    if color: d['color']=color
    return d
fr=lambda t:{"from":t}
def shot(s,e,layers):
    sp=e-s
    for l in layers:
        for k in l.get('keys',[]): k['t']=round(min(k['t'],sp-0.03),3)
    shots.append({"start":s,"end":e,"layers":layers})
bump=lambda t,dy=10,y=480:[{"t":t,"y":y},{"t":t+.05,"y":y+dy},{"t":t+.2,"y":y}]
shot(0,3.25,[T("1993",300,230,keys=[{"t":0,"alpha":0,"x":140},{"t":.25,"alpha":1,"x":70}]),
  img("v01_pc1993",keys=[{"t":0,"alpha":0},{"t":.35,"alpha":1},{"t":.9,"y":480},{"t":.95,"y":486},{"t":1.1,"y":480},{"t":3.2,"x":30,"w":1220}])])
shot(3.25,4.88,[T("KHÔNG CÓ",230,110),T("THỊ TRƯỜNG GAME",370,100,RED,**fr(.15)),
  img("v02_investors",keys=[{"t":0,"x":110,"alpha":0},{"t":.3,"x":50,"alpha":1},{"t":.75,"angle":0},{"t":.9,"angle":.02},{"t":1.05,"angle":-.02},{"t":1.2,"angle":0}])])
shot(4.88,7.45,[T("MẸ HỎI:",230,110),T("SAO KHÔNG ĐI LÀM THUÊ?",370,76,RED,**fr(.95)),
  img("v03_mom",keys=[{"t":0,"alpha":0,"y":520},{"t":.3,"alpha":1,"y":480},{"t":1.0,"angle":0},{"t":1.25,"angle":.025},{"t":1.5,"angle":0}])])
shot(7.45,11.88,[T("16 NĂM SAU...",230,110),T("STANFORD, 2009",370,110,NAVY,**fr(1.0)),
  img("v04_stage",keys=[{"t":0,"alpha":0},{"t":.4,"alpha":1},{"t":2.0,"w":1180,"x":50},{"t":4.4,"w":1260,"x":10}])])
shot(11.88,17.95,[T("BÀI HỌC #1",210,100,GOLD),T("TẦM NHÌN",350,120,**fr(1.1)),
  {"type":"line","points":[[60,420],[590,405]],"color":RED,"lineWidth":12,"from":1.4,"keys":[{"t":1.4,"progress":0},{"t":1.8,"progress":1}]},
  T("GÓC NHÌN",350,120,GREEN,x=700,w=580,**fr(2.85)),
  img("v05_lens",**fr(2.85),keys=[{"t":2.85,"alpha":0,"y":520},{"t":3.2,"alpha":1,"y":480},{"t":4.3,"w":1180,"x":50},{"t":6.0,"w":1240,"x":20}])])
shot(17.95,23.45,[T("ĐỒ HỌA 3D",230,120),T("ĐẮT",370,130,RED,**fr(2.4)),T("RẺ",370,130,GREEN,x=520,**fr(4.55)),
  {"type":"arrow","x":300,"y":430,"w":190,"from":4.4,"keys":[{"t":4.4,"progress":0},{"t":4.6,"progress":1}]},
  img("v06_workstation",keys=[{"t":0,"alpha":0},{"t":.35,"alpha":1},{"t":2.4,"x":50},{"t":2.6,"x":40},{"t":2.8,"x":50},{"t":5.4,"y":470}])])
shot(23.45,26.42,[T("GAME",230,130,GOLD),T("KÉO CẢ THỊ TRƯỜNG",380,92,**fr(1.0)),
  img("v07_gamepad",keys=[{"t":0,"alpha":0,"y":520},{"t":.3,"alpha":1,"y":480},{"t":1.4,"y":480},{"t":1.45,"y":470},{"t":1.6,"y":480},{"t":2.9,"w":1220,"x":30}])])
shot(26.42,33.09,[T("BÀI HỌC #2",210,100,GOLD),T("ĐI NGƯỢC KHÁCH HÀNG",350,90,**fr(.75)),
  img("v08_boxes",x=50,y=560,w=1180,**fr(2.4),keys=[{"t":2.4,"alpha":0},{"t":2.65,"alpha":1}]),
  T("DELL",780,60,x=130,**fr(2.7)),T("HP",780,60,x=465,**fr(3.15)),T("IBM",780,60,x=735,**fr(3.75)),T("GATEWAY",780,46,x=950,w=330,**fr(4.45)),
  img("stamp",x=300,y=1080,w=700,**fr(5.8),keys=[{"t":5.8,"w":900,"x":200,"alpha":0},{"t":5.95,"w":700,"x":300,"alpha":1}]),
  T("QUÁ ĐẮT!",1160,120,RED,x=420,**fr(5.85))])
shot(33.09,37.85,[T("MẤY TRIỆU ĐÔ",230,110),T("CUỐI CÙNG",370,120,RED,**fr(.9)),T("TIN: CHIP SẼ RẺ ĐI",1600,90,GREEN,**fr(2.9)),
  img("v10_bigchip",keys=[{"t":0,"x":-120,"alpha":0},{"t":.4,"x":50,"alpha":1},{"t":1.5,"x":40},{"t":2.3,"x":50},{"t":3.1,"x":40},{"t":4.7,"x":50}])])
shot(37.85,44.0,[T("~200 ĐỐI THỦ",230,120),T("TIỀN, NGƯỜI, CÔNG NGHỆ: NGANG NHAU",380,56,**fr(2.85)),
  img("dots200",x=140,y=560,w=1000,to=3.75,keys=[{"t":0,"alpha":0},{"t":.4,"alpha":1}]),
  img("dots60",x=140,y=560,w=1000,**fr(3.75),to=4.45),img("dots12",x=140,y=560,w=1000,**fr(4.45),to=5.0),
  img("dots1",x=140,y=560,w=1000,**fr(5.0)),T("CÒN 1.",1600,140,GREEN,x=430,**fr(5.15))])
shot(44.0,47.1,[T("HIỂU VÌ SAO",230,120),T("MÌNH THẮNG",370,130,GREEN,**fr(.8)),
  img("v12_why",keys=[{"t":0,"alpha":0},{"t":.3,"alpha":1},{"t":1.0,"angle":0},{"t":1.2,"angle":-.015},{"t":1.4,"angle":0},{"t":3.0,"w":1230,"x":25}])])
shot(47.1,53.78,[T("BÀI HỌC #3",210,100,GOLD),T("QUEN VỚI MƠ HỒ",350,110,**fr(.7)),
  T("KHÔNG CẦN HƯỚNG NGOẠI",1500,70,**fr(2.7)),T("NHƯNG PHẢI DÁM LÀM",1610,70,RED,**fr(4.3)),
  img("v13_fog",x=140,w=1000,keys=[{"t":0,"alpha":0},{"t":.5,"alpha":1,"w":1000,"x":140,"y":480},{"t":6.6,"w":1060,"x":110,"y":460}])])
shot(53.78,57.9,[T("BÀI HỌC #4",210,100,GOLD),T("TỰ ĐẬP ĐI XÂY LẠI",350,100,RED,**fr(.9)),
  img("v14_collapse",x=160,w=960,keys=[{"t":0,"alpha":0},{"t":.2,"alpha":1,"angle":0},{"t":.3,"angle":.02},{"t":.4,"angle":-.02},{"t":.5,"angle":.015},{"t":.6,"angle":0},{"t":2.4,"angle":0,"y":480,"w":960,"x":160},{"t":2.5,"angle":.02,"y":490},{"t":2.65,"angle":-.015},{"t":2.8,"angle":0,"y":480},{"t":4.1,"w":1020,"x":130}]),
  T("THÀNH CÔNG RỒI",1520,70,**fr(2.45)),T("CŨNG PHẢI LÀM LẠI",1620,70,RED,**fr(3.15))])
shot(57.9,63.1,[T("~10 NĂM MỘT LẦN",230,110),T("TRƯỚC KHI ĐỐI THỦ",1530,80,RED,**fr(3.55)),T("LÀM THAY",1630,80,RED,**fr(3.85)),
  img("v15_rebuild",y=420,keys=[{"t":0,"alpha":0,"y":520},{"t":.35,"alpha":1,"y":420},{"t":.45,"y":426},{"t":.6,"y":420},{"t":1.5,"w":1180,"x":50},{"t":1.6,"y":428},{"t":1.75,"y":420},{"t":2.4,"w":1180,"x":50},{"t":3.4,"w":1240,"x":20},{"t":5.1,"w":1180,"x":50}]),
  {"type":"underline","x":70,"y":395,"w":600,"color":GOLD,"from":1.5,"keys":[{"t":1.5,"progress":0},{"t":1.9,"progress":1}]}])
chk=lambda x,y,t:{"type":"line","points":[[x,y],[x+30,y+35],[x+85,y-40]],"color":GREEN,"lineWidth":10,"from":t,"keys":[{"t":t,"progress":0},{"t":t+.25,"progress":1}]}
shot(63.1,67.0,[T("KỸ NĂNG",560,120,x=220,**fr(.65)),chk(110,640,.75),T("TRÍ TUỆ",760,120,x=220,**fr(1.15)),chk(110,840,1.25),
  T("ĐÀO TẠO",960,120,x=220,**fr(1.55)),chk(110,1040,1.65),T("CHƯA ĐỦ.",1260,150,RED,x=220,**fr(3.0),keys=[{"t":3.0,"w":1100,"alpha":0},{"t":3.2,"alpha":1}])])
shot(67.0,69.5,[T("ĐAM MÊ",230,170,RED),T("CẢ PHẦN ĐAU ĐỚN",440,90,**fr(.7)),
  img("v17_passion",keys=[{"t":0,"alpha":0,"x":110},{"t":.3,"alpha":1,"x":50},{"t":2.4,"x":10,"y":460}])])
shot(69.5,72.26,[T("BẠN THIẾU",230,120),T("BÀI HỌC NÀO?",370,130,RED,**fr(.4)),
  T("#1 GÓC NHÌN",640,90,**fr(.6)),T("#2 ĐI NGƯỢC",800,90,**fr(.8)),T("#3 MƠ HỒ",960,90,**fr(1.0)),T("#4 XÂY LẠI",1120,90,**fr(1.2)),
  img("p_bubble",x=760,y=1240,w=440,**fr(1.4),keys=[{"t":1.4,"w":280,"x":840,"alpha":0},{"t":1.65,"w":460,"x":750,"alpha":1},{"t":1.8,"w":440,"x":760}])])
p={"version":1,"style":"B1","width":1080,"height":1560,"fps":30,"captionSize":54,"font":"fonts/PatrickHand_400Regular.ttf",
   "voice":{"path":"audio/master_mix.wav","lead":0,"tail":0,"contains_sfx":True},"captions":caps,"shots":shots,"sfx":[]}
json.dump(p,open('project.json','w'),indent=1,ensure_ascii=False)
