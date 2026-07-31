# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    Table, TableStyle, ListFlowable, ListItem, HRFlowable, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ---------- Fonts ----------
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DejaVu", FONT_DIR + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", FONT_DIR + "DejaVuSans-Bold.ttf"))
FONT = "DejaVu"
FONT_BOLD = "DejaVu-Bold"

# ---------- Brand colors ----------
PURPLE = HexColor("#7B52AB")
PURPLE_DARK = HexColor("#5C3D82")
ORANGE = HexColor("#F0811E")
GREEN = HexColor("#52AB7B")
GREEN_DARK = HexColor("#3C8560")
DARK = HexColor("#2C2C2C")
GRAY = HexColor("#6B6B6B")
LIGHT_PURPLE = HexColor("#F4F0FA")
LIGHT_GREEN = HexColor("#E8F3EC")
LIGHT_ORANGE = HexColor("#FFF4E6")
WHITE = HexColor("#FFFFFF")

PAGE_W, PAGE_H = A4

# ---------- Styles ----------
styles = {}
styles['h1'] = ParagraphStyle('h1', fontName=FONT_BOLD, fontSize=22, leading=26,
                              textColor=PURPLE, spaceAfter=6, spaceBefore=4)
styles['h2'] = ParagraphStyle('h2', fontName=FONT_BOLD, fontSize=15, leading=19,
                              textColor=GREEN_DARK, spaceAfter=6, spaceBefore=10)
styles['body'] = ParagraphStyle('body', fontName=FONT, fontSize=10.5, leading=15,
                                textColor=DARK, spaceAfter=5, alignment=TA_LEFT)
styles['bodyw'] = ParagraphStyle('bodyw', fontName=FONT, fontSize=10.5, leading=15,
                                 textColor=WHITE, spaceAfter=4)
styles['bullet'] = ParagraphStyle('bullet', fontName=FONT, fontSize=10.5, leading=14.5,
                                  textColor=DARK, leftIndent=4)
styles['small'] = ParagraphStyle('small', fontName=FONT, fontSize=9, leading=12,
                                 textColor=GRAY)
styles['cardtitle'] = ParagraphStyle('cardtitle', fontName=FONT_BOLD, fontSize=12,
                                     leading=15, textColor=PURPLE)
styles['step_head'] = ParagraphStyle('step_head', fontName=FONT_BOLD, fontSize=13,
                                     leading=16, textColor=ORANGE, spaceAfter=3)


def bulleted(items, color=GREEN, size=10.5):
    flow = []
    st = ParagraphStyle('b', fontName=FONT, fontSize=size, leading=14.5, textColor=DARK)
    lst = ListFlowable(
        [ListItem(Paragraph(t, st), value='circle', leftIndent=14) for t in items],
        bulletType='bullet', start='circle', bulletColor=color, bulletFontSize=7,
        leftIndent=10,
    )
    flow.append(lst)
    return flow


# ---------- Page decoration ----------
def header_footer(canvas, doc):
    canvas.saveState()
    # running header
    canvas.setFont(FONT_BOLD, 8)
    canvas.setFillColor(GREEN)
    canvas.drawString(2*cm, PAGE_H - 1.1*cm, "WELLNESS CODE BY ANNA")
    canvas.setFont(FONT, 8)
    canvas.setFillColor(GRAY)
    canvas.drawRightString(PAGE_W - 2*cm, PAGE_H - 1.1*cm, "Гайд · Пробіотик L. reuteri")
    canvas.setStrokeColor(HexColor("#E0DCD3"))
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, PAGE_H - 1.3*cm, PAGE_W - 2*cm, PAGE_H - 1.3*cm)
    # footer
    canvas.setFont(FONT, 8)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(PAGE_W/2, 1*cm, f"Anna Soloviova · Лікар-дієтолог, нутриціолог · сторінка {doc.page}")
    canvas.restoreState()


