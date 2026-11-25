import json
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from vi_script import VI, CH_VI, VIDEO_TITLE_VI, TOC_TITLE_VI
RATE=3.5; GAP=0.7; CHGAP=1.8
d=json.load(open('scenes.json')); sc=d['scenes']
assert set(VI)=={s['code'] for s in sc}, set(VI)^{s['code'] for s in sc}
def syl(t): return len(t.split())
doc=Document(); sec=doc.sections[0]; sec.orientation=WD_ORIENT.LANDSCAPE
sec.page_width,sec.page_height=Cm(29.7),Cm(21)
for m in ('left_margin','right_margin','top_margin','bottom_margin'): setattr(sec,m,Cm(1.6))
st=doc.styles['Normal']; st.font.name='Arial'; st.font.size=Pt(10); st.element.rPr.rFonts.set(qn('w:eastAsia'),'Arial')
def shade(c,h):
    p=c._tc.get_or_add_tcPr(); s=OxmlElement('w:shd'); s.set(qn('w:val'),'clear'); s.set(qn('w:fill'),h); p.append(s)
tot=sum(syl(VI[s['code']][1]) for s in sc); mins=(tot/RATE+len(sc)*GAP+17*CHGAP)/60
doc.add_heading(f'{VIDEO_TITLE_VI}: kịch bản tiếng Việt (bản đề xuất)',0)
tots=f'{tot:,}'.replace(',', '.'); rates=str(RATE).replace('.', ',')
doc.add_paragraph(f'Phiên bản tiếng Việt của video, dịch từ kịch bản tiếng Anh rút gọn đã duyệt (kịch bản tiếng Anh giữ nguyên). '
  f'Giữ nguyên 122 tranh, trang mục lục và thứ tự 17 chương. Lời dẫn: {tots} âm tiết; thời lượng ước tính khoảng {mins:.0f} phút '
  f'(tốc độ đọc tiếng Việt của giọng Algieba đo được ở các video trước: khoảng {rates} âm tiết/giây).')
doc.add_heading('Quy ước dịch',1)
for t in ['Văn phong thuyết minh phim tài liệu, câu ngắn, dễ nghe; nội dung và số liệu giữ đúng bản tiếng Anh, không thêm ý mới.',
          'Số viết theo kiểu Việt Nam (5.400; 4,6 tỷ; 8.848,86 mét). Đơn vị viết đủ chữ (ki-lô-mét, xăng-ti-mét) để giọng đọc phát âm đúng.',
          'Tên riêng nước ngoài giữ nguyên (Everest, Eyjafjallajökull, Pompeii); tên đã có cách gọi quen thuộc thì dùng tiếng Việt (sông Nin, Tứ Xuyên, Thổ Nhĩ Kỳ, hang Sơn Đoòng).',
          'Tiêu đề cảnh và tên chương (hiện trên hình) cũng được dịch; chữ tiếng Việt dùng font Patrick Hand vì font Caveat của bản tiếng Anh không có dấu tiếng Việt.',
          f'Tiêu đề video đề xuất: "{VIDEO_TITLE_VI}". Tiêu đề trang mục lục: "{TOC_TITLE_VI}".']:
    doc.add_paragraph(t,style='List Bullet')
doc.add_heading('Tên chương',1)
t=doc.add_table(rows=1,cols=3); t.style='Light Grid Accent 1'
for c,h in zip(t.rows[0].cells,['Chương','Tiếng Anh','Tiếng Việt']): c.text=h
for n,name in d['chapters']:
    r=t.add_row().cells; r[0].text=n; r[1].text=name; r[2].text=CH_VI[n]
groups=[('0','Mở đầu: trang mục lục (sau cảnh 1.1)')]+[(n,f'Chương {n}: {CH_VI[n]} ({name})') for n,name in d['chapters']]
for n,head in groups:
    doc.add_page_break(); doc.add_heading(head,1)
    t=doc.add_table(rows=1,cols=3); t.style='Table Grid'
    for c,h in zip(t.rows[0].cells,['Cảnh / tranh','Tiếng Anh (bản rút gọn)','Tiếng Việt (đề xuất)']):
        c.text=h; shade(c,'D9E2F3'); c.paragraphs[0].runs[0].bold=True
    for s in [s for s in sc if s['code'].split('.')[0]==n]:
        title,text=VI[s['code']]; r=t.add_row().cells
        p=r[0].paragraphs[0]; a=p.add_run(s['code']+'  '); a.bold=True; p.add_run(title)
        g=r[0].add_paragraph(s['file']).runs[0]; g.font.color.rgb=RGBColor(0x80,0x80,0x80)
        run=r[1].paragraphs[0].add_run(s['narration']); run.font.size=Pt(9); run.font.color.rgb=RGBColor(0x70,0x70,0x70)
        r[2].paragraphs[0].add_run(text).font.size=Pt(10.5); shade(r[2],'F4F9EE')
    for row in t.rows:
        for c,w in zip(row.cells,(Cm(5.2),Cm(10.6),Cm(10.6))): c.width=w
doc.save('kich-ban-tieng-viet.docx'); print(tot, round(mins,1))
