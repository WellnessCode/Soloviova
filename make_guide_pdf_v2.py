"""Generate Wellness Code guide PDF in branded medical document style."""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ── Colors ─────────────────────────────────────────────────────────────────────
PURPLE  = colors.HexColor('#7B52AB')
GREEN   = colors.HexColor('#52AB7B')
LAVENDER= colors.HexColor('#EEE8F8')
L_GREEN = colors.HexColor('#E8F8EE')
WHITE   = colors.white
BLACK   = colors.HexColor('#1E1E1E')
GRAY    = colors.HexColor('#666666')
L_GRAY  = colors.HexColor('#F5F5F5')
LINE_CLR= colors.HexColor('#CCCCCC')

W, H = A4
DOC_TITLE = 'Як організувати харчування, щоб не жити на кухні'

# ── Register fonts ─────────────────────────────────────────────────────────────
registered = False
bold_registered = False
for d in ['/usr/share/fonts', '/usr/local/share/fonts']:
    if not os.path.isdir(d):
        continue
    for root, dirs, files in os.walk(d):
        for f in files:
            if f.lower() == 'dejavusans.ttf':
                try:
                    pdfmetrics.registerFont(TTFont('DejaVu', os.path.join(root, f)))
                    registered = True
                except: pass
            elif f.lower() == 'dejavusans-bold.ttf':
                try:
                    pdfmetrics.registerFont(TTFont('DejaVu-Bold', os.path.join(root, f)))
                    bold_registered = True
                except: pass

FONT      = 'DejaVu' if registered else 'Helvetica'
FONT_BOLD = ('DejaVu-Bold' if bold_registered else FONT) if registered else 'Helvetica-Bold'

# ── Styles ─────────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name,
        fontName   = kw.get('font', FONT),
        fontSize   = kw.get('size', 11),
        leading    = kw.get('leading', 16),
        textColor  = kw.get('color', BLACK),
        alignment  = kw.get('align', TA_LEFT),
        spaceAfter = kw.get('after', 4),
        spaceBefore= kw.get('before', 0),
        leftIndent = kw.get('left', 0),
    )

title_white = S('tw', font=FONT_BOLD, size=16, color=WHITE, leading=22, after=0)
author_name = S('an', font=FONT_BOLD, size=18, color=GREEN,  leading=26, after=4)
author_role = S('ar', font=FONT,      size=11, color=BLACK,  leading=16, after=2)
sec_hdr_s   = S('sh', font=FONT_BOLD, size=13, color=WHITE,  align=TA_CENTER, after=0, leading=18)
body_s      = S('bs', font=FONT,      size=11, color=BLACK,  leading=17, after=4, align=TA_JUSTIFY)
bold_s      = S('bd', font=FONT_BOLD, size=11, color=BLACK,  leading=17, after=4)
bullet_s    = S('bu', font=FONT,      size=11, color=BLACK,  leading=17, after=3, left=4)
orange_h_s  = S('oh', font=FONT_BOLD, size=12, color=PURPLE, leading=18, after=6)
gray_s      = S('gr', font=FONT,      size=9,  color=GRAY,   align=TA_RIGHT, after=0)
tbl_hdr     = S('th', font=FONT_BOLD, size=10, color=WHITE,  after=0)
tbl_lbl     = S('tl', font=FONT_BOLD, size=10, color=PURPLE, after=0)
tbl_val     = S('tv', font=FONT,      size=10, color=BLACK,  after=0)
green_lbl   = S('gl', font=FONT_BOLD, size=10, color=GREEN,  after=0)

def sp(n=8): return Spacer(1, n)

# ── Section header (full-width colored bar) ─────────────────────────────────
def sec_header(text, color=PURPLE):
    return Table(
        [[Paragraph(text, sec_hdr_s)]],
        colWidths=[17.0*cm],
        style=TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), color),
            ('TOPPADDING',    (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING',   (0,0), (-1,-1), 16),
            ('RIGHTPADDING',  (0,0), (-1,-1), 16),
        ])
    )