def cover_page(canvas, doc):
    canvas.saveState()
    # background band
    canvas.setFillColor(PURPLE)
    canvas.rect(0, PAGE_H - 9*cm, PAGE_W, 9*cm, fill=1, stroke=0)
    canvas.setFillColor(GREEN)
    canvas.rect(0, PAGE_H - 9.4*cm, PAGE_W, 0.4*cm, fill=1, stroke=0)
    # tag
    canvas.setFont(FONT_BOLD, 10)
    canvas.setFillColor(WHITE)
    canvas.drawString(2*cm, PAGE_H - 2.3*cm, "WELLNESS CODE BY ANNA · ГАЙД")
    # title
    canvas.setFont(FONT_BOLD, 30)
    canvas.setFillColor(WHITE)
    canvas.drawString(2*cm, PAGE_H - 4.4*cm, "Пробіотик")
    canvas.drawString(2*cm, PAGE_H - 5.7*cm, "L. reuteri")
    canvas.setFont(FONT, 14)
    canvas.drawString(2*cm, PAGE_H - 7*cm, "Бактерія, що керує гормонами,")
    canvas.drawString(2*cm, PAGE_H - 7.7*cm, "кістками, настроєм і шкірою")
    # author block
    canvas.setFillColor(LIGHT_PURPLE)
    canvas.roundRect(2*cm, PAGE_H - 13*cm, PAGE_W - 4*cm, 2.6*cm, 10, fill=1, stroke=0)
    canvas.setFillColor(ORANGE)
    canvas.rect(2*cm, PAGE_H - 13*cm, 0.15*cm, 2.6*cm, fill=1, stroke=0)
    canvas.setFont(FONT_BOLD, 13)
    canvas.setFillColor(PURPLE_DARK)
    canvas.drawString(2.6*cm, PAGE_H - 11*cm, "Anna Soloviova")
    canvas.setFont(FONT, 10.5)
    canvas.setFillColor(DARK)
    canvas.drawString(2.6*cm, PAGE_H - 11.6*cm, "Лікар-дієтолог, нутриціолог")
    canvas.drawString(2.6*cm, PAGE_H - 12.2*cm, "і мама проєкту WELLNESS CODE by Anna Soloviova")
    # bottom note
    canvas.setFont(FONT, 9)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(PAGE_W/2, 2*cm,
        "Освітній матеріал. Не замінює консультацію лікаря.")
    canvas.restoreState()


# ---------- Card helper ----------
class Card(Table):
    pass


def make_card(inner_flowables, bg, width=PAGE_W - 4*cm, border=None, pad=10):
    t = Table([[inner_flowables]], colWidths=[width])
    style = [
        ('BACKGROUND', (0, 0), (-1, -1), bg),
        ('LEFTPADDING', (0, 0), (-1, -1), pad + 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), pad + 2),
        ('TOPPADDING', (0, 0), (-1, -1), pad),
        ('BOTTOMPADDING', (0, 0), (-1, -1), pad),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
    ]
    if border:
        style.append(('LINEBELOW', (0, 0), (-1, -1), 0, bg))
        style.append(('BOX', (0, 0), (-1, -1), 1.5, border))
    t.setStyle(TableStyle(style))
    return t


# ---------- Build document ----------
doc = BaseDocTemplate(
    "/home/user/Soloviova/Гайд_Пробіотик_Reuteri_WellnessCode.pdf",
    pagesize=A4, leftMargin=2*cm, rightMargin=2*cm,
    topMargin=1.6*cm, bottomMargin=1.6*cm,
)
frame = Frame(2*cm, 1.6*cm, PAGE_W - 4*cm, PAGE_H - 3.2*cm, id='main')
doc.addPageTemplates([
    PageTemplate(id='cover', frames=[frame], onPage=cover_page),
    PageTemplate(id='content', frames=[frame], onPage=header_footer),
])

story = []
from reportlab.platypus import NextPageTemplate, PageBreak

# COVER (blank frame, drawn by cover_page)
story.append(NextPageTemplate('content'))
story.append(PageBreak())

# ===== Section 1: What is it =====
story.append(Paragraph("Що таке L. reuteri", styles['h1']))
story.append(HRFlowable(width="100%", thickness=1.5, color=PURPLE, spaceAfter=8))
story.append(Paragraph(
    "<b>Lactobacillus reuteri</b> (нова назва — <i>Limosilactobacillus reuteri</i>) — "
    "одна з найбільш вивчених пробіотичних бактерій. Живе природно в кишківнику людини, "
    "у грудному молоці й ротовій порожнині. Це «рідна» для людини бактерія, а не чужорідна — "
    "тому вона безпечна і діє мʼяко.", styles['body']))

story.append(Paragraph("Чим особлива серед інших пробіотиків", styles['h2']))
story.append(Paragraph(
    "Більшість пробіотиків просто «заселяють» кишківник. Reuteri діє <b>системно</b> — "
    "впливає на весь організм одразу через три механізми:", styles['body']))

mech = [
    ("1. Виробляє власний антибіотик — реутерин",
     "Природна речовина, що вбиває патогенні бактерії, гриби (кандида), віруси і паразитів — "
     "але не чіпає корисну флору. Це наче «розумний антибіотик»."),
    ("2. Підвищує окситоцин («гормон прив’язаності»)",
     "Доведено дослідженнями MIT: reuteri стимулює вироблення окситоцину через блукаючий нерв. "
     "Наслідки — краще загоєння ран, кращий настрій, менше тривоги, ефект «молодшої шкіри»."),
    ("3. Знижує запалення",
     "Зменшує прозапальні цитокіни, підвищує регуляторні Т-клітини. Корисно при аутоімунних станах."),
]
for title, txt in mech:
    inner = [Paragraph(title, styles['cardtitle']),
             Spacer(1, 3),
             Paragraph(txt, styles['body'])]
    story.append(make_card(inner, LIGHT_GREEN))
    story.append(Spacer(1, 7))

