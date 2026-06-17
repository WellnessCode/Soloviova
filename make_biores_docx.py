"""Generate compliant bioresonance wellness report template (Wellness Code style)."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PURPLE_HEX   = '7B52AB'
LAVENDER_HEX = 'EEE8F8'
GREEN_HEX    = '52AB7B'
L_GREEN_HEX  = 'E8F8EE'
ORANGE_HEX   = 'F0811E'
GRAY_HEX     = 'F5F5F5'

PURPLE_RGB  = RGBColor(123, 82,  171)
GREEN_RGB   = RGBColor(82,  171, 123)
ORANGE_RGB  = RGBColor(240, 129, 30)
WHITE_RGB   = RGBColor(255, 255, 255)
BLACK_RGB   = RGBColor(30,  30,  30)
GRAY_RGB    = RGBColor(100, 100, 100)
RED_RGB     = RGBColor(180, 40,  40)
FONT        = 'Calibri'


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


def thin_borders(tbl, color='D4C8F0'):
    tblPr = get_or_add_tblPr(tbl._tbl)
    tb = OxmlElement('w:tblBorders')
    for s in ('top','left','bottom','right','insideH','insideV'):
        b = OxmlElement(f'w:{s}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), '4')
        b.set(qn('w:color'), color)
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


def run(para, text, bold=False, color=None, size=10.5):
    r = para.add_run(text)
    r.bold = bold
    r.font.name = FONT
    r.font.size = Pt(size)
    r.font.color.rgb = color or BLACK_RGB
    return r


def section_header(doc, text, bg_hex=PURPLE_HEX):
    tbl = doc.add_table(rows=1, cols=1)
    no_borders(tbl)
    cell = tbl.cell(0, 0)
    shd(cell, bg_hex)
    cell_margins(cell, top=100, bottom=100, left=160, right=160)
    p = cell.paragraphs[0]
    spacing(p)
    run(p, text, bold=True, color=WHITE_RGB, size=11)
    sp = doc.add_paragraph()
    spacing(sp, before=0, after=40)


def disclaimer_box(doc):
    tbl = doc.add_table(rows=1, cols=1)
    no_borders(tbl)
    cell = tbl.cell(0, 0)
    shd(cell, 'FFF3CD')
    cell_margins(cell, top=100, bottom=100, left=160, right=160)

    # left border simulation via another nested table
    p = cell.paragraphs[0]
    spacing(p)
    run(p, '⚠  ВАЖЛИВО: ', bold=True, color=RGBColor(160, 100, 0), size=10)
    run(p, 'Цей документ є звітом функціонального біорезонансного аналізу і '
           'НЕ є медичним діагнозом. Він не замінює консультацію лікаря та не '
           'може використовуватися для самолікування. Для встановлення діагнозу '
           'зверніться до авторизованого медичного спеціаліста.',
        color=RGBColor(120, 80, 0), size=10)
    sp = doc.add_paragraph()
    spacing(sp, before=0, after=80)


def bullet_row(doc, text, color=PURPLE_RGB):
    p = doc.add_paragraph()
    spacing(p, before=0, after=30)
    run(p, '●  ', bold=True, color=color, size=10.5)
    run(p, text, size=10.5)


def two_col_table(doc, h1, h2, rows_data, c1=5.5, c2=11.0,
                  hdr_hex=PURPLE_HEX, alt_hex=LAVENDER_HEX, border_color='D4C8F0'):
    tbl = doc.add_table(rows=1+len(rows_data), cols=2)
    thin_borders(tbl, border_color)
    tbl.columns[0].width = Cm(c1)
    tbl.columns[1].width = Cm(c2)

    h0, h1c = tbl.cell(0,0), tbl.cell(0,1)
    shd(h0, hdr_hex); shd(h1c, hdr_hex)
    cell_margins(h0); cell_margins(h1c)
    p = h0.paragraphs[0]; spacing(p)
    run(p, h1, bold=True, color=WHITE_RGB)
    p = h1c.paragraphs[0]; spacing(p)
    run(p, h2, bold=True, color=WHITE_RGB)

    for i, (label, value) in enumerate(rows_data):
        bg = alt_hex if i % 2 == 0 else 'FFFFFF'
        c0, c1_ = tbl.cell(i+1, 0), tbl.cell(i+1, 1)
        shd(c0, bg); shd(c1_, bg)
        cell_margins(c0); cell_margins(c1_)
        p0 = c0.paragraphs[0]; spacing(p0)
        lbl_color = PURPLE_RGB if hdr_hex == PURPLE_HEX else GREEN_RGB
        run(p0, label, bold=True, color=lbl_color)
        p1 = c1_.paragraphs[0]; spacing(p1)
        run(p1, value)

    sp = doc.add_paragraph()
    spacing(sp, before=0, after=80)


# ── BUILD ──────────────────────────────────────────────────────────────────────
doc = Document()
for section in doc.sections:
    section.top_margin    = Cm(1.5)
    section.bottom_margin = Cm(1.5)
    section.left_margin   = Cm(2.0)
    section.right_margin  = Cm(2.0)

# ── Title block ────────────────────────────────────────────────────────────────
logo_p = doc.add_paragraph()
spacing(logo_p, before=0, after=0)
logo_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
run(logo_p, 'WELLNESS CODE by Anna Soloviova', bold=True, color=PURPLE_RGB, size=9)

line_tbl = doc.add_table(rows=1, cols=1)
no_borders(line_tbl)
shd(line_tbl.cell(0,0), PURPLE_HEX)
cell_margins(line_tbl.cell(0,0), top=10, bottom=10)
sp0 = doc.add_paragraph(); spacing(sp0, before=0, after=60)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
spacing(p, before=0, after=40)
run(p, 'ЗВІТ ФУНКЦІОНАЛЬНОГО БІОРЕЗОНАНСНОГО АНАЛІЗУ', bold=True, color=PURPLE_RGB, size=15)

p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
spacing(p2, before=0, after=20)
run(p2, 'Wellness-оцінка стану функціональних систем організму', color=GRAY_RGB, size=10.5)

p3 = doc.add_paragraph()
p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
spacing(p3, before=0, after=120)
run(p3, '[ПІБ клієнта]', bold=True, color=ORANGE_RGB, size=12)

# ── Disclaimer ─────────────────────────────────────────────────────────────────
disclaimer_box(doc)

# ══════════════════════════════════════════════════════════════════════════════
# 1. НЕРВОВА СИСТЕМА
# ══════════════════════════════════════════════════════════════════════════════
section_header(doc, '1. НЕРВОВА СИСТЕМА', PURPLE_HEX)
bullet_row(doc, 'Функціональні зміни в зоні стовбура головного мозку справа, '
                'що можуть бути пов\'язані з особливостями емоційно-поведінкової регуляції')
bullet_row(doc, 'Показники підвищеної реактивності нервової системи')
doc.add_paragraph();

# ══════════════════════════════════════════════════════════════════════════════
# 2. ОПОРНО-РУХОВИЙ АПАРАТ
# ══════════════════════════════════════════════════════════════════════════════
section_header(doc, '2. ОПОРНО-РУХОВИЙ АПАРАТ', PURPLE_HEX)
bullet_row(doc, 'Функціональні зміни в зоні атланто-аксіального з\'єднання С1–С2, '
                'що можуть впливати на кровопостачання мозку, координацію, слух, зір '
                'та чутливість верхніх кінцівок')
bullet_row(doc, 'Показники функціональних змін у грудному та крижовому відділах '
                'хребта (потребують додаткового обстеження)')
bullet_row(doc, 'Показники зниженого тонусу м\'язів нижніх кінцівок')
bullet_row(doc, 'Функціональні зміни в зоні сухожилля та капсули плечового суглоба')
bullet_row(doc, 'Функціональні зміни в зоні дрібних суглобів нижніх кінцівок')
bullet_row(doc, 'Показники порушення положення та рухливості діафрагми')
bullet_row(doc, 'Функціональні зміни склепіння стопи (плоскостопість)')
bullet_row(doc, 'Показники зниження щільності кісткової тканини (потребують підтвердження денситометрією)')
doc.add_paragraph()

# ══════════════════════════════════════════════════════════════════════════════
# 3. СЕРЦЕВО-СУДИННА СИСТЕМА
# ══════════════════════════════════════════════════════════════════════════════
section_header(doc, '3. СЕРЦЕВО-СУДИННА СИСТЕМА', PURPLE_HEX)
bullet_row(doc, 'Показники підвищеного навантаження на судинну стінку, характерні для '
                'порушення ліпідного обміну')
bullet_row(doc, 'Показники реактивного ліпідного дисбалансу, пов\'язаного зі стресовою реакцією')
bullet_row(doc, 'Функціональні зміни в зоні венозного кровотоку нижніх кінцівок '
                '(рання стадія)')
doc.add_paragraph()

# ══════════════════════════════════════════════════════════════════════════════
# 4. ТРАВНА СИСТЕМА
# ══════════════════════════════════════════════════════════════════════════════
section_header(doc, '4. ТРАВНА СИСТЕМА', PURPLE_HEX)
bullet_row(doc, 'Функціональні зміни в зоні жовчного міхура зі схильністю до '
                'застою жовчі та порушення жовчовиділення за гіпокінетичним типом')
bullet_row(doc, 'Функціональні зміни в зоні підшлункової залози')
bullet_row(doc, 'Показники підвищеного газоутворення в кишківнику')
doc.add_paragraph()

# ══════════════════════════════════════════════════════════════════════════════
# 5. ЕНДОКРИННА СИСТЕМА
# ══════════════════════════════════════════════════════════════════════════════
section_header(doc, '5. ЕНДОКРИННА СИСТЕМА', PURPLE_HEX)
bullet_row(doc, 'Показники зниженої функціональної активності щитоподібної залози')
bullet_row(doc, 'Показники змін функціональної активності прищитоподібних залоз')
bullet_row(doc, 'Показники дисбалансу секреції статевих гормонів')
bullet_row(doc, 'Показники схильності до підвищеної імунної реактивності')
bullet_row(doc, 'Показники підвищеної активності симпато-адреналової системи')
doc.add_paragraph()

# ══════════════════════════════════════════════════════════════════════════════
# 6. СЕЧОСТАТЕВА СИСТЕМА
# ══════════════════════════════════════════════════════════════════════════════
section_header(doc, '6. СЕЧОСТАТЕВА СИСТЕМА', PURPLE_HEX)
bullet_row(doc, 'Показники підвищеної чутливості сечового міхура')
bullet_row(doc, 'Функціональні зміни в зоні передміхурової залози '
                '(доброякісне розростання тканини — потребує підтвердження у уролога)')
doc.add_paragraph()

# ══════════════════════════════════════════════════════════════════════════════
# 7. ОРГАНИ ЗОРУ
# ══════════════════════════════════════════════════════════════════════════════
section_header(doc, '7. ОРГАНИ ЗОРУ', PURPLE_HEX)
bullet_row(doc, 'Функціональні зміни в зоні судин сітківки лівого ока')
bullet_row(doc, 'Показники змін центрального зору зі схильністю до помутніння '
                'кришталика правого ока')
doc.add_paragraph()

# ══════════════════════════════════════════════════════════════════════════════
# 8. ЛОР / ПОРОЖНИНА РОТА
# ══════════════════════════════════════════════════════════════════════════════
section_header(doc, '8. ЛОР / ПОРОЖНИНА РОТА', PURPLE_HEX)
bullet_row(doc, 'Функціональні зміни в зоні носової перегородки, що можуть '
                'ускладнювати носове дихання')
bullet_row(doc, 'Показники хронічного запального процесу в зоні придаткових пазух носа')
bullet_row(doc, 'Показники хронічного запального процесу в зоні мигдаликів')
bullet_row(doc, 'Показники зниженого тонусу м\'якого піднебіння (може впливати '
                'на якість сну)')
bullet_row(doc, 'Показники запального процесу в зоні ясен')
doc.add_paragraph()

# ══════════════════════════════════════════════════════════════════════════════
# 9. ІМУННА СИСТЕМА ТА ІНФЕКЦІЙНЕ НАВАНТАЖЕННЯ
# ══════════════════════════════════════════════════════════════════════════════
section_header(doc, '9. ІМУННА СИСТЕМА ТА ІНФЕКЦІЙНЕ НАВАНТАЖЕННЯ', PURPLE_HEX)
bullet_row(doc, 'Показники мікотичного (грибкового) дисбалансу в зоні уретри, '
                'зовнішнього та середнього вуха')
bullet_row(doc, 'Показники активності герпесвірусу 1-го, 2-го, 7-го типу')
bullet_row(doc, 'Перенесена вірусна інфекція COVID у попередні 3 місяці — '
                'постковідне навантаження на імунну систему')
bullet_row(doc, 'Показники підвищеного паразитарного навантаження')
doc.add_paragraph()

# ══════════════════════════════════════════════════════════════════════════════
# 10. ДЕФІЦИТИ ПОЖИВНИХ РЕЧОВИН
# ══════════════════════════════════════════════════════════════════════════════
section_header(doc, '10. ДЕФІЦИТИ ПОЖИВНИХ РЕЧОВИН', GREEN_HEX)
bullet_row(doc, 'Показники дефіциту вітамінів А, D, групи В', GREEN_RGB)
bullet_row(doc, 'Показники дефіциту мінералів', GREEN_RGB)
bullet_row(doc, 'Показники дефіциту цинку', GREEN_RGB)
bullet_row(doc, 'Показники дефіциту амінокислот: аргінін, гліцин, аспарагінова '
                'кислота, таурин, орнітин, диметилгліцин, глутатіон, валін, метіонін',
           GREEN_RGB)
bullet_row(doc, 'Показники підвищеного мікотоксинового навантаження', GREEN_RGB)
doc.add_paragraph()

# ══════════════════════════════════════════════════════════════════════════════
# 11. ХАРЧОВА ТА ХІМІЧНА ЧУТЛИВІСТЬ
# ══════════════════════════════════════════════════════════════════════════════
section_header(doc, '11. ХАРЧОВА ТА ХІМІЧНА ЧУТЛИВІСТЬ', GREEN_HEX)
bullet_row(doc, 'Показники підвищеної чутливості організму до: бобових, цукру, '
                'рису, продуктів, що містять глютен (пшениця, жито, вівсянка), '
                'жирних сортів риби',
           GREEN_RGB)
bullet_row(doc, 'Показники підвищеної чутливості до летких речовин: парфумерія, '
                'вихлопні гази та інші хімічні подразники',
           GREEN_RGB)
doc.add_paragraph()

# ══════════════════════════════════════════════════════════════════════════════
# ЗАВЕРШАЛЬНЕ СЛОВО
# ══════════════════════════════════════════════════════════════════════════════
section_header(doc, 'ВІТАЄМО З ПОЧАТКОМ ПРОГРАМИ!', PURPLE_HEX)

p = doc.add_paragraph()
spacing(p, before=60, after=40)
run(p, 'Дякую за довіру.', bold=True, color=PURPLE_RGB, size=11)

closing = [
    'Я рада вітати Вас на Вашій програмі корекції ваги та здоров\'я.',
    'Моя мета — допомогти Вам впоратися з Вашою проблемою і навчитися '
    'усвідомлено керувати своїм здоров\'ям.',
    'З турботою та вірою у Вас,',
]
for line in closing:
    p = doc.add_paragraph()
    spacing(p, before=0, after=30)
    run(p, line, size=10.5)

p = doc.add_paragraph()
spacing(p, before=40, after=120)
run(p, 'Health-coach Anna Soloviova та команда проєкту WELLNESS CODE by Anna Soloviova',
    bold=True, color=PURPLE_RGB, size=10.5)

# Footer
sp_p = doc.add_paragraph(); spacing(sp_p, before=120, after=0)
tbl = doc.add_table(rows=1, cols=2)
no_borders(tbl)
tbl.columns[0].width = Cm(8)
tbl.columns[1].width = Cm(8.5)
cell_margins(tbl.cell(0,0)); cell_margins(tbl.cell(0,1))
p0 = tbl.cell(0,0).paragraphs[0]
run(p0, 'Дата складання: ________________', color=GRAY_RGB, size=9)
p1 = tbl.cell(0,1).paragraphs[0]
p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
run(p1, 'Health-coach: ________________', color=GRAY_RGB, size=9)

OUT = '/home/user/Soloviova/Шаблон_Біорезонанс_WellnessCode.docx'
doc.save(OUT)
print(f'Saved: {OUT}')
