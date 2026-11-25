import json
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from short_narration import SHORT
RATE=2.48; GAP=0.7; CHGAP=1.8
d=json.load(open('scenes.json')); chap=dict(d['chapters'])
doc=Document()
sec=doc.sections[0]; sec.orientation=WD_ORIENT.LANDSCAPE
sec.page_width,sec.page_height=Cm(29.7),Cm(21)
for m in ('left_margin','right_margin','top_margin','bottom_margin'): setattr(sec,m,Cm(1.6))
st=doc.styles['Normal']; st.font.name='Arial'; st.font.size=Pt(10)
st.element.rPr.rFonts.set(qn('w:eastAsia'),'Arial')
def shade(cell,hexc):
    tcPr=cell._tc.get_or_add_tcPr(); s=OxmlElement('w:shd'); s.set(qn('w:val'),'clear'); s.set(qn('w:fill'),hexc); tcPr.append(s)
def mins(words,n,nch): return (words/RATE+n*GAP+nch*CHGAP)/60
sc=d['scenes']
ow=sum(len(s['narration'].split()) for s in sc); nw=sum(len(SHORT[s['code']].split()) for s in sc)
doc.add_heading('Wonders of Planet Earth: kịch bản rút gọn (bản đề xuất)',0)
doc.add_paragraph(f'Giữ nguyên 122 cảnh và 122 tranh đã tạo, giữ thứ tự 17 chương. Lời dẫn tiếng Anh giảm từ {ow:,} từ xuống {nw:,} từ ({nw/ow:.0%}). '
 f'Thời lượng ước tính theo tốc độ đọc thực tế của giọng Algieba ({RATE} từ/giây): khoảng {mins(nw,122,17):.0f} phút, so với khoảng {mins(ow,122,17):.0f} phút của bản hiện tại.')
doc.add_heading('Nguyên tắc rút gọn',1)
for t in ['Mỗi câu dẫn vẫn mô tả đúng nội dung tranh của cảnh đó, để hình và lời khớp nhau.',
          'Giữ một hoặc hai ý chính và con số nổi bật nhất của mỗi cảnh; bỏ các chi tiết phụ (ví dụ danh sách đầy đủ các mảng kiến tạo, độ cao từng trại trên Everest, chi tiết thảm họa phụ).',
          'Câu ngắn, dễ nghe, hợp phụ đề một dòng. Mỗi tranh hiện khoảng 9–12 giây thay vì 18–30 giây.',
          'Không thêm sự kiện hay số liệu mới ngoài kịch bản gốc.',
          'Cột "Bản gốc" để anh đối chiếu; chỉ cột "Bản rút gọn" sẽ được đọc.']:
    doc.add_paragraph(t,style='List Bullet')
doc.add_heading('Tóm tắt theo chương',1)
t=doc.add_table(rows=1,cols=5); t.style='Light Grid Accent 1'
for c,h in zip(t.rows[0].cells,['Chương','Số cảnh','Từ (gốc → rút gọn)','Phút (gốc → rút gọn)','Giảm']): c.text=h
for n,name in d['chapters']:
    ss=[s for s in sc if s['code'].split('.')[0]==n]
    o=sum(len(s['narration'].split()) for s in ss); w=sum(len(SHORT[s['code']].split()) for s in ss)
    r=t.add_row().cells; r[0].text=f'{n}. {name}'; r[1].text=str(len(ss)); r[2].text=f'{o} → {w}'
    r[3].text=f'{mins(o,len(ss),1):.1f} → {mins(w,len(ss),1):.1f}'; r[4].text=f'{1-w/o:.0%}'
r=t.add_row().cells; r[0].text='Tổng'; r[1].text='122'; r[2].text=f'{ow:,} → {nw:,}'; r[3].text=f'{mins(ow,122,17):.0f} → {mins(nw,122,17):.0f}'; r[4].text=f'{1-nw/ow:.0%}'
for c in r:
    for p in c.paragraphs:
        for run in p.runs: run.bold=True
for n,name in d['chapters']:
    doc.add_page_break(); doc.add_heading(f'Chương {n}: {name}',1)
    t=doc.add_table(rows=1,cols=3); t.style='Table Grid'
    for c,h in zip(t.rows[0].cells,['Cảnh / tranh','Bản gốc','Bản rút gọn (đề xuất)']):
        c.text=h; shade(c,'D9E2F3'); c.paragraphs[0].runs[0].bold=True
    for s in [s for s in sc if s['code'].split('.')[0]==n]:
        r=t.add_row().cells
        p=r[0].paragraphs[0]; a=p.add_run(s['code']+'  '); a.bold=True; p.add_run(s['title'])
        r[0].add_paragraph(s['file']).runs[0].font.color.rgb=RGBColor(0x80,0x80,0x80)
        o=len(s['narration'].split()); w=len(SHORT[s['code']].split())
        r[0].add_paragraph(f'{o} → {w} từ').runs[0].font.color.rgb=RGBColor(0x80,0x80,0x80)
        run=r[1].paragraphs[0].add_run(s['narration']); run.font.size=Pt(8.5); run.font.color.rgb=RGBColor(0x70,0x70,0x70)
        r[2].paragraphs[0].add_run(SHORT[s['code']]).font.size=Pt(10.5); shade(r[2],'F4F9EE')
    for row in t.rows:
        for c,wd in zip(row.cells,(Cm(5),Cm(10.8),Cm(10.6))): c.width=wd
doc.save('kich-ban-rut-gon.docx')
print(ow,nw,round(mins(ow,122,17),1),round(mins(nw,122,17),1))
