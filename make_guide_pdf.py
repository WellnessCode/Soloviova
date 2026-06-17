"""Generate Wellness Code guide PDF in Ukrainian."""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, PageBreak, HRFlowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ── Colors ────────────────────────────────────────────────────────────────────
PURPLE = colors.HexColor('#7B52AB')
ORANGE = colors.HexColor('#F0811E')
LAVENDER = colors.HexColor('#EEE8F8')
LIGHT_ORANGE = colors.HexColor('#FEF0E6')
WHITE = colors.white
BLACK = colors.HexColor('#1E1E1E')
GRAY = colors.HexColor('#666666')

W, H = A4

# ── Register fonts ─────────────────────────────────────────────────────────────
font_dirs = ['/usr/share/fonts', '/usr/local/share/fonts',
             os.path.expanduser('~/.fonts'), '/home/user/Soloviova']
registered = False
bold_registered = False
italic_registered = False
for d in font_dirs:
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
            elif f.lower() in ('dejavusans-oblique.ttf', 'dejavusans-italic.ttf'):
                try:
                    pdfmetrics.registerFont(TTFont('DejaVu-Italic', os.path.join(root, f)))
                    italic_registered = True
                except: pass

FONT = 'DejaVu' if registered else 'Helvetica'
FONT_BOLD = ('DejaVu-Bold' if bold_registered else FONT) if registered else 'Helvetica-Bold'
FONT_ITALIC = ('DejaVu-Italic' if italic_registered else FONT) if registered else 'Helvetica-Oblique'

# ── Styles ────────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, fontName=kw.get('font', FONT),
                          fontSize=kw.get('size', 11),
                          leading=kw.get('leading', 16),
                          textColor=kw.get('color', BLACK),
                          alignment=kw.get('align', TA_LEFT),
                          spaceAfter=kw.get('after', 6),
                          spaceBefore=kw.get('before', 0),
                          leftIndent=kw.get('left', 0))

cover_title  = S('ct', font=FONT_BOLD, size=28, color=WHITE, align=TA_CENTER, leading=36, after=12)
cover_sub    = S('cs', font=FONT, size=14, color=WHITE, align=TA_CENTER, leading=20, after=8)
cover_author = S('ca', font=FONT_BOLD, size=13, color=ORANGE, align=TA_CENTER, leading=18, after=4)
cover_role   = S('cr', font=FONT_ITALIC, size=11, color=WHITE, align=TA_CENTER, leading=16)

sec_num   = S('sn', font=FONT_BOLD, size=10, color=ORANGE, after=2)
sec_title = S('st', font=FONT_BOLD, size=16, color=PURPLE, leading=22, after=8)
body      = S('bd', font=FONT, size=11, color=BLACK, leading=17, after=5, align=TA_JUSTIFY)
bold_body = S('bb', font=FONT_BOLD, size=11, color=BLACK, leading=17, after=5)
bullet    = S('bu', font=FONT, size=11, color=BLACK, leading=16, after=3, left=12)
orange_h  = S('oh', font=FONT_BOLD, size=12, color=ORANGE, leading=18, after=4)
note      = S('nt', font=FONT_ITALIC, size=10, color=GRAY, leading=15, after=6)
step_s    = S('sp', font=FONT_BOLD, size=11, color=PURPLE, leading=16, after=3)

def hr(): return HRFlowable(width='100%', thickness=1, color=LAVENDER, spaceAfter=10, spaceBefore=4)
def sp(n=8): return Spacer(1, n)

def section_box(number, title):
    return Table([[Paragraph(f'{number}', S('x', font=FONT_BOLD, size=14, color=WHITE, align=TA_CENTER)),
                   Paragraph(title, S('x', font=FONT_BOLD, size=14, color=WHITE))]],
                 colWidths=[1.2*cm, 14*cm],
                 style=TableStyle([
                     ('BACKGROUND', (0,0), (-1,-1), PURPLE),
                     ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                     ('TOPPADDING', (0,0), (-1,-1), 8),
                     ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                     ('LEFTPADDING', (0,0), (0,0), 10),
                     ('LEFTPADDING', (1,0), (1,0), 8),
                     ('RIGHTPADDING', (0,0), (-1,-1), 8),
                 ]))

