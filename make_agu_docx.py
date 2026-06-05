"""Generate Agu Iryna wellness program in Barvysh (Wellness Code) format."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── Palette ──────────────────────────────────────────────────────────────────
PURPLE_HEX   = '7B52AB'
PURPLE_LIGHT = 'D4C8F0'
LAVENDER_HEX = 'EEE8F8'
PURPLE_RGB   = RGBColor(123, 82, 171)
ORANGE_RGB   = RGBColor(240, 129, 30)
GRAY_RGB     = RGBColor(120, 120, 120)
WHITE_RGB    = RGBColor(255, 255, 255)
BLACK_RGB    = RGBColor(30,  30,  30)

FONT = 'Calibri'


# ── XML helpers ───────────────────────────────────────────────────────────────
def shd(cell, hex_color):
    tc  = cell._tc
    tcPr = tc.get_or_add_tcPr()
    e = OxmlElement('w:shd')
    e.set(qn('w:val'),   'clear')
    e.set(qn('w:color'), 'auto')
    e.set(qn('w:fill'),  hex_color)
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


def cell_margins(cell, val=80):
    tcPr = cell._tc.get_or_add_tcPr()
    m = OxmlElement('w:tcMar')
    for s in ('top','bottom','left','right'):
        e = OxmlElement(f'w:{s}')
        e.set(qn('w:w'),    str(val))
        e.set(qn('w:type'), 'dxa')
        m.append(e)
    tcPr.append(m)


def spacing(para, before=0, after=0):
    pPr = para._p.get_or_add_pPr()
    sp = OxmlElement('w:spacing')
    sp.set(qn('w:before'), str(before))
    sp.set(qn('w:after'),  str(after))
    pPr.append(sp)


def add_run(para, text, bold=False, italic=False, size=10.5,
            color=None, font=FONT):
    r = para.add_run(text)
    r.bold        = bold
    r.italic      = italic
    r.font.size   = Pt(size)
    r.font.name   = font
    r.font.color.rgb = color or BLACK_RGB
    return r


def para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, before=0, after=60):
    p = doc.add_paragraph()
    p.alignment = align
    spacing(p, before, after)
    return p


# ── Running header / footer ───────────────────────────────────────────────────
def set_header_footer(section, patient_name):
    # Header
    hdr = section.header
    hdr.is_linked_to_previous = False
    hp = hdr.paragraphs[0]
    hp.clear()
    spacing(hp, 0, 40)
    add_run(hp, f'WELLNESS CODE by Anna Soloviova  |  Програма корекції — {patient_name}',
            size=8, color=GRAY_RGB)
    # Rule under header
    pPr = hp._p.get_or_add_pPr()
    pb = OxmlElement('w:pBdr')
    bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'),   'single')
    bot.set(qn('w:sz'),    '4')
    bot.set(qn('w:space'), '1')
    bot.set(qn('w:color'), 'AAAAAA')
    pb.append(bot)
    pPr.append(pb)

    # Footer
    ftr = section.footer
    ftr.is_linked_to_previous = False
    fp = ftr.paragraphs[0]
    fp.clear()
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    spacing(fp, 20, 0)
    add_run(fp,
            'wellness-code.com  |  Конфіденційна медична інформація  |  © WELLNESS CODE by Anna Soloviova',
            size=8, color=GRAY_RGB)


# ── Section header block ──────────────────────────────────────────────────────
def section_header(doc, title):
    doc.add_paragraph()   # small spacer
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    no_borders(tbl)
    cell = tbl.cell(0, 0)
    shd(cell, PURPLE_HEX)
    cell_margins(cell, 120)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    spacing(p, 20, 20)
    add_run(p, title, bold=True, size=11, color=WHITE_RGB)
    doc.add_paragraph()   # spacer after


# ── Orange sub-header ─────────────────────────────────────────────────────────
def sub_header(doc, text, before=80, after=40):
    p = para(doc, before=before, after=after)
    add_run(p, text, bold=True, size=10.5, color=ORANGE_RGB)


# ── Bullet line  ● orange dot + black text ───────────────────────────────────
def bullet(doc, text, after=50):
    p = para(doc, before=0, after=after)
    p.paragraph_format.left_indent     = Cm(0.6)
    p.paragraph_format.first_line_indent = Cm(-0.5)
    add_run(p, '● ', bold=False, color=ORANGE_RGB)
    add_run(p, text)


# ── Numbered meal item  N. orange + black text ────────────────────────────────
def numbered(doc, n, text, after=40):
    p = para(doc, before=0, after=after)
    p.paragraph_format.left_indent     = Cm(0.7)
    p.paragraph_format.first_line_indent = Cm(-0.6)
    add_run(p, f'{n}. ', bold=True, color=ORANGE_RGB)
    add_run(p, text)


# ── Dash line ─────────────────────────────────────────────────────────────────
def dash_line(doc, text, after=50):
    p = para(doc, before=0, after=after)
    p.paragraph_format.left_indent     = Cm(0.5)
    p.paragraph_format.first_line_indent = Cm(-0.4)
    add_run(p, '— ', bold=True)
    add_run(p, text)


# ── ✗ / ✓ lines ──────────────────────────────────────────────────────────────
def excl_line(doc, text, after=40):
    p = para(doc, before=0, after=after)
    p.paragraph_format.left_indent     = Cm(0.7)
    p.paragraph_format.first_line_indent = Cm(-0.6)
    add_run(p, '✗ ', bold=True, color=ORANGE_RGB)
    add_run(p, text)


def ok_line(doc, text, after=40):
    p = para(doc, before=0, after=after)
    p.paragraph_format.left_indent     = Cm(0.7)
    p.paragraph_format.first_line_indent = Cm(-0.6)
    add_run(p, '✓ ', bold=True, color=PURPLE_RGB)
    add_run(p, text)


# ── Highlight box (НОРМА ВОДИ) ────────────────────────────────────────────────
def highlight_box(doc, title, subtitle):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    no_borders(tbl)
    cell = tbl.cell(0, 0)
    shd(cell, LAVENDER_HEX)
    cell_margins(cell, 140)
    # border on left — purple
    tcPr = cell._tc.get_or_add_tcPr()
    tcBd = OxmlElement('w:tcBorders')
    left = OxmlElement('w:left')
    left.set(qn('w:val'),   'single')
    left.set(qn('w:sz'),    '18')
    left.set(qn('w:color'), PURPLE_HEX)
    tcBd.append(left)
    tcPr.append(tcBd)

    p1 = cell.paragraphs[0]
    spacing(p1, 10, 0)
    add_run(p1, title, bold=True, size=11, color=ORANGE_RGB)
    p2 = cell.add_paragraph()
    spacing(p2, 0, 10)
    add_run(p2, subtitle, italic=True, size=10, color=RGBColor(80, 80, 80))
    doc.add_paragraph()


# ══════════════════════════════════════════════════════════════════════════════
# BUILD DOCUMENT
# ══════════════════════════════════════════════════════════════════════════════
doc = Document()
section = doc.sections[0]
section.top_margin    = Cm(2.0)
section.bottom_margin = Cm(1.8)
section.left_margin   = Cm(2.0)
section.right_margin  = Cm(1.5)

PATIENT = 'Агу Ірина'
set_header_footer(section, PATIENT)

# ── COVER PAGE ────────────────────────────────────────────────────────────────
# Logo + Title row
cover = doc.add_table(rows=1, cols=2)
cover.alignment = WD_TABLE_ALIGNMENT.CENTER
no_borders(cover)
# Column widths via tblGrid
tblGrid = OxmlElement('w:tblGrid')
for w in (1440, 7920):          # ~2.5 cm logo, ~14 cm title
    gc = OxmlElement('w:gridCol')
    gc.set(qn('w:w'), str(w))
    tblGrid.append(gc)
cover._tbl.insert(0, tblGrid)

logo_cell  = cover.cell(0, 0)
title_cell = cover.cell(0, 1)

shd(logo_cell,  'F4F0FA')
shd(title_cell, PURPLE_HEX)
cell_margins(logo_cell,  160)
cell_margins(title_cell, 200)

# Logo text
lp = logo_cell.paragraphs[0]
lp.alignment = WD_ALIGN_PARAGRAPH.CENTER
spacing(lp, 60, 0)
add_run(lp, 'W', bold=True, size=20, color=PURPLE_RGB)
lp2 = logo_cell.add_paragraph()
lp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
spacing(lp2, 0, 0)
add_run(lp2, 'WELLNESS CODE', bold=True, size=7, color=PURPLE_RGB)
lp3 = logo_cell.add_paragraph()
lp3.alignment = WD_ALIGN_PARAGRAPH.CENTER
spacing(lp3, 0, 60)
add_run(lp3, 'by Anna Soloviova', italic=True, size=6.5, color=GRAY_RGB)

# Title
tp = title_cell.paragraphs[0]
spacing(tp, 40, 0)
add_run(tp, 'ПРОГРАМА КОРЕКЦІЇ\nВАГИ ТА ЗДОРОВ\'Я',
        bold=True, size=16, color=WHITE_RGB)

doc.add_paragraph()   # spacer

# Patient info block (lavender)
info = doc.add_table(rows=1, cols=1)
info.alignment = WD_TABLE_ALIGNMENT.CENTER
no_borders(info)
info_cell = info.cell(0, 0)
shd(info_cell, LAVENDER_HEX)
cell_margins(info_cell, 180)
# left purple border
tcPr2 = info_cell._tc.get_or_add_tcPr()
tcBd2 = OxmlElement('w:tcBorders')
lft2  = OxmlElement('w:left')
lft2.set(qn('w:val'),   'single')
lft2.set(qn('w:sz'),    '24')
lft2.set(qn('w:color'), PURPLE_HEX)
tcBd2.append(lft2)
tcPr2.append(tcBd2)

ip1 = info_cell.paragraphs[0]
spacing(ip1, 10, 0)
add_run(ip1, PATIENT, bold=True, size=20, color=ORANGE_RGB)

for line in [
    'Дата народження: 03.05.1977  |  Вік: 48 років',
    'Телефон: +491746670435',
    'Email: stbiz.dk@gmail.com  |  Місце проживання: Augsburg, Deutschland',
]:
    ip = info_cell.add_paragraph()
    spacing(ip, 0, 0)
    add_run(ip, line, size=10, color=BLACK_RGB)

doc.add_paragraph()

date_p = para(doc, WD_ALIGN_PARAGRAPH.RIGHT, before=0, after=120)
add_run(date_p, 'Дата складання: 05.06.2026', italic=True, size=10, color=GRAY_RGB)

# ── РЕЖИМ ────────────────────────────────────────────────────────────────────
section_header(doc, 'РЕЖИМ')
for t in [
    'Активний рух — кровообіг, обмін речовин, зниження АТ, нормалізація ваги. Починати м\'яко — без різких навантажень на хребет та суглоби.',
    'Паузи кожні 60 хв — вставати, розминатися, не перебувати довго в одному положенні (захист від защемлення сідничного нерва).',
    'Уникати підняття важкого — посилює гіперлордоз, навантаження на хребет та суглоби.',
    'Сон 7–8 годин — критично для відновлення нервової системи, зниження кортизолу, контролю ваги та зменшення панічних атак.',
    'Відбій о 22:00 — нормалізація мелатоніну, кортизолу. Безсоння прямо пов\'язане з тривожністю та набряками.',
    'Контроль набряків — піднімати ноги увечері 15–20 хв, обмежити сіль до 3–5 г/день, компресійні шкарпетки при тривалому сидінні.',
    'Ранок без різких звуків і стресу — 10–15 хв тиші або легкої музики. Кортизол зранку і так підвищений — не підсилювати його.',
]: bullet(doc, t)

# ── МОДИФІКАЦІЯ СПОСОБУ ЖИТТЯ ────────────────────────────────────────────────
section_header(doc, 'МОДИФІКАЦІЯ СПОСОБУ ЖИТТЯ')
for t in [
    'Знизити масу тіла — ціль: –50 кг (до 70 кг). Темп 4–5 кг/міс — повільно та стабільно. Швидке схуднення при такому надлишку ваги провокує відкат та стрес для організму.',
    'Зменшити обхват живота (143 см → до 78 см) — вісцеральний жир — головна причина підвищеного АТ, задишки, гіперлордозу та навантаження на суглоби.',
    'Дихальні вправи: вдих 1–2–3 → видих 1–2–3–4–5–6. 10–15 разів × 2 рази/день. Знижує кортизол, зменшує тривожність, допомагає при панічних атаках.',
    'Бодіфлекс 20–30 хвилин натщесерце або через 2,5–3 години після їжі — зміцнює м\'язи спини та живота, підтримує хребет та внутрішні органи.',
    'Ходьба 60 хв/день — починати з 10–15 хв. Покращує кровообіг, знижує АТ, зменшує набряки, розвантажує суглоби. Поступово збільшувати темп.',
    'Східні танці продовжувати — чудовий вибір для даного стану (м\'яке навантаження, координація, емоційний стан).',
    'Плавання або аквааеробіка 1–2 рази/тиж — ідеально при гіперлордозі, кіфозі, капсуліті, артриті та надлишковій вазі.',
    'Вимірювання вранці натщесерце 1 раз/тиж — вага, талія, живіт, груди, стегна + фото за інструкцією.',
    'Жувати їжу повільно — 25–30 рухів на шматок, 20–25 хв на прийом їжі, без телефону. Зменшує здуття та відрижку.',
    'Робота зі стресом — ключовий пріоритет! Дихальні практики, прогулянки, щоденник вдячності, сміхотерапія (10–15 хв смішних відео зранку).',
]: bullet(doc, t)

# ── ПАНІЧНІ АТАКИ ТА НЕРВОВА СИСТЕМА ────────────────────────────────────────
section_header(doc, 'ПАНІЧНІ АТАКИ ТА НЕРВОВА СИСТЕМА')

sub_header(doc, 'Щоденний антистресовий протокол:', before=0, after=30)
for t in [
    'Ранок: 5 хв дихальних вправ + склянка теплої води + 10 хв тиші (без телефону)',
    'Вдень: 2–3 паузи по 3 хв — закрити очі, глибоке дихання, розслабити плечі та щелепу',
    'Ввечері: 20 хв прогулянки або танців, щоденник вдячності (3 речі), відбій без гаджетів',
]: bullet(doc, t)

sub_header(doc, 'При панічній атаці:', after=30)
for t in [
    'Дихання 4–4–6 (вдих 4 сек → затримка 4 сек → видих 6 сек) — 10 разів. Активує парасимпатичну нервову систему.',
    'Холодна вода на зап\'ястя та обличчя — знижує частоту серцебиття.',
    'Заземлення: назвати 5 речей які бачите, 4 які можна доторкнутись, 3 які чуєте.',
    'Магній гліцинат — ключовий нутрієнт для зниження тривожності та нормалізації серцебиття.',
]: bullet(doc, t)

# ── ХРЕБЕТ ТА СУГЛОБИ ────────────────────────────────────────────────────────
section_header(doc, 'ХРЕБЕТ ТА СУГЛОБИ')
for t in [
    'НЕ ПІДНІМАТИ важкі предмети — мінімум перші 2 місяці.',
    'При болі в спині — горизонтальне положення на рівній поверхні 15–20 хв, легке розтягування.',
    'Плавання — найкращий вид активності при гіперлордозі та кіфозі.',
    'Ортопедична подушка та матрац середньої жорсткості.',
    'Кожні 10 кг знятої ваги — значно знижує навантаження на хребет та суглоби.',
    'Тепло на поперек при болі — не холод (при защемленні сідничного нерва).',
]: bullet(doc, t)

# ── АРТЕРІАЛЬНИЙ ТИСК ТА СЕРЦЕ ───────────────────────────────────────────────
section_header(doc, 'АРТЕРІАЛЬНИЙ ТИСК ТА СЕРЦЕ')
for t in [
    'Сіль — не більше 3–5 г/день. Основна причина підвищеного АТ разом з надлишковою вагою.',
    'Вода 2–2,5 л/день рівномірно.',
    'Продукти, багаті калієм та магнієм: авокадо, шпинат, броколі, гречка, гарбуз, горіхи.',
    'Алкоголь — виключити повністю. Алкоголь підвищує АТ на 5–10 мм рт.ст.',
    'При значному підвищенні АТ (вище 160/100) — звернутись до лікаря для медикаментозної корекції.',
]: bullet(doc, t)

# ── ВОДНИЙ РЕЖИМ ─────────────────────────────────────────────────────────────
section_header(doc, 'ВОДНИЙ РЕЖИМ — КРИТИЧНО ВАЖЛИВО')
highlight_box(doc,
    'НОРМА ВОДИ НА ДЕНЬ: 2,5–3,0 л — ОБОВ\'ЯЗКОВО!',
    'Зараз п\'єте 1000–1500 мл/день — цього недостатньо при вазі 120 кг та набряках.\n'
    'Саме через це набряки, здуття, відрижка, підвищений АТ.')

for t in [
    'Вранці натщесерце: 1 склянка теплої води → через 15 хв ще одна з ¼ лимона.',
    'Перед кожним прийомом їжі — склянка теплої води за 20–30 хв.',
    'Між прийомами їжі — пити рівномірно, не залпами.',
    'Увечері до 20:00 — основний об\'єм, після 20:00 мінімум (набряки).',
]: bullet(doc, t)

sub_header(doc, 'Що пити:', after=30)
bullet(doc, 'Чиста вода, трав\'яні чаї (ромашка, меліса, шипшина, хвощ при набряках), відвар шипшини, вода з лимоном.')
sub_header(doc, 'НЕ пити:', after=30)
bullet(doc, 'Солодкі напої, газована вода, пакетовані соки, алкоголь.')

# ── РЕЖИМ ХАРЧУВАННЯ ─────────────────────────────────────────────────────────
section_header(doc, 'РЕЖИМ ХАРЧУВАННЯ — 5 ПРИЙОМІВ НА ДЕНЬ')

# Meal schedule table
mt = doc.add_table(rows=6, cols=3)
mt.alignment = WD_TABLE_ALIGNMENT.CENTER
no_borders(mt)

headers = ['ЧАС', 'ПРИЙОМ ЇЖІ', 'ПОРЦІЯ']
rows_data = [
    ('07:00–08:00', 'СНІДАНОК',               '250–300 г'),
    ('10:30–11:00', '1-й ПЕРЕКУС',             '100–150 г'),
    ('13:00–14:00', 'ОБІД',                    '250–300 г'),
    ('16:00–16:30', '2-й ПЕРЕКУС',             '100–150 г'),
    ('18:30–19:00', 'ВЕЧЕРЯ — НЕ ПІЗНІШЕ 19:00', '250–300 г'),
]

for ci, h in enumerate(headers):
    c = mt.cell(0, ci)
    shd(c, PURPLE_HEX)
    cell_margins(c, 80)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    spacing(p, 40, 40)
    add_run(p, h, bold=True, size=10, color=WHITE_RGB)

for ri, (time, meal, portion) in enumerate(rows_data, 1):
    bg = LAVENDER_HEX if ri % 2 == 0 else 'F4F0FA'
    row = mt.rows[ri]
    for ci, val in enumerate([time, meal, portion]):
        c = row.cells[ci]
        shd(c, bg)
        cell_margins(c, 80)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ci != 1 else WD_ALIGN_PARAGRAPH.LEFT
        spacing(p, 30, 30)
        add_run(p, val, bold=(ci == 1), size=10,
                color=PURPLE_RGB if ci == 1 else BLACK_RGB)

doc.add_paragraph()

for t in [
    '5-разове харчування — стабілізує рівень цукру, знижує тягу до солодкого, зменшує вечірнє переїдання.',
    'НІКОЛИ не пропускати сніданок — запускає обмін речовин після ночі.',
    'Вечеря НЕ ПІЗНІШЕ 19:00. Після їжі 1–1,5 год не займати горизонтальне положення (здуття, відрижка, опущення органів).',
    'Жувати 25–30 рухів на шматок, їжа 20–25 хв, без телефону.',
    'Проміжки між прийомами — 2,5–3,5 год.',
]: bullet(doc, t)

# ── ХАРЧУВАННЯ — ВИКЛЮЧИТИ АБО ОБМЕЖИТИ ─────────────────────────────────────
section_header(doc, 'ХАРЧУВАННЯ — ВИКЛЮЧИТИ АБО ОБМЕЖИТИ')

sub_header(doc, 'ВИКЛЮЧИТИ повністю (мінімум 2 місяці):', before=0, after=30)
for t in [
    'Цукор, солодощі, випічка — тяга 6/10, але при такому надлишку ваги — бажано виключити',
    'Борошняне з глютеном (білий хліб, здоба, вареники, макарони) — здуття, набряки, уповільнення метаболізму',
    'Смажене, гостре, копчене — здуття, відрижка, навантаження на ШКТ',
    'Газовані та солодкі напої — здуття, набряки',
    'Алкоголь — підвищує АТ, посилює набряки, провокує тривожність',
    'Ананас та помідори — індивідуальна реакція (висипання на язиці)',
    'Коров\'яче молоко — замінити на козяче або рослинне',
]: excl_line(doc, t)

sub_header(doc, 'ОБМЕЖИТИ:', after=30)
for t in [
    'Картопля, білий рис — 2–3 рази/тиж, невеликими порціями',
    'Фрукти — тільки до 16:00, до 150–200 г/день',
    'Сіль — не більше 3–5 г/день',
    'Кава — максимум 1 чашка/день ПІСЛЯ їжі',
]: bullet(doc, t)

sub_header(doc, 'РЕКОМЕНДОВАНІ ПРОДУКТИ:', after=30)
for t in [
    'Овочі та зелень 400–500 г/день — основа раціону. Акцент: броколі, цвітна капуста, кабачок, огірок, шпинат, морква, буряк, гарбуз',
    'Яйця 2 шт./день — білок, холін (нервова система, печінка)',
    'Крупи без глютену: гречка, бурий рис, кіноа, пшоно — тільки сніданок/обід',
    'Риба нежирна 4–5 р/тиж (тріска, хек, судак) + жирна 1–2 р/тиж (лосось, скумбрія — Омега-3, суглоби, нервова система)',
    'Птиця (курка, індичка) 4–5 р/тиж — основне джерело білка',
    'Молочне козяче: йогурт, кефір — замість коров\'ячого',
    'Горіхи: волоські, мигдаль — 20–30 г/день (магній, Омега-3, нервова система)',
    'Авокадо — 2–3 р/тиж ½ шт. (калій — АТ, магній — нерви)',
    'Насіння льону, чіа — 1–2 ч.л./день (Омега-3, клітковина, гормональний баланс, міоми)',
    'Олія оливкова та лляна (холодна) — в салати',
    'Імбир, куркума — протизапальна дія (суглоби, капсуліт, артрит)',
]: ok_line(doc, t)

# ── СНІДАНКИ ─────────────────────────────────────────────────────────────────
section_header(doc, 'СНІДАНКИ — 15 ВАРІАНТІВ  (250–300 Г)')
for i, t in enumerate([
    'Омлет з 2 яєць + тушкований шпинат (100 г) + гречана каша (80 г)',
    'Гречана каша на воді (150 г) + 2 яйця некруто + огірок + 1 ч.л. лляної олії',
    'Кіноа (120 г) + варена куряча грудка (100 г) + зелень + ½ авокадо',
    'Пшоняна каша з гарбузом (180 г) + горіхи волоські 5 шт. + насіння льону ½ ч.л.',
    'Бурий рис (130 г) + 2 яйця некруто + огірок + зелень + 1 ч.л. оливкової олії',
    'Омлет зі шпинатом та броколі (2 яйця) + гречана каша (100 г)',
    'Кіноа (120 г) + тушковані овочі морква/кабачок (100 г) + яйце варене + насіння чіа 1 ч.л.',
    'Рисова каша на воді (150 г) + 1 яйце + груша (80 г) + горіхи 20 г',
    'Пшоняна каша з печеним яблуком (180 г) + кориця + мигдаль 10 шт.',
    'Гречка (120 г) + тушковані гриби (80 г) + яйце варене + зелень',
    'Омлет із броколі та кабачком (2 яйця) + бурий рис (100 г) + ½ авокадо',
    'Нутовий хумус (70 г) + рисові хлібці 2 шт. + огірок + морква (150 г)',
    'Рибні котлети на пару (тріска/хек) 150 г + гречка (100 г) + зелень',
    'Козячий йогурт без цукру (150 г) + ягоди заморожені (80 г) + насіння чіа 1 ч.л. + горіхи 20 г',
    'Яйця-пашот 2 шт. + рукола (50 г) + авокадо ½ + 1 ч.л. оливкової олії + рисовий хлібець',
], 1): numbered(doc, i, t)

# ── ПЕРЕКУСИ ─────────────────────────────────────────────────────────────────
section_header(doc, 'ПЕРЕКУСИ — 8 ВАРІАНТІВ  (100–150 Г)')
ip = para(doc, before=0, after=40)
add_run(ip, '(1-й перекус о 10:30, 2-й о 16:30 — обов\'язковий! Пропуск перекусу = вечірнє переїдання)',
        italic=True, size=9.5, color=GRAY_RGB)

for i, t in enumerate([
    'Яблуко зелене (120 г) + мигдаль 15 г',
    'Козячий йогурт без цукру (150 г) + насіння чіа 1 ч.л. + ягоди 50 г',
    'Груша (120 г) + волоський горіх 20 г',
    'Козячий кефір 150 мл + ягоди заморожені 50 г',
    'Овочеві палички (морква, огірок, селера 120 г) + хумус нутовий 30 г',
    'Горіхи мікс (30 г) + яблуко зелене (100 г)',
    '½ авокадо (80 г) + огірок (100 г) + лимонний сік',
    'Відварне яйце (1 шт.) + огірок (100 г) + зелень',
], 1): numbered(doc, i, t)

# ── ОБІДИ ────────────────────────────────────────────────────────────────────
section_header(doc, 'ОБІДИ — 15 ВАРІАНТІВ  (250–300 Г)')
for i, t in enumerate([
    'Куряче філе відварне (130 г) + гречка (100 г) + салат зі свіжих овочів з оливковою олією (80 г)',
    'Індичка тушкована (130 г) + пшоно (100 г) + тушковані овочі + зелень',
    'Лосось на пару (90–100 г) + кіноа (100 г) + тушковані зелені овочі (80 г) + лимон — до 2 р/тиж',
    'Куриний суп-пюре з овочами без молока/вершків — до 300 г',
    'Тріска запечена з лимоном (130 г) + бурий рис (100 г) + салат + оливкова олія',
    'Суп-пюре з червоної сочевиці з овочами без зажарки — до 300 г',
    'Куряча грудка (130 г) + бурий рис (100 г) + тушкована цвітна капуста (80 г)',
    'Борщ без зажарки з куркою — до 300 г + рисовий хлібець',
    'Рибні котлети на пару (130 г) + пюре з цвітної капусти (130 г) + зелень',
    'Нут тушкований з овочами (морква, кабачок, перець) — 250 г + зелень',
    'Скумбрія запечена (90–100 г) + гречка (100 г) + салат — 1–2 р/тиж',
    'Індичка відварна (130 г) + кіноа (100 г) + тушкована морква з куркумою (70 г)',
    'Суп-пюре гарбузовий (без вершків, з імбиром) — до 300 г + рисовий хлібець',
    'Суп з курячими фрикадельками та зеленню — до 300 г',
    'Хек запечений (130 г) + гречка (100 г) + тушкована капуста з морквою (80 г)',
], 1): numbered(doc, i, t)

# ── ВЕЧЕРІ ───────────────────────────────────────────────────────────────────
section_header(doc, 'ВЕЧЕРІ — 15 ВАРІАНТІВ  (250–300 Г)')
vp = para(doc, before=0, after=40)
add_run(vp, '(Легка, без круп, не пізніше 19:00)', italic=True, size=9.5, color=GRAY_RGB)

for i, t in enumerate([
    'Тріска на пару (140–150 г) + тушковані кабачки з морквою (130 г) + зелень',
    'Хек запечений (140 г) + тушкована капуста з морквою (130 г) + лимон',
    'Куряча грудка відварна (130 г) + тушкована стручкова квасоля (130 г) + зелень',
    'Рибні котлети на пару (130 г) + буряк відварний з оливковою олією (130 г)',
    'Омлет з 2 яєць + броколі на пару (130 г) + морква тушкована (80 г)',
    'Індичка відварна (130 г) + тушкована капуста з морквою (130 г)',
    'Крем-суп із броколі та кабачка без вершків — до 300 г',
    'Судак відварний (140 г) + овочеве рагу: кабачок, морква, перець (130 г)',
    'Лосось на пару (90 г) + броколі на пару (150 г) + лимон — до 2 р/тиж',
    'Креветки відварні (120 г) + рагу з овочів: кабачок, перець (130 г)',
    'Крем-суп гарбузовий з імбиром без вершків — до 300 г',
    'Кальмар відварний (120 г) + тушковані овочі (150 г) + 1 ч.л. оливкової олії',
    'Куряча грудка на грилі (130 г) + рукола + огірок + оливкова олія (130 г)',
    'Хек або минтай запечений (140 г) + тушкований перець з кабачком (130 г)',
    'Омлет з 2 яєць на пару + тушкована цвітна капуста з куркумою (150 г)',
], 1): numbered(doc, i, t)

# ── ВАЖЛИВО ПАМ'ЯТАТИ ────────────────────────────────────────────────────────
section_header(doc, 'ВАЖЛИВО ПАМ\'ЯТАТИ')
for t in [
    'Всі страви: варити, тушкувати, запікати, на пару. НЕ СМАЖИТИ.',
    'Сніданок ЗАВЖДИ — пропуск їжі провокує переїдання ввечері та уповільнення метаболізму.',
    'Вечеря НЕ ПІЗНІШЕ 19:00 — після їжі не лягати одразу (опущення органів, відрижка, здуття).',
    'Вода 2,5–3,0 л/день — без неї набряки, підвищений АТ, здуття, втома.',
    'Ананас та томати — виключити повністю (індивідуальна реакція).',
    'Суші та сире м\'ясо — виключити (є кіт вдома — паразитологічний ризик).',
    'Крупи — тільки на сніданок і обід. Вечеря — без круп.',
    'Фрукти — тільки до 16:00. Не більше 150–200 г/день.',
    'При болі в спині: не піднімати важке, горизонтальне положення 15 хв, тепло на поперек.',
    'Набряки ніг: піднімати ноги увечері 15 хв, обмежити сіль, прогулянки щогодини.',
    'Алкоголь — виключити повністю на час програми (підвищує АТ, набряки, тривожність).',
    'При панічній атаці: дихання 4–4–6, холодна вода на зап\'ястя, заземлення.',
]: dash_line(doc, t)

# ── СХЕМА КОРЕКЦІЇ ЗДОРОВ'Я ──────────────────────────────────────────────────
section_header(doc, 'СХЕМА КОРЕКЦІЇ ЗДОРОВ\'Я')

sub_header(doc, 'НУТРИЦІЙНА КОРЕКЦІЯ — ПРІОРИТЕТИ:', before=0, after=40)
for name, desc in [
    ('Магній гліцинат 400 мг перед сном',
     ' — КЛЮЧОВИЙ нутрієнт: панічні атаки, тривожність, безсоння, АТ, набряки, болісний цикл, міоми. Курс 3 міс.'),
    ('Омега-3 2000 мг під час їжі',
     ' — запалення, суглоби (капсуліт, артрит), нервова система, гормони, міоми. Курс 3 міс.'),
    ('Вітамін D3 4000 ОД',
     ' — імунітет, гормони, настрій, схуднення, кістки. 4 тижні → потім 2000 ОД довгостроково.'),
    ('К2 (МК-7) 100 мкг',
     ' — разом з D3, захист судин та кісток. Довгостроково.'),
    ('Вітамін В-комплекс (В6 + В12)',
     ' — нервова система, енергія, гормональний баланс, ПМС, панічні атаки. Курс 2 міс.'),
    ('Вітамін С 250 мг × 2 рази/день',
     ' — антиоксидант, судини, суглоби, імунітет, надниркові залози. Курс 2 міс.'),
    ('Цинк 25 мг під час їжі',
     ' — гормони, імунітет, шкіра, ПМС. Курс 2 міс.'),
    ('L-теанін 200 мг увечері',
     ' — тривожність, сон, заспокоєння без седативного ефекту. Курс 1 міс.'),
    ('5-НТР 150 мг зранку натщесерце і перед сном',
     ' — нормалізація роботи нервової системи. Курс 1 місяць.'),
    ('Насіння льону 1–2 ч.л./день у їжу',
     ' — фітоестрогени (підтримка при міомах), клітковина, Омега-3.'),
]:
    p = para(doc, before=0, after=50)
    p.paragraph_format.left_indent      = Cm(0.5)
    p.paragraph_format.first_line_indent = Cm(-0.4)
    add_run(p, '— ' + name, bold=True, size=10.5)
    add_run(p, desc, size=10.5)

# ── FOOTER BOX ───────────────────────────────────────────────────────────────
doc.add_paragraph()
ftbl = doc.add_table(rows=1, cols=1)
ftbl.alignment = WD_TABLE_ALIGNMENT.CENTER
no_borders(ftbl)
fc = ftbl.cell(0, 0)
shd(fc, 'FFFFFF')
cell_margins(fc, 200)
# Border: light purple all sides
fcPr = fc._tc.get_or_add_tcPr()
fcBd = OxmlElement('w:tcBorders')
for s in ('top','left','bottom','right'):
    be = OxmlElement(f'w:{s}')
    be.set(qn('w:val'),   'single')
    be.set(qn('w:sz'),    '12')
    be.set(qn('w:color'), PURPLE_HEX)
    fcBd.append(be)
fcPr.append(fcBd)

# Logo W
fp1 = fc.paragraphs[0]
fp1.alignment = WD_ALIGN_PARAGRAPH.CENTER
spacing(fp1, 20, 0)
add_run(fp1, 'W', bold=True, size=22, color=PURPLE_RGB)

fp2 = fc.add_paragraph()
fp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
spacing(fp2, 0, 0)
add_run(fp2, 'WELLNESS CODE', bold=True, size=8, color=PURPLE_RGB)

fp3 = fc.add_paragraph()
fp3.alignment = WD_ALIGN_PARAGRAPH.CENTER
spacing(fp3, 0, 20)
add_run(fp3, 'by Anna Soloviova', italic=True, size=7, color=GRAY_RGB)

fp4 = fc.add_paragraph()
fp4.alignment = WD_ALIGN_PARAGRAPH.CENTER
spacing(fp4, 10, 0)
add_run(fp4, 'З турботою і вірою у Вас,', italic=True, size=10.5, color=GRAY_RGB)

fp5 = fc.add_paragraph()
fp5.alignment = WD_ALIGN_PARAGRAPH.CENTER
spacing(fp5, 0, 0)
add_run(fp5, 'Лікар Анна Соловйова та команда', bold=True, size=12, color=PURPLE_RGB)

fp6 = fc.add_paragraph()
fp6.alignment = WD_ALIGN_PARAGRAPH.CENTER
spacing(fp6, 0, 20)
add_run(fp6, 'WELLNESS CODE by Anna Soloviova', bold=True, size=14, color=PURPLE_RGB)

# ─────────────────────────────────────────────────────────────────────────────
out = '/home/user/Soloviova/АГУ_Ірина_Програма_2026.docx'
doc.save(out)
print(f'DONE: {out}')