# ===== Section 2: Strains table =====
story.append(Paragraph("Головні штами і за що відповідають", styles['h2']))
strain_data = [
    ["Штам", "Для чого"],
    ["DSM 17938", "Кольки у немовлят, діарея, імунітет, здоров’я кишківника"],
    ["ATCC PTA 6475\n(Gastrus)", "Кістки (щільність!), тестостерон, окситоцин, запалення"],
    ["Prodentis\n(17938 + 5289)", "Здоров’я ясен і зубів, проти карієсу й пародонтозу"],
]
strain_tbl = Table(strain_data, colWidths=[4.2*cm, PAGE_W - 4*cm - 4.2*cm])
strain_tbl.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PURPLE),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, 0), FONT_BOLD),
    ('FONTNAME', (0, 1), (0, -1), FONT_BOLD),
    ('FONTNAME', (1, 1), (-1, -1), FONT),
    ('TEXTCOLOR', (0, 1), (0, -1), PURPLE_DARK),
    ('TEXTCOLOR', (1, 1), (-1, -1), DARK),
    ('FONTSIZE', (0, 0), (-1, -1), 9.5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_PURPLE]),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#E0DCD3")),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
story.append(strain_tbl)
story.append(Spacer(1, 10))

# ===== Section 3: Benefits =====
story.append(PageBreak())
story.append(Paragraph("Доведена користь", styles['h1']))
story.append(HRFlowable(width="100%", thickness=1.5, color=PURPLE, spaceAfter=8))

benefits = [
    ("🌿 Травлення", [
        "Прибирає здуття і симптоми СРК",
        "Допомагає проти H. pylori (гелікобактер) у комплексі",
        "Відновлює флору після антибіотиків",
        "Кольки у немовлят — золотий стандарт (штам DSM 17938)",
    ]),
    ("💗 Гормони і настрій", [
        "Підвищує окситоцин → менше стресу, краща прив’язаність",
        "У чоловіків підтримує тестостерон",
        "Покращує сон (через блукаючий нерв)",
    ]),
    ("🦴 Кістки", [
        "Штам 6475 зупиняє втрату кісткової маси",
        "Важливо при менопаузі й остеопорозі (є клінічні дослідження на жінках)",
    ]),
    ("✨ Шкіра", [
        "«Ефект сяйва» — через окситоцин і зниження запалення",
        "Допомагає при екземі й атопічному дерматиті",
    ]),
    ("🦷 Ротова порожнина", [
        "Проти карієсу, гінгівіту й неприємного запаху (штам Prodentis)",
    ]),
    ("🛡 Імунітет", [
        "Менше застуд, коротший перебіг",
        "Підтримка при алергіях",
    ]),
]
for title, items in benefits:
    inner = [Paragraph(title, styles['cardtitle']), Spacer(1, 4)]
    inner += bulleted(items, color=GREEN, size=10)
    story.append(make_card(inner, WHITE, border=HexColor("#E0DCD3")))
    story.append(Spacer(1, 7))

# ===== Section 4: How to take =====
story.append(PageBreak())
story.append(Paragraph("Як приймати", styles['h1']))
story.append(HRFlowable(width="100%", thickness=1.5, color=PURPLE, spaceAfter=8))
take_items = [
    "<b>Дозування:</b> зазвичай 1–10 млрд КУО на день (залежить від штаму)",
    "<b>Коли:</b> можна натщесерце або з їжею",
    "<b>Форми:</b> таблетки для розсмоктування, краплі (для дітей), капсули",
    "<b>Курс:</b> від 4 тижнів; для стійкого ефекту — 2–3 місяці",
]
for t in take_items:
    story.append(Paragraph("•  " + t, styles['body']))
story.append(Spacer(1, 6))

# Caution card
inner = [Paragraph("⚠️ Кому обережно", ParagraphStyle('c', fontName=FONT_BOLD, fontSize=12, textColor=ORANGE)),
         Spacer(1, 4)]
inner += bulleted([
    "Імунодефіцит, хіміотерапія — тільки після консультації",
    "Центральний венозний катетер — ризик",
    "Тяжкі захворювання — з лікарем",
    "Здоровим людям — безпечний, це «рідна» бактерія",
], color=ORANGE, size=10)
story.append(make_card(inner, LIGHT_ORANGE))
story.append(Spacer(1, 8))