def highlight_box(text, bg=LAVENDER, fc=PURPLE):
    return Table([[Paragraph(text, S('x', font=FONT_BOLD, size=11, color=fc, leading=16))]],
                 colWidths=[15.2*cm],
                 style=TableStyle([
                     ('BACKGROUND', (0,0), (-1,-1), bg),
                     ('TOPPADDING', (0,0), (-1,-1), 8),
                     ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                     ('LEFTPADDING', (0,0), (-1,-1), 12),
                     ('RIGHTPADDING', (0,0), (-1,-1), 12),
                     ('ROUNDEDCORNERS', [4]),
                 ]))


# ── Cover page background ─────────────────────────────────────────────────────
def cover_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PURPLE)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # Decorative circles
    canvas.setFillColor(colors.HexColor('#9B72CB'))
    canvas.circle(W, H, 180, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor('#6A3D9A'))
    canvas.circle(0, 0, 140, fill=1, stroke=0)
    canvas.setFillColor(ORANGE)
    canvas.circle(W*0.5, H*0.12, 60, fill=1, stroke=0)
    canvas.restoreState()

def normal_bg(canvas, doc):
    canvas.saveState()
    # Thin purple top bar
    canvas.setFillColor(PURPLE)
    canvas.rect(0, H-0.8*cm, W, 0.8*cm, fill=1, stroke=0)
    # Page number
    canvas.setFillColor(GRAY)
    canvas.setFont(FONT, 9)
    canvas.drawRightString(W-2*cm, 1*cm, f'{doc.page}')
    # Footer line
    canvas.setStrokeColor(LAVENDER)
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, 1.4*cm, W-2*cm, 1.4*cm)
    # Footer text
    canvas.setFillColor(GRAY)
    canvas.setFont(FONT_ITALIC, 8)
    canvas.drawString(2*cm, 0.7*cm, 'WELLNESS CODE by Anna Soloviova')
    canvas.restoreState()


# ── Build document ─────────────────────────────────────────────────────────────
OUT = '/home/user/Soloviova/Гайд_Харчування_WellnessCode.pdf'
doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=2*cm, rightMargin=2*cm,
                        topMargin=2.5*cm, bottomMargin=2*cm)

story = []

# ═══════════════════════════════════════════════════════════════
# COVER
# ═══════════════════════════════════════════════════════════════
story.append(sp(80))
story.append(Paragraph('ГАЙД', S('x', font=FONT_BOLD, size=13, color=ORANGE, align=TA_CENTER, after=6)))
story.append(sp(10))
story.append(Paragraph('Як організувати харчування,', cover_title))
story.append(Paragraph('щоб не жити на кухні', cover_title))
story.append(sp(20))
story.append(Paragraph('Закупи на тиждень · Готування 2 рази · Лайфхаки для зайнятих', cover_sub))
story.append(Paragraph('Для сімей 2–5 осіб | Контроль ваги | Українська та європейська кухня', cover_sub))
story.append(sp(60))
story.append(Paragraph('Автор:', S('x', font=FONT, size=11, color=WHITE, align=TA_CENTER, after=2)))
story.append(Paragraph('Anna Soloviova', cover_author))
story.append(Paragraph('Лікар-дієтолог, нутриціолог', cover_role))
story.append(Paragraph('WELLNESS CODE by Anna Soloviova', cover_role))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 1 — ПРОБЛЕМА
# ═══════════════════════════════════════════════════════════════
story.append(section_box('01', 'Проблема, яку ми вирішуємо'))
story.append(sp(10))
story.append(Paragraph('Чому харчування перетворюється на каторгу?', orange_h))
story.append(Paragraph('• Щодня думаємо «що приготувати?» — витрачаємо енергію на рішення', bullet))
story.append(Paragraph('• Часті походи в магазин = імпульсивні покупки + переплати', bullet))
story.append(Paragraph('• Готуємо щодня → втомлюємося → їмо що попало', bullet))
story.append(Paragraph('• Результат: стрес, зайва вага, гроші на вітер', bullet))
story.append(sp(8))
story.append(highlight_box('РІШЕННЯ: система, а не сила волі'))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 2 — BATCH COOKING
# ═══════════════════════════════════════════════════════════════
story.append(section_box('02', 'Принцип Batch Cooking'))
story.append(sp(10))
story.append(Paragraph('Готуємо 2 рази на тиждень — їмо 7 днів', orange_h))
story.append(Paragraph('День 1 (неділя): велике приготування на 3–4 дні', bullet))
story.append(Paragraph('День 2 (середа/четвер): невелике доготовування на залишок тижня', bullet))
story.append(sp(8))
story.append(Paragraph('Що готуємо за 1 сесію (2–3 години):', bold_body))

