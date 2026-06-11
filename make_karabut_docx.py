"""Generate Karabut Oleksandra patient extract in Smolych/Wellness Code format."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PURPLE_HEX = '7B52AB'
PURPLE_RGB = RGBColor(123, 82, 171)
ORANGE_RGB = RGBColor(240, 129, 30)
WHITE_RGB = RGBColor(255, 255, 255)
BLACK_RGB = RGBColor(30, 30, 30)
GRAY_RGB = RGBColor(100, 100, 100)
FONT = 'Calibri'


def shd(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    e = OxmlElement('w:shd')
    e.set(qn('w:val'), 'clear')
    e.set(qn('w:color'), 'auto')
    e.set(qn('w:fill'), hex_color)
    tcPr.append(e)

def get_or_add_tblPr(tbl_elem):
    tblPr = tbl_elem.find(qn('w:tblPr'))
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl_elem.insert(0, tblPr)
    return tblPr

def no_borders(tbl):
    tblPr = get_or_add_tblPr(tbl._tbl)
    tb = OxmlElement('w:tblBorders')
    for s in ('top','left','bottom','right','insideH','insideV'):
        b = OxmlElement(f'w:{s}')
        b.set(qn('w:val'), 'none')
        tb.append(b)
    tblPr.append(tb)

def thin_borders(tbl):
    tblPr = get_or_add_tblPr(tbl._tbl)
    tb = OxmlElement('w:tblBorders')
    for s in ('top','left','bottom','right','insideH','insideV'):
        b = OxmlElement(f'w:{s}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), '4')
        b.set(qn('w:color'), 'D4C8F0')
        tb.append(b)
    tblPr.append(tb)

def cell_margins(cell, top=60, bottom=60, left=120, right=120):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    mar = OxmlElement('w:tcMar')
    for name, val in [('top',top),('bottom',bottom),('left',left),('right',right)]:
        e = OxmlElement(f'w:{name}')
        e.set(qn('w:w'), str(val))
        e.set(qn('w:type'), 'dxa')
        mar.append(e)
    tcPr.append(mar)

def spacing(para, before=0, after=0):
    pPr = para._p.get_or_add_pPr()
    sp = OxmlElement('w:spacing')
    sp.set(qn('w:before'), str(before))
    sp.set(qn('w:after'), str(after))
    pPr.append(sp)

def run(para, text, bold=False, italic=False, color=None, size=10.5):
    r = para.add_run(text)
    r.bold = bold
    r.italic = italic
    r.font.name = FONT
    r.font.size = Pt(size)
    r.font.color.rgb = color or BLACK_RGB
    return r

def section_header(doc, text):
    tbl = doc.add_table(rows=1, cols=1)
    no_borders(tbl)
    cell = tbl.cell(0, 0)
    shd(cell, PURPLE_HEX)
    cell_margins(cell, top=100, bottom=100, left=160, right=160)
    p = cell.paragraphs[0]
    spacing(p)
    run(p, text, bold=True, color=WHITE_RGB, size=11.5)
    sp = doc.add_paragraph()
    spacing(sp, before=0, after=40)

def two_col_table(doc, col1_header, col2_header, rows_data, col1_w=5.5, col2_w=11.0, warn_rows=None):
    tbl = doc.add_table(rows=1+len(rows_data), cols=2)
    thin_borders(tbl)
    tbl.columns[0].width = Cm(col1_w)
    tbl.columns[1].width = Cm(col2_w)
    h0, h1 = tbl.cell(0,0), tbl.cell(0,1)
    shd(h0, PURPLE_HEX); shd(h1, PURPLE_HEX)
    cell_margins(h0); cell_margins(h1)
    p = h0.paragraphs[0]; spacing(p)
    run(p, col1_header, bold=True, color=WHITE_RGB)
    p = h1.paragraphs[0]; spacing(p)
    run(p, col2_header, bold=True, color=WHITE_RGB)
    warn_rows = warn_rows or []
    for i, (label, value) in enumerate(rows_data):
        c0 = tbl.cell(i+1, 0); c1 = tbl.cell(i+1, 1)
        bg = 'EEE8F8' if i % 2 == 0 else 'FFFFFF'
        shd(c0, bg); shd(c1, bg)
        cell_margins(c0); cell_margins(c1)
        p0 = c0.paragraphs[0]; spacing(p0)
        run(p0, label, bold=True, color=PURPLE_RGB)
        p1 = c1.paragraphs[0]; spacing(p1)
        val_color = ORANGE_RGB if i in warn_rows else BLACK_RGB
        run(p1, value, bold=(i in warn_rows), color=val_color)
    sp = doc.add_paragraph()
    spacing(sp, before=0, after=80)


doc = Document()
for section in doc.sections:
    section.top_margin = Cm(1.5)
    section.bottom_margin = Cm(1.5)
    section.left_margin = Cm(2.0)
    section.right_margin = Cm(2.0)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
spacing(p, before=0, after=60)
run(p, 'ВИТЯГ З АНКЕТИ ПАЦІЄНТА', bold=True, color=PURPLE_RGB, size=16)

p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
spacing(p2, before=0, after=40)
run(p2, 'Скарги та порушення здоров\'я', italic=True, color=GRAY_RGB, size=11)

p3 = doc.add_paragraph()
p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
spacing(p3, before=0, after=160)
run(p3, 'Карабут Олександра', bold=True, color=ORANGE_RGB, size=13)

# 1. КОНТАКТНІ ДАНІ
section_header(doc, '1. КОНТАКТНІ ДАНІ')
two_col_table(doc, 'Поле', 'Дані', [
    ('ПІБ', 'Карабут Олександра'),
    ('Дата народження', '30.06.1983 (41 рік)'),
    ('Телефон', '+491734293675'),
    ('Email', 'aleksa833006@gmail.com'),
    ('Місце проживання', 'Німеччина'),
    ('Рід занять', 'Велнес масаж'),
    ('Подорожі', 'Нідерланди, Польща (2025, 2026)'),
])

# 2. АНТРОПОМЕТРИЧНІ ПОКАЗНИКИ
section_header(doc, '2. АНТРОПОМЕТРИЧНІ ПОКАЗНИКИ')
two_col_table(doc, 'Показник', 'Значення', [
    ('Зріст', '160 см'),
    ('Вага', '69 кг  ⚠️ (бажане зниження ~10 кг, цільова ~59 кг)'),
    ('Об\'єм талії', 'Не виміряно'),
    ('Об\'єм живота', 'Не виміряно'),
    ('Об\'єм грудей', 'Не виміряно'),
    ('Об\'єм стегон', 'Не виміряно'),
], warn_rows=[1])

# 3. ОСНОВНІ СКАРГИ
section_header(doc, '3. ОСНОВНІ СКАРГИ')
two_col_table(doc, 'Система / Орган', 'Скарга / Порушення', [
    ('Психоемоційний стан', 'Психічний розлад — не відчуває тіла, немає енергії, не в гармонії з собою (80% причина звернення) ⚠️. Відчуття пустоти, соціальна тривога після переїзду. Тривога постійно, незалежно від приводу'),
    ('Набряки', 'Набряки всього тіла — дуже часто ⚠️'),
    ('Травна система', 'Підвищена кислотність шлунку. Відрижка майже постійно ⚠️. Здуття живота — постійно ⚠️. Печія — іноді'),
    ('Серцево-судинна', 'Варикоз на ногах. Задишка при навантаженні — трохи. Тиск 120/80 (норма)'),
    ('Опорно-рухова', 'Сколіоз. Рідко — болі в суглобах пальців рук'),
    ('Статева система', 'Менструальний цикл болісний, постійно приймає знеболюючі ⚠️. В анамнезі — ерозія матки (УЗД 2024 — норма)'),
    ('Нирки', 'Пієлонефрит під час вагітності (в нормі зараз)'),
    ('COVID-19', 'Перехворіла у 2019 р. — дуже тяжко: проблеми з диханням, тривале відновлення ⚠️'),
    ('Сон', 'Прокидається не завжди відпочившою. Іноді важко прокидатись. Підйом 5:30–9:00, відбій ~22:00'),
], warn_rows=[0, 1, 2, 5, 7])

# 4. ОБТЯЖЕНИЙ СІМЕЙНИЙ АНАМНЕЗ
section_header(doc, '4. ОБТЯЖЕНИЙ СІМЕЙНИЙ АНАМНЕЗ')
two_col_table(doc, 'Родич', 'Захворювання', [
    ('Батько', 'Помер від інфаркту міокарда ⚠️'),
    ('Мама', 'Запалення суглобів, захворювання щитоподібної залози'),
    ('Бабуся', 'Рак молочної залози ⚠️'),
    ('Сестра 1', 'Захворювання щитоподібної залози'),
    ('Сестра 2', 'Кісти жіночих органів'),
], col1_w=6.0, col2_w=10.5, warn_rows=[0, 2])

# 5. ОПЕРАТИВНІ ВТРУЧАННЯ В АНАМНЕЗІ
section_header(doc, '5. ОПЕРАТИВНІ ВТРУЧАННЯ В АНАМНЕЗІ')
two_col_table(doc, 'Рік', 'Операція / Процедура', [
    ('Травм і операцій', 'Не було'),
    ('Косметологія', 'Уколи в губи (філери)'),
    ('Пологи', 'Двоє дітей, природні. Останні — 2009 р.'),
], col1_w=4.0, col2_w=12.5)

# 6. ПОТОЧНА ТЕРАПІЯ / БАДи
section_header(doc, '6. ПОТОЧНА ТЕРАПІЯ / БАДи')
two_col_table(doc, 'Препарат', 'Призначення', [
    ('Магній', 'Підтримка нервової системи'),
    ('Вітамін D3', 'Профілактика'),
    ('Омега-3', 'Серцево-судинна система'),
    ('Вітамін B12', 'Енергія, нервова система'),
])

# 7. ХАРЧОВІ ЗВИЧКИ ТА ПОРУШЕННЯ
section_header(doc, '7. ХАРЧОВІ ЗВИЧКИ ТА ПОРУШЕННЯ')
two_col_table(doc, 'Показник', 'Дані', [
    ('Кількість прийомів їжі', '3–4 рази на день'),
    ('Основна їжа', 'М\'ясо, риба, яйця, хліб з маслом, овочі, фрукти'),
    ('Сніданок (7:00–8:00)', 'Вівсянка, кава з сиром, кефір з насінням чіа, бутерброд'),
    ('Обід', 'Гарнір з м\'ясом, яйця, риба, овочі'),
    ('Вечеря (19:00–20:00)', 'Гарнір з м\'ясом/рибою або перші страви'),
    ('Перекуси', 'Горіхи, банани, морозиво, фрукти'),
    ('Порція', '200–250 г'),
    ('Більше їсть', 'Ввечері ⚠️'),
    ('Вода на день', '1000–1500 мл'),
    ('Кава', 'Натуральна, ~3 чашки/день'),
    ('Спорт', 'Біг, велосипед, розтяжки, спортзал, плавання, сауна'),
    ('Солодке', '5/10'),
    ('Борошняне', '7/10 ⚠️'),
    ('Алкоголь', '2–3 рази/місяць — біле або червоне сухе вино, 1–2 бокали'),
    ('Паління', 'Ні'),
], warn_rows=[7, 12])

# Footer
sp = doc.add_paragraph()
spacing(sp, before=200, after=0)
tbl = doc.add_table(rows=1, cols=2)
no_borders(tbl)
tbl.columns[0].width = Cm(8)
tbl.columns[1].width = Cm(8.5)
cell_margins(tbl.cell(0,0)); cell_margins(tbl.cell(0,1))
p0 = tbl.cell(0,0).paragraphs[0]
run(p0, 'Дата складання витягу: ________________', color=GRAY_RGB, size=9.5)
p1 = tbl.cell(0,1).paragraphs[0]
p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
run(p1, 'Лікар: ________________', color=GRAY_RGB, size=9.5)

OUT = '/home/user/Soloviova/Карабут_Олександра_Витяг.docx'
doc.save(OUT)
print(f'Saved: {OUT}')