# Brands
story.append(Paragraph("Популярні бренди (для орієнтиру)", styles['h2']))
story.append(Paragraph(
    "<b>BioGaia</b> (Швеція) — найвідоміший, штами DSM 17938, Gastrus, Prodentis. "
    "Золотий стандарт досліджень.", styles['body']))
story.append(Paragraph("Обирай за задачею:", styles['body']))
story += bulleted([
    "Немовлята / кишківник → BioGaia Protectis (краплі)",
    "Кістки / гормони / запалення → BioGaia Gastrus",
    "Зуби / ясна → BioGaia Prodentis",
], color=GREEN)

# ===== Section 5: Homemade yogurt =====
story.append(PageBreak())
story.append(Paragraph("Бонус: домашній reuteri-йогурт", styles['h1']))
story.append(HRFlowable(width="100%", thickness=1.5, color=ORANGE, spaceAfter=8))
story.append(Paragraph(
    "Домашній йогурт містить у <b>100+ разів більше</b> бактерій, ніж капсули — "
    "і виходить значно дешевше. Один флакон закваски = багато місяців йогурту.", styles['body']))
story.append(Spacer(1, 4))

# Ingredients card
inner = [Paragraph("🛒 Що потрібно", styles['cardtitle']), Spacer(1, 4)]
inner += bulleted([
    "10 таблеток BioGaia Gastrus (тільки на перший раз — як стартова закваска)",
    "1 літр вершків (10–18%) або незбираного молока",
    "2 столові ложки інуліну або цукру (їжа для бактерій)",
    "Йогуртниця або мультиварка з точним контролем t° (потрібно 36–38 °C, НЕ вище!)",
    "Скляна банка з кришкою, чиста ложка",
], color=GREEN, size=10)
story.append(make_card(inner, LIGHT_GREEN))
story.append(Spacer(1, 8))

# Steps
story.append(Paragraph("👩‍🍳 Покроково", styles['h2']))
steps = [
    ("Крок 1. Підготувати закваску",
     "Розтовкти 10 таблеток Gastrus у порошок. Змішати з інуліном/цукром і 2 ложками "
     "вершків до однорідної пасти — без грудочок."),
    ("Крок 2. Зʼєднати з вершками",
     "Додати пасту в решту вершків (1 л), добре розмішати. Перелити в чисту банку."),
    ("Крок 3. Ферментація 36 годин",
     "Поставити при <b>36–38 °C рівно на 36 годин</b>. Це головне: вище 40 °C бактерії "
     "гинуть, менше 36 годин — не встигають розмножитись. Тому потрібен точний прилад."),
    ("Крок 4. Готово",
     "Через 36 годин зʼявиться густа кремова маса з приємним кислуватим смаком. "
     "Зберігати в холодильнику до 1–2 тижнів."),
    ("Крок 5. Наступні порції",
     "Тепер таблетки НЕ потрібні. Просто бери <b>2 ложки готового йогурту</b> як закваску "
     "для нового літра. Так можна робити багато разів поспіль."),
]
for title, txt in steps:
    inner = [Paragraph(title, styles['step_head']), Paragraph(txt, styles['body'])]
    story.append(make_card(inner, WHITE, border=HexColor("#E0DCD3")))
    story.append(Spacer(1, 6))

# Dosage note
inner = [Paragraph("🥄 Як їсти", styles['cardtitle']), Spacer(1, 3),
         Paragraph(
    "Починай з <b>1 чайної ложки на день</b> і поступово збільшуй до 2–4 столових ложок. "
    "Спершу можливе легке здуття — це нормально, флора перебудовується. "
    "Найкраще вранці або за годину до сну.", styles['body'])]
story.append(make_card(inner, LIGHT_PURPLE))
story.append(Spacer(1, 10))

# Final note
story.append(HRFlowable(width="100%", thickness=1, color=PURPLE, spaceAfter=8))
story.append(Paragraph(
    "💜 <b>Порада від Анни:</b> reuteri — це не «просто пробіотик для кишківника», "
    "а системний регулятор гормонів, кісток, настрою, імунітету і шкіри. Особливо цінний "
    "для жінок у пери/менопаузі, після антибіотиків, при стресі й тривозі, "
    "та при підготовці до вагітності.",
    ParagraphStyle('fin', fontName=FONT, fontSize=10.5, leading=15, textColor=PURPLE_DARK)))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "Цей матеріал має освітній характер і не замінює індивідуальну консультацію лікаря.",
    styles['small']))

doc.build(story)
print("Saved: /home/user/Soloviova/Гайд_Пробіотик_Reuteri_WellnessCode.pdf")