data = [
    ['1–2 білкові страви', 'М\'ясо, риба, птиця'],
    ['2–3 гарніри', 'Крупи, запечені овочі'],
    ['Базові заправки', 'Салатні соуси та нарізки'],
    ['1 суп або крем-суп', 'На першу половину тижня'],
]
t = Table(data, colWidths=[7*cm, 8.2*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), LAVENDER),
    ('BACKGROUND', (0,1), (-1,1), WHITE),
    ('BACKGROUND', (0,2), (-1,2), LAVENDER),
    ('BACKGROUND', (0,3), (-1,3), WHITE),
    ('FONTNAME', (0,0), (0,-1), FONT_BOLD),
    ('FONTNAME', (1,0), (1,-1), FONT),
    ('FONTSIZE', (0,0), (-1,-1), 11),
    ('TEXTCOLOR', (0,0), (0,-1), PURPLE),
    ('TEXTCOLOR', (1,0), (1,-1), BLACK),
    ('TOPPADDING', (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D4C8F0')),
]))
story.append(t)
story.append(sp(10))
story.append(highlight_box('Принцип конструктора: з одних продуктів — різні страви щодня'))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 3 — ПЛАНУВАННЯ МЕНЮ
# ═══════════════════════════════════════════════════════════════
story.append(section_box('03', 'Планування меню на тиждень'))
story.append(sp(10))
story.append(Paragraph('Алгоритм на 5 хвилин', orange_h))
story.append(Paragraph('<b>Крок 1:</b> Визначити 2 білки (курка, риба, яловичина, індичка, яйця)', body))
story.append(Paragraph('<b>Крок 2:</b> Визначити 3 гарніри (гречка, рис, булгур, батат, картопля)', body))
story.append(Paragraph('<b>Крок 3:</b> Додати 4–5 видів овочів (свіжі + для запікання)', body))
story.append(Paragraph('<b>Крок 4:</b> Скласти список покупок', body))
story.append(sp(8))
story.append(Paragraph('Зразок меню на тиждень (сім\'я 3 особи):', bold_body))

menu = [
    ['День', 'Меню'],
    ['Пн / Вт', 'Куряче філе + гречка + свіжий салат'],
    ['Середа', 'Запечена риба + батат + тушковані овочі'],
    ['Чт / Пт', 'Котлети з індички + рис + тушковані овочі'],
    ['Сб / Нд', 'Яловичина з овочами в мультиварці + салат'],
]
mt = Table(menu, colWidths=[3.5*cm, 11.7*cm])
mt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PURPLE),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), FONT_BOLD),
    ('BACKGROUND', (0,1), (-1,1), LAVENDER),
    ('BACKGROUND', (0,2), (-1,2), WHITE),
    ('BACKGROUND', (0,3), (-1,3), LAVENDER),
    ('BACKGROUND', (0,4), (-1,4), WHITE),
    ('FONTNAME', (0,1), (0,-1), FONT_BOLD),
    ('TEXTCOLOR', (0,1), (0,-1), ORANGE),
    ('FONTNAME', (1,1), (1,-1), FONT),
    ('FONTSIZE', (0,0), (-1,-1), 11),
    ('TOPPADDING', (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D4C8F0')),
]))
story.append(mt)
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 4 — ЗАКУПИ
# ═══════════════════════════════════════════════════════════════
story.append(section_box('04', 'Закупи: список і бюджет'))
story.append(sp(10))
story.append(Paragraph('Як закупитися раз на тиждень і нічого не забути', orange_h))
story.append(Paragraph('Структура кошика (сім\'я 3–5 осіб):', bold_body))