# ── Bullet line ────────────────────────────────────────────────────────────────
def bul(text, color=PURPLE):
    dot = f'<font color="#{color.hexval()[2:]}">●</font>'
    return Paragraph(f'{dot}  {text}', bullet_s)

def bul_g(text): return bul(text, GREEN)
def bul_p(text): return bul(text, PURPLE)

# ── Highlight box ──────────────────────────────────────────────────────────────
def info_box(text, bg=LAVENDER, fc=PURPLE):
    return Table(
        [[Paragraph(text, S('ib', font=FONT_BOLD, size=11, color=fc, leading=16, after=0))]],
        colWidths=[17.0*cm],
        style=TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), bg),
            ('TOPPADDING',    (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING',   (0,0), (-1,-1), 14),
            ('RIGHTPADDING',  (0,0), (-1,-1), 14),
            ('LINEAFTER',     (0,0), (0,-1), 4, fc),
        ])
    )

def info_box_g(text): return info_box(text, L_GREEN, GREEN)

# ── Running header/footer ──────────────────────────────────────────────────────
def page_header(canvas, doc):
    canvas.saveState()
    # Header line
    header_txt = f'WELLNESS CODE by Anna Soloviova  |  {DOC_TITLE}'
    canvas.setFont(FONT, 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(2*cm, H - 1.2*cm, header_txt)
    canvas.setStrokeColor(LINE_CLR)
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, H - 1.4*cm, W - 2*cm, H - 1.4*cm)
    # Footer line
    canvas.line(2*cm, 1.6*cm, W - 2*cm, 1.6*cm)
    # Page number
    canvas.setFont(FONT, 9)
    canvas.setFillColor(GRAY)
    canvas.drawRightString(W - 2*cm, 1.0*cm, str(doc.page))
    canvas.restoreState()

def first_page(canvas, doc):
    page_header(canvas, doc)

def later_pages(canvas, doc):
    page_header(canvas, doc)

# ── Grid table helper ──────────────────────────────────────────────────────────
def grid_table(rows, col_widths, header_color=PURPLE, alt_bg=LAVENDER):
    t = Table(rows, colWidths=col_widths)
    styles = [
        ('BACKGROUND',    (0,0), (-1,0), header_color),
        ('TEXTCOLOR',     (0,0), (-1,0), WHITE),
        ('FONTNAME',      (0,0), (-1,0), FONT_BOLD),
        ('FONTSIZE',      (0,0), (-1,-1), 10),
        ('TOPPADDING',    (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('RIGHTPADDING',  (0,0), (-1,-1), 8),
        ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#D4C8F0')),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]
    for i in range(1, len(rows)):
        bg = alt_bg if i % 2 == 1 else WHITE
        styles.append(('BACKGROUND', (0,i), (-1,i), bg))
    t.setStyle(TableStyle(styles))
    return t

# ── BUILD ──────────────────────────────────────────────────────────────────────
OUT = '/home/user/Soloviova/Гайд_Харчування_WellnessCode.pdf'
doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=2*cm, rightMargin=2*cm,
                        topMargin=2.5*cm, bottomMargin=2.2*cm)
story = []

# ════════════════════════════════════════════════════════
# COVER BLOCK — logo left / title right (как на скриншоте)
# ════════════════════════════════════════════════════════
logo_para = Paragraph(
    '<font size="28" color="#7B52AB"><b>W</b></font><br/>'
    '<font size="8" color="#7B52AB">WELLNESS CODE</font><br/>'
    '<font size="7" color="#999999">by Anna Soloviova</font>',
    S('lp', align=TA_CENTER, after=0, leading=14)
)
title_para = Paragraph('ГАЙД<br/>ЯК ОРГАНІЗУВАТИ ХАРЧУВАННЯ,<br/>ЩОБ НЕ ЖИТИ НА КУХНІ', title_white)

cover_block = Table(
    [[logo_para, title_para]],
    colWidths=[4.5*cm, 12.5*cm],
    style=TableStyle([
        ('BACKGROUND',    (0,0), (0,0), L_GRAY),
        ('BACKGROUND',    (1,0), (1,0), PURPLE),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1,-1), 20),
        ('BOTTOMPADDING', (0,0), (-1,-1), 20),
        ('LEFTPADDING',   (0,0), (0,0), 12),
        ('LEFTPADDING',   (1,0), (1,0), 20),
        ('RIGHTPADDING',  (0,0), (-1,-1), 12),
    ])
)
story.append(cover_block)
story.append(sp(20))

# Author card (як картка пацієнта)
author_card = Table(
    [[
        Table(
            [[Paragraph('Anna Soloviova', author_name)],
             [Paragraph('Лікар-дієтолог, нутриціолог', author_role)],
             [Paragraph('WELLNESS CODE by Anna Soloviova', author_role)]],
            colWidths=[15.8*cm],
            style=TableStyle([
                ('TOPPADDING',    (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ('LEFTPADDING',   (0,0), (-1,-1), 0),
            ])
        )
    ]],
    colWidths=[17*cm],
    style=TableStyle([
        ('BACKGROUND',   (0,0), (-1,-1), LAVENDER),
        ('LINEBEFORE',   (0,0), (0,-1), 5, PURPLE),
        ('TOPPADDING',   (0,0), (-1,-1), 12),
        ('BOTTOMPADDING',(0,0), (-1,-1), 12),
        ('LEFTPADDING',  (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ])
)
story.append(author_card)
story.append(sp(10))
story.append(Paragraph('Дата складання: 17.06.2026', gray_s))
story.append(sp(20))

# ════════════════════════════════════════════════════════
# SECTION 1 — ПРОБЛЕМА
# ════════════════════════════════════════════════════════
story.append(KeepTogether([
    sec_header('ПРОБЛЕМА', PURPLE),
    sp(10),
    Paragraph('Чому харчування перетворюється на каторгу?', orange_h_s),
    bul_p('Щодня думаємо «що приготувати?» — витрачаємо енергію на рішення'),
    bul_p('Часті походи в магазин = імпульсивні покупки + переплати'),
    bul_p('Готуємо щодня → втомлюємося → їмо що попало'),
    bul_p('Результат: стрес, зайва вага, гроші на вітер'),
    sp(8),
    info_box('РІШЕННЯ: система, а не сила волі'),
    sp(14),
]))

# ════════════════════════════════════════════════════════
# SECTION 2 — BATCH COOKING
# ════════════════════════════════════════════════════════
story.append(sec_header('ПРИНЦИП BATCH COOKING', GREEN))
story.append(sp(10))
story.append(Paragraph('Готуємо 2 рази на тиждень — їмо 7 днів', orange_h_s))
story.append(bul_g('День 1 (неділя): велике приготування на 3–4 дні'))
story.append(bul_g('День 2 (середа/четвер): невелике доготовування на залишок тижня'))
story.append(sp(10))
story.append(Paragraph('Що готуємо за 1 сесію (2–3 години):', bold_s))
batch_data = [
    ['Страва', 'Опис'],
    ['1–2 білкові страви', "М'ясо, риба, птиця"],
    ['2–3 гарніри', 'Крупи, запечені овочі'],
    ['Базові заправки', 'Салатні соуси та нарізки'],
    ['1 суп або крем-суп', 'На першу половину тижня'],
]
story.append(grid_table(batch_data, [7*cm, 10*cm], GREEN, L_GREEN))
story.append(sp(10))
story.append(info_box_g('Принцип конструктора: з одних продуктів — різні страви щодня'))
story.append(sp(14))

# ════════════════════════════════════════════════════════
# SECTION 3 — ПЛАНУВАННЯ МЕНЮ
# ════════════════════════════════════════════════════════
story.append(sec_header('ПЛАНУВАННЯ МЕНЮ', PURPLE))
story.append(sp(10))
story.append(Paragraph('Алгоритм на 5 хвилин', orange_h_s))
story.append(Paragraph('<b>Крок 1:</b> Визначити 2 білки (курка, риба, яловичина, індичка, яйця)', body_s))
story.append(Paragraph('<b>Крок 2:</b> Визначити 3 гарніри (гречка, рис, булгур, батат, картопля)', body_s))
story.append(Paragraph('<b>Крок 3:</b> Додати 4–5 видів овочів (свіжі + для запікання)', body_s))
story.append(Paragraph('<b>Крок 4:</b> Скласти список покупок', body_s))
story.append(sp(10))
story.append(Paragraph("Зразок меню на тиждень (сім'я 3 особи):", bold_s))
menu_data = [
    ['День', 'Меню'],
    ['Пн / Вт', 'Куряче філе + гречка + свіжий салат'],
    ['Середа', 'Запечена риба + батат + тушковані овочі'],
    ['Чт / Пт', 'Котлети з індички + рис + тушковані овочі'],
    ['Сб / Нд', "Яловичина з овочами в мультиварці + салат"],
]
story.append(grid_table(menu_data, [3.5*cm, 13.5*cm]))
story.append(sp(14))

# ════════════════════════════════════════════════════════
# SECTION 4 — ЗАКУПИ
# ════════════════════════════════════════════════════════
story.append(sec_header('ЗАКУПИ', GREEN))
story.append(sp(10))
story.append(Paragraph("Структура кошика (сім'я 3–5 осіб):", bold_s))
shop_data = [
    ['Категорія', 'Продукти', '%'],
    ['Білки', 'Куряче філе 1–1,5 кг · Риба 1 кг · Яйця 15–20 шт · Фарш 500 г', '40%'],
    ['Овочі та зелень', 'Броколі, цвітна капуста, цукіні, морква, помідори, перець, шпинат', '30%'],
    ['Крупи', 'Гречка, рис, булгур, вівсянка, батат, сочевиця', '20%'],
    ['Запас', 'Консерви (тунець, нут, квасоля), олія, спеції, горіхи', '10%'],
]
story.append(grid_table(shop_data, [4*cm, 10.5*cm, 2.5*cm], GREEN, L_GREEN))
story.append(sp(10))
story.append(info_box_g('Лайфхак: зберігайте список у телефоні як шаблон — оновлюйте щотижня 5 хвилин'))
story.append(sp(14))

# ════════════════════════════════════════════════════════
# SECTION 5 — ГАДЖЕТИ
# ════════════════════════════════════════════════════════
story.append(sec_header('ГАДЖЕТИ, ЯКІ ЗМІНЮЮТЬ ЖИТТЯ', PURPLE))
story.append(sp(10))
gadgets = [
    ('Мультиварка', "Закинув і забув. М'ясо, каші, супи, тушковані овочі. Час активної роботи: 5 хв"),
    ('Духовка', 'Деко з пергаментом, 180°C, 40 хв. Мінімум зусиль — максимум смаку'),
    ('Блендер / чоппер', 'Крем-супи, соуси, нарізка за 2 хвилини'),
    ('Вакуумний пакувальник', 'Зберігає їжу в 2–3 рази довше'),
    ('Контейнери з підписами', 'Порційне зберігання готових страв'),
    ('Пароварка', 'Паровий спосіб зберігає максимум поживних речовин'),
]
for name, desc in gadgets:
    row = Table(
        [[Paragraph(name, S('gn', font=FONT_BOLD, size=11, color=WHITE, after=0)),
          Paragraph(desc, S('gd', font=FONT, size=11, color=BLACK, after=0))]],
        colWidths=[4.5*cm, 12.5*cm],
        style=TableStyle([
            ('BACKGROUND',    (0,0), (0,0), PURPLE),
            ('BACKGROUND',    (1,0), (1,0), LAVENDER),
            ('TOPPADDING',    (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING',   (0,0), (-1,-1), 10),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ('LINEBELOW',     (0,0), (-1,-1), 0.5, WHITE),
        ])
    )
    story.append(row)
story.append(sp(10))
story.append(info_box('Принцип: один гаджет = звільнена година на тиждень'))
story.append(sp(14))

# ════════════════════════════════════════════════════════
# SECTION 6 — ПЛАН СЕСІЇ
# ════════════════════════════════════════════════════════
story.append(sec_header('СЕСІЯ ПРИГОТУВАННЯ: ПОКРОКОВИЙ ПЛАН', GREEN))
story.append(sp(10))
story.append(Paragraph('Неділя, 2,5 години — їжа на 4 дні', orange_h_s))
steps = [
    ('0:00–0:20', 'Мити, чистити, нарізати всі овочі одразу'),
    ('0:20–0:30', "Завантажити мультиварку (м'ясо / каша на таймер)"),
    ('0:30–1:00', 'Викласти овочі на деко, поставити в духовку'),
    ('1:00–1:30', 'Зварити 2 гарніри на плиті, зробити соус/заправку'),
    ('1:30–2:00', 'Приготувати суп або крем-суп'),
    ('2:00–2:30', 'Розкласти по контейнерах, підписати, охолодити'),
]
for time, desc in steps:
    row = Table(
        [[Paragraph(time, S('st', font=FONT_BOLD, size=11, color=WHITE, align=TA_CENTER, after=0)),
          Paragraph(desc, S('sd', font=FONT, size=11, color=BLACK, after=0))]],
        colWidths=[2.8*cm, 14.2*cm],
        style=TableStyle([
            ('BACKGROUND',    (0,0), (0,0), GREEN),
            ('BACKGROUND',    (1,0), (1,0), L_GREEN),
            ('TOPPADDING',    (0,0), (-1,-1), 9),
            ('BOTTOMPADDING', (0,0), (-1,-1), 9),
            ('LEFTPADDING',   (0,0), (-1,-1), 8),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ('LINEBELOW',     (0,0), (-1,-1), 0.5, WHITE),
        ])
    )
    story.append(row)
story.append(sp(10))
story.append(info_box_g('Результат: 8–10 готових компонентів для збирання страв протягом тижня'))
story.append(sp(14))

# ════════════════════════════════════════════════════════
# SECTION 7 — КОНТРОЛЬ ВАГИ
# ════════════════════════════════════════════════════════
story.append(sec_header('КОНТРОЛЬ ВАГИ БЕЗ ДІЄТ', PURPLE))
story.append(sp(10))
story.append(bul_p('Готова їжа вдома = немає спокуси замовити піцу'))
story.append(bul_p('Порційні контейнери = автоматичний контроль розміру порції'))
story.append(bul_p('Білок у кожному прийомі = ситість на 3–4 години'))
story.append(bul_p('Мінімум обробленої їжі = менше цукру та солі'))
story.append(sp(10))
story.append(Paragraph('Формула збалансованої тарілки:', bold_s))
plate_data = [
    ['Частина', 'Продукт'],
    ['1/2 тарілки', 'Овочі (свіжі або запечені)'],
    ['1/4 тарілки', "Білок (м'ясо / риба / яйця / бобові)"],
    ['1/4 тарілки', 'Складні вуглеводи (крупа / батат)'],
    ['1 ст. ложка', 'Корисний жир (олія / авокадо / горіхи)'],
]
story.append(grid_table(plate_data, [4*cm, 13*cm]))
story.append(sp(10))
story.append(info_box('Лайфхак: якщо порція вже розкладена — переїсти значно важче'))
story.append(sp(14))

# ════════════════════════════════════════════════════════
# SECTION 8 — ЛАЙФХАКИ
# ════════════════════════════════════════════════════════
story.append(sec_header('ТОП-10 ЛАЙФХАКІВ', GREEN))
story.append(sp(10))
hacks = [
    'Варіть яйця одразу десяток — вистачить на тиждень',
    "Маринуйте м'ясо відразу після покупки — потім просто в духовку",
    'Бланшуйте і заморожуйте сезонні овочі в сезон',
    'Каша в мультиварці на таймері — готова до сніданку',
    'Заправку для салату робіть одразу на 5 днів (банка в холодильнику)',
    'Лимонний сік, заморожений у кубиках льоду — завжди під рукою',
    'Контейнери одного розміру — зручно складати в холодильнику',
    'Список покупок = лише те що в меню. Жодних імпульсів',
    'Зелень замочіть у воді — простоїть свіжою цілий тиждень',
    'Таймер у духовці — поставив і пішов займатись своїми справами',
]
for i, h in enumerate(hacks):
    num_para = Paragraph(f'0{i+1}' if i < 9 else '10',
                         S('hn', font=FONT_BOLD, size=12, color=WHITE, align=TA_CENTER, after=0))
    txt_para = Paragraph(h, S('hd', font=FONT, size=11, color=BLACK, after=0))
    row = Table(
        [[num_para, txt_para]],
        colWidths=[1.4*cm, 15.6*cm],
        style=TableStyle([
            ('BACKGROUND',    (0,0), (0,0), GREEN),
            ('BACKGROUND',    (1,0), (1,0), L_GREEN if i % 2 == 0 else WHITE),
            ('TOPPADDING',    (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING',   (0,0), (-1,-1), 8),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ('LINEBELOW',     (0,0), (-1,-1), 0.5, WHITE),
        ])
    )
    story.append(row)
story.append(sp(14))

# ════════════════════════════════════════════════════════
# SECTION 9 — РЕЗУЛЬТАТИ
# ════════════════════════════════════════════════════════
story.append(sec_header('ЩО ВИ ОТРИМУЄТЕ', PURPLE))
story.append(sp(10))
results = [
    ('5–7 годин', 'вільного часу на тиждень'),
    ('20–30%', 'економія бюджету на їжу'),
    ('Контроль ваги', 'без стресу і дієт'),
    ('Здорове харчування', 'для всієї родини'),
    ('Менше стресу', 'більше енергії та сил'),
]
for val, desc in results:
    row = Table(
        [[Paragraph(val, S('rv', font=FONT_BOLD, size=13, color=WHITE, align=TA_CENTER, after=0)),
          Paragraph(desc, S('rd', font=FONT, size=12, color=BLACK, after=0))]],
        colWidths=[5*cm, 12*cm],
        style=TableStyle([
            ('BACKGROUND',    (0,0), (0,0), PURPLE),
            ('BACKGROUND',    (1,0), (1,0), LAVENDER),
            ('TOPPADDING',    (0,0), (-1,-1), 11),
            ('BOTTOMPADDING', (0,0), (-1,-1), 11),
            ('LEFTPADDING',   (0,0), (-1,-1), 14),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ('LINEBELOW',     (0,0), (-1,-1), 2, WHITE),
        ])
    )
    story.append(row)
    story.append(sp(3))
story.append(sp(14))

# ════════════════════════════════════════════════════════
# SECTION 10 — ПЕРШИЙ КРОК
# ════════════════════════════════════════════════════════
story.append(sec_header('ВАШ ПЕРШИЙ КРОК', GREEN))
story.append(sp(10))
first_steps = [
    ('Крок 1', 'Скласти меню на 7 днів', '15 хв'),
    ('Крок 2', 'Написати список покупок за шаблоном', '10 хв'),
    ('Крок 3', 'Виділити 2,5 години в неділю для першої сесії', 'блокуємо в календарі'),
]
for s_num, s_desc, s_time in first_steps:
    row = Table(
        [[Paragraph(s_num,  S('sn', font=FONT_BOLD, size=11, color=WHITE, align=TA_CENTER, after=0)),
          Paragraph(s_desc, S('sd', font=FONT,      size=11, color=BLACK, after=0)),
          Paragraph(s_time, S('st', font=FONT_BOLD, size=10, color=GREEN, align=TA_CENTER, after=0))]],
        colWidths=[2.5*cm, 10.5*cm, 4*cm],
        style=TableStyle([
            ('BACKGROUND',    (0,0), (0,0), GREEN),
            ('BACKGROUND',    (1,0), (1,0), L_GREEN),
            ('BACKGROUND',    (2,0), (2,0), WHITE),
            ('TOPPADDING',    (0,0), (-1,-1), 11),
            ('BOTTOMPADDING', (0,0), (-1,-1), 11),
            ('LEFTPADDING',   (0,0), (-1,-1), 10),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ('LINEBELOW',     (0,0), (-1,-1), 2, WHITE),
            ('BOX',           (0,0), (-1,-1), 0.5, colors.HexColor('#C8E8D4')),
        ])
    )
    story.append(row)
    story.append(sp(5))

story.append(sp(20))

# ════════════════════════════════════════════════════════
# БОНУС — Шаблони
# ════════════════════════════════════════════════════════
story.append(sec_header('БОНУС: ШАБЛОН МЕНЮ НА ТИЖДЕНЬ', PURPLE))
story.append(sp(10))
menu_tmpl = [
    ['День', 'Сніданок', 'Обід', 'Вечеря'],
    ['Понеділок', '', '', ''],
    ['Вівторок', '', '', ''],
    ['Середа', '', '', ''],
    ['Четвер', '', '', ''],
    ["П'ятниця", '', '', ''],
    ['Субота', '', '', ''],
    ['Неділя', '', '', ''],
]
story.append(grid_table(menu_tmpl, [3*cm, 4.7*cm, 4.7*cm, 4.6*cm]))
story.append(sp(20))

story.append(sec_header('БОНУС: ШАБЛОН СПИСКУ ПОКУПОК', GREEN))
story.append(sp(10))
shop_tmpl = [
    ['Білки', 'Кількість', 'Овочі та зелень', 'Кількість'],
    ['Куряче філе', '', 'Броколі', ''],
    ['Риба (хек/лосось)', '', 'Цвітна капуста', ''],
    ['Яйця', '', 'Цукіні', ''],
    ['Фарш', '', 'Морква', ''],
    ['', '', 'Перець, помідори', ''],
    ['Крупи та вуглеводи', 'Кількість', 'Запас', 'Кількість'],
    ['Гречка', '', 'Тунець (конс.)', ''],
    ['Рис / булгур', '', 'Нут / квасоля', ''],
    ['Вівсянка', '', 'Оливкова олія', ''],
    ['Батат', '', 'Горіхи / насіння', ''],
]
t_shop = Table(shop_tmpl, colWidths=[4.6*cm, 2.4*cm, 4.6*cm, 5.4*cm])
shop_styles = [
    ('BACKGROUND',    (0,0), (-1,0), GREEN),
    ('TEXTCOLOR',     (0,0), (-1,0), WHITE),
    ('FONTNAME',      (0,0), (-1,0), FONT_BOLD),
    ('BACKGROUND',    (0,6), (-1,6), PURPLE),
    ('TEXTCOLOR',     (0,6), (-1,6), WHITE),
    ('FONTNAME',      (0,6), (-1,6), FONT_BOLD),
    ('FONTSIZE',      (0,0), (-1,-1), 10),
    ('TOPPADDING',    (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LEFTPADDING',   (0,0), (-1,-1), 8),
    ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#D4C8F0')),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
]
for i in range(1, 6):
    bg = L_GREEN if i % 2 == 1 else WHITE
    shop_styles.append(('BACKGROUND', (0,i), (-1,i), bg))
for i in range(7, 11):
    bg = LAVENDER if i % 2 == 1 else WHITE
    shop_styles.append(('BACKGROUND', (0,i), (-1,i), bg))
t_shop.setStyle(TableStyle(shop_styles))
story.append(t_shop)

# ── Build ───────────────────────────────────────────────────────────────────────
doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
print(f'Saved: {OUT}')