shop = [
    ['Категорія', 'Продукти', '%'],
    ['Білки', 'Куряче філе 1–1,5 кг · Риба (хек/лосось) 1 кг\nЯйця 15–20 шт · Фарш 500 г', '40%'],
    ['Овочі та зелень', 'Броколі, цвітна капуста, цукіні, морква\nПомідори, перець, шпинат, огірки', '30%'],
    ['Крупи та вуглеводи', 'Гречка, рис, булгур, вівсянка, батат, сочевиця', '20%'],
    ['Запас', 'Консерви (тунець, нут, квасоля)\nОлія, спеції, горіхи', '10%'],
]
st = Table(shop, colWidths=[4*cm, 9*cm, 2.2*cm])
st.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PURPLE),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), FONT_BOLD),
    ('BACKGROUND', (0,1), (-1,1), LIGHT_ORANGE),
    ('BACKGROUND', (0,2), (-1,2), WHITE),
    ('BACKGROUND', (0,3), (-1,3), LIGHT_ORANGE),
    ('BACKGROUND', (0,4), (-1,4), WHITE),
    ('FONTNAME', (0,1), (0,-1), FONT_BOLD),
    ('TEXTCOLOR', (0,1), (0,-1), PURPLE),
    ('FONTNAME', (2,1), (2,-1), FONT_BOLD),
    ('TEXTCOLOR', (2,1), (2,-1), ORANGE),
    ('ALIGN', (2,0), (2,-1), 'CENTER'),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('TOPPADDING', (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D4C8F0')),
]))
story.append(st)
story.append(sp(10))
story.append(highlight_box('Лайфхак: зберігайте список у телефоні як шаблон — оновлюйте щотижня 5 хвилин'))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 5 — ГАДЖЕТИ
# ═══════════════════════════════════════════════════════════════
story.append(section_box('05', 'Гаджети, які змінюють життя'))
story.append(sp(10))
story.append(Paragraph('Ваші помічники на кухні', orange_h))

gadgets = [
    ('Мультиварка', 'Закинув і забув. М\'ясо, каші, супи, тушковані овочі. Час активної роботи: 5 хв'),
    ('Духовка', 'Деко з пергаментом, 180°C, 40 хв. Мінімум зусиль — максимум смаку'),
    ('Блендер / чоппер', 'Крем-супи, соуси, нарізка за 2 хвилини'),
    ('Вакуумний пакувальник', 'Зберігає їжу в 2–3 рази довше'),
    ('Контейнери з підписами', 'Порційне зберігання готових страв'),
    ('Пароварка', 'Паровий спосіб зберігає максимум поживних речовин'),
]
for g_name, g_desc in gadgets:
    row = Table([[Paragraph(g_name, S('x', font=FONT_BOLD, size=11, color=WHITE)),
                  Paragraph(g_desc, S('x', font=FONT, size=11, color=BLACK))]],
                colWidths=[4.5*cm, 10.7*cm])
    row.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), ORANGE),
        ('BACKGROUND', (1,0), (1,0), LAVENDER),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, WHITE),
    ]))
    story.append(row)
    story.append(sp(3))
story.append(sp(6))
story.append(highlight_box('Принцип: один гаджет = звільнена година на тиждень'))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 6 — ПЛАН СЕСІЇ
# ═══════════════════════════════════════════════════════════════
story.append(section_box('06', 'Сесія приготування: покроковий план'))
story.append(sp(10))
story.append(Paragraph('Неділя, 2,5 години — їжа на 4 дні', orange_h))

steps = [
    ('0:00–0:20', 'Мити, чистити, нарізати всі овочі одразу'),
    ('0:20–0:30', 'Завантажити мультиварку (м\'ясо / каша на таймер)'),
    ('0:30–1:00', 'Викласти овочі на деко, поставити в духовку'),
    ('1:00–1:30', 'Зварити 2 гарніри на плиті, зробити соус/заправку'),
    ('1:30–2:00', 'Приготувати суп або крем-суп'),
    ('2:00–2:30', 'Розкласти по контейнерах, підписати, охолодити'),
]
for time, desc in steps:
    row = Table([[Paragraph(time, S('x', font=FONT_BOLD, size=11, color=WHITE, align=TA_CENTER)),
                  Paragraph(desc, S('x', font=FONT, size=11, color=BLACK))]],
                colWidths=[2.5*cm, 12.7*cm])
    row.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), PURPLE),
        ('BACKGROUND', (1,0), (1,0), LAVENDER),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 1, WHITE),
    ]))
    story.append(row)
    story.append(sp(3))
story.append(sp(8))
story.append(highlight_box('Результат: 8–10 готових компонентів для збирання страв протягом тижня'))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 7 — КОНТРОЛЬ ВАГИ
# ═══════════════════════════════════════════════════════════════
story.append(section_box('07', 'Контроль ваги без дієт'))
story.append(sp(10))
story.append(Paragraph('Як система харчування допомагає схуднути', orange_h))
story.append(Paragraph('Готова їжа вдома = немає спокуси замовити піцу', bullet))
story.append(Paragraph('Порційні контейнери = автоматичний контроль розміру порції', bullet))
story.append(Paragraph('Білок у кожному прийомі = ситість на 3–4 години', bullet))
story.append(Paragraph('Мінімум обробленої їжі = менше цукру та солі', bullet))
story.append(sp(10))
story.append(Paragraph('Формула збалансованої тарілки:', orange_h))

plate = [
    ['1/2 тарілки', 'Овочі (свіжі або запечені)'],
    ['1/4 тарілки', 'Білок (м\'ясо / риба / яйця / бобові)'],
    ['1/4 тарілки', 'Складні вуглеводи (крупа / батат)'],
    ['1 ст. ложка', 'Корисний жир (олія / авокадо / горіхи)'],
]
pt = Table(plate, colWidths=[3.5*cm, 11.7*cm])
pt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,-1), ORANGE),
    ('TEXTCOLOR', (0,0), (0,-1), WHITE),
    ('FONTNAME', (0,0), (0,-1), FONT_BOLD),
    ('BACKGROUND', (1,0), (1,0), LAVENDER),
    ('BACKGROUND', (1,1), (1,1), WHITE),
    ('BACKGROUND', (1,2), (1,2), LAVENDER),
    ('BACKGROUND', (1,3), (1,3), WHITE),
    ('FONTNAME', (1,0), (1,-1), FONT),
    ('FONTSIZE', (0,0), (-1,-1), 11),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('GRID', (0,0), (-1,-1), 0.5, WHITE),
]))
story.append(pt)
story.append(sp(10))
story.append(highlight_box('Лайфхак: якщо порція вже розкладена — переїсти значно важче'))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 8 — ЛАЙФХАКИ
# ═══════════════════════════════════════════════════════════════
story.append(section_box('08', 'Топ-10 лайфхаків'))
story.append(sp(10))
story.append(Paragraph('Економимо час і нерви', orange_h))

hacks = [
    ('01', 'Варіть яйця одразу десяток — вистачить на тиждень'),
    ('02', 'Маринуйте м\'ясо відразу після покупки — потім просто в духовку'),
    ('03', 'Бланшуйте і заморожуйте сезонні овочі в сезон'),
    ('04', 'Каша в мультиварці на таймері — готова до сніданку'),
    ('05', 'Заправку для салату робіть одразу на 5 днів (банка в холодильнику)'),
    ('06', 'Лимонний сік, заморожений у кубиках льоду — завжди під рукою'),
    ('07', 'Контейнери одного розміру — зручно складати в холодильнику'),
    ('08', 'Список покупок = лише те що в меню. Жодних імпульсів'),
    ('09', 'Зелень замочіть у воді — простоїть свіжою цілий тиждень'),
    ('10', 'Таймер у духовці — поставив і пішов займатись своїми справами'),
]
for num, hack in hacks:
    row = Table([[Paragraph(num, S('x', font=FONT_BOLD, size=12, color=WHITE, align=TA_CENTER)),
                  Paragraph(hack, S('x', font=FONT, size=11, color=BLACK))]],
                colWidths=[1.2*cm, 14*cm])
    row.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), ORANGE),
        ('BACKGROUND', (1,0), (1,0), LAVENDER if int(num)%2==1 else WHITE),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 1, WHITE),
    ]))
    story.append(row)
    story.append(sp(2))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 9 — РЕЗУЛЬТАТИ
# ═══════════════════════════════════════════════════════════════
story.append(section_box('09', 'Що ви отримуєте, впровадивши систему'))
story.append(sp(14))

results = [
    ('5–7 годин', 'вільного часу на тиждень'),
    ('20–30%', 'економія бюджету на їжу'),
    ('Контроль ваги', 'без стресу і дієт'),
    ('Здорове харчування', 'для всієї родини'),
    ('Менше стресу', 'більше енергії та сил'),
]
for val, desc in results:
    row = Table([[Paragraph(val, S('x', font=FONT_BOLD, size=13, color=WHITE, align=TA_CENTER)),
                  Paragraph(desc, S('x', font=FONT, size=12, color=BLACK))]],
                colWidths=[5*cm, 10.2*cm])
    row.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), PURPLE),
        ('BACKGROUND', (1,0), (1,0), LAVENDER),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 2, WHITE),
    ]))
    story.append(row)
    story.append(sp(5))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 10 — ПЕРШИЙ КРОК + БОНУС ШАБЛОНИ
# ═══════════════════════════════════════════════════════════════
story.append(section_box('10', 'Ваш перший крок на цьому тижні'))
story.append(sp(10))

first_steps = [
    ('Крок 1', 'Скласти меню на 7 днів', '15 хв'),
    ('Крок 2', 'Написати список покупок за шаблоном нижче', '10 хв'),
    ('Крок 3', 'Виділити 2,5 години в неділю для першої сесії', 'блокуємо в календарі'),
]
for s_num, s_desc, s_time in first_steps:
    row = Table([[Paragraph(s_num, S('x', font=FONT_BOLD, size=11, color=WHITE, align=TA_CENTER)),
                  Paragraph(s_desc, S('x', font=FONT, size=11, color=BLACK)),
                  Paragraph(s_time, S('x', font=FONT_BOLD, size=10, color=ORANGE, align=TA_CENTER))]],
                colWidths=[2.5*cm, 9.5*cm, 3.2*cm])
    row.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), PURPLE),
        ('BACKGROUND', (1,0), (1,0), LAVENDER),
        ('BACKGROUND', (2,0), (2,0), LIGHT_ORANGE),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 2, WHITE),
    ]))
    story.append(row)
    story.append(sp(4))

story.append(sp(14))

# БОНУС — Шаблон меню
story.append(Paragraph('БОНУС: Шаблон меню на тиждень', S('x', font=FONT_BOLD, size=13, color=PURPLE, after=8)))
menu_tmpl = [['День', 'Сніданок', 'Обід', 'Вечеря'],
             ['Понеділок', '', '', ''],
             ['Вівторок', '', '', ''],
             ['Середа', '', '', ''],
             ['Четвер', '', '', ''],
             ['П\'ятниця', '', '', ''],
             ['Субота', '', '', ''],
             ['Неділя', '', '', '']]
mt2 = Table(menu_tmpl, colWidths=[2.8*cm, 4.1*cm, 4.1*cm, 4.2*cm])
ts2 = TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PURPLE),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), FONT_BOLD),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('FONTNAME', (0,1), (0,-1), FONT_BOLD),
    ('TEXTCOLOR', (0,1), (0,-1), ORANGE),
    ('TOPPADDING', (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D4C8F0')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [LAVENDER, WHITE]),
])
mt2.setStyle(ts2)
story.append(mt2)

story.append(sp(14))

# БОНУС — Шаблон списку покупок
story.append(Paragraph('БОНУС: Шаблон списку покупок', S('x', font=FONT_BOLD, size=13, color=PURPLE, after=8)))
shop_tmpl = [
    ['Білки', 'Кількість', 'Овочі та зелень', 'Кількість'],
    ['Куряче філе', '', 'Броколі', ''],
    ['Риба (хек/лосось)', '', 'Цвітна капуста', ''],
    ['Яйця', '', 'Цукіні', ''],
    ['Фарш', '', 'Морква', ''],
    ['', '', 'Перець, помідори', ''],
    ['Крупи', 'Кількість', 'Запас', 'Кількість'],
    ['Гречка', '', 'Тунець (конс.)', ''],
    ['Рис / булгур', '', 'Нут / квасоля', ''],
    ['Вівсянка', '', 'Оливкова олія', ''],
    ['Батат', '', 'Горіхи', ''],
]
st2 = Table(shop_tmpl, colWidths=[4.5*cm, 2.5*cm, 4.5*cm, 3.7*cm])
ts3 = TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PURPLE),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), FONT_BOLD),
    ('BACKGROUND', (0,6), (-1,6), ORANGE),
    ('TEXTCOLOR', (0,6), (-1,6), WHITE),
    ('FONTNAME', (0,6), (-1,6), FONT_BOLD),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('TOPPADDING', (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D4C8F0')),
    ('ROWBACKGROUNDS', (0,1), (-1,5), [LAVENDER, WHITE]),
    ('ROWBACKGROUNDS', (0,7), (-1,-1), [LIGHT_ORANGE, WHITE]),
])
st2.setStyle(ts3)
story.append(st2)

# ── Build ──────────────────────────────────────────────────────────────────────
def first_page(c, d):
    cover_bg(c, d)

def later_pages(c, d):
    normal_bg(c, d)

doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
print(f'Saved: {OUT}')
