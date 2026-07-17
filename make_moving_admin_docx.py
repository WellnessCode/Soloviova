from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PURPLE = RGBColor(0x7B, 0x52, 0xAB)
ORANGE = RGBColor(0xF0, 0x81, 0x1E)
GREEN = RGBColor(0x52, 0xAB, 0x7B)
DARK = RGBColor(0x2C, 0x2C, 0x2C)
GRAY = RGBColor(0x6B, 0x6B, 0x6B)
LIGHT_BG = "F5F0FA"

doc = Document()

for section in doc.sections:
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2)
    section.right_margin = Cm(2)

style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)


def shade_cell(cell, color_hex):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), color_hex)
    tc_pr.append(shd)


def add_heading(text, level=1, color=PURPLE):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.bold = True
    run.font.color.rgb = color
    if level == 1:
        run.font.size = Pt(20)
    elif level == 2:
        run.font.size = Pt(15)
    else:
        run.font.size = Pt(12)
    return p


def add_para(text, bold=False, color=DARK, size=11, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color
    run.font.size = Pt(size)
    return p


def add_bullet(text, color=DARK):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.font.color.rgb = color
    run.font.size = Pt(11)


def add_checkbox(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Cm(0.5)
    r1 = p.add_run("☐  ")
    r1.font.size = Pt(12)
    r2 = p.add_run(text)
    r2.font.size = Pt(11)
    r2.font.color.rgb = DARK


def divider():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run("─" * 60)
    run.font.color.rgb = PURPLE


# ============ COVER ============
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.space_before = Pt(80)
r = title.add_run("АДМІНШКАЛА")
r.bold = True
r.font.color.rgb = PURPLE
r.font.size = Pt(36)

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub.paragraph_format.space_after = Pt(20)
r = sub.add_run("Переїзд та облаштування")
r.bold = True
r.font.color.rgb = ORANGE
r.font.size = Pt(22)

date = doc.add_paragraph()
date.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = date.add_run("Дедлайн: 01.08.2026")
r.bold = True
r.font.color.rgb = GREEN
r.font.size = Pt(16)

doc.add_paragraph()
doc.add_paragraph()

# Goal card
tbl = doc.add_table(rows=1, cols=1)
tbl.autofit = False
tbl.columns[0].width = Cm(16)
cell = tbl.rows[0].cells[0]
cell.width = Cm(16)
shade_cell(cell, LIGHT_BG)
cp = cell.paragraphs[0]
r = cp.add_run("🎯 ГОЛОВНА ЦІЛЬ")
r.bold = True
r.font.size = Pt(13)
r.font.color.rgb = PURPLE
p = cell.add_paragraph()
p.add_run("Швидкий, легкий, комфортний і максимально бюджетний переїзд та облаштування у строк до 01.08.2026").font.size = Pt(11)

doc.add_paragraph()

tbl2 = doc.add_table(rows=1, cols=1)
tbl2.columns[0].width = Cm(16)
cell = tbl2.rows[0].cells[0]
shade_cell(cell, "FFF4E6")
cp = cell.paragraphs[0]
r = cp.add_run("✨ ІДЕАЛЬНА КАРТИНА")
r.bold = True
r.font.size = Pt(13)
r.font.color.rgb = ORANGE
p = cell.add_paragraph()
p.add_run(
    "1 серпня ввечері я сплю у своєму ліжку у новій квартирі з облаштованою спальнею, "
    "працюючою кухнею і туалетом. Всі старі речі вивезені, всі борги закриті, "
    "адреса змінена. Спокій, чистота, порядок. Витрати — в межах бюджету."
).font.size = Pt(11)

doc.add_page_break()

# ============ CONTENT ============
add_heading("📋 8 ЦІЛЕЙ ЗА ПРІОРИТЕТОМ", 1, PURPLE)
divider()

# CEL 1
add_heading("1️⃣  Затвердити дату передачі ключів 31.07", 2, PURPLE)
add_para("Ідеальна картина:", bold=True, color=ORANGE)
add_para("У руках підписаний договір з чіткою датою і часом передачі ключів 31.07.")
add_para("Програма:", bold=True, color=GREEN)
add_checkbox("Зв'язатися з орендодавцем / агентом до 20.07 — підтвердити дату і час")
add_checkbox("Отримати письмове підтвердження (SMS / email) — до 22.07")
add_checkbox("Уточнити: хто передає, де підписуємо акт, чи потрібен депозит наперед")
add_checkbox("Внести в календар точний час 31.07")
add_checkbox("За 2 дні (29.07) — нагадати орендодавцю")
add_para("Дедлайн: 22.07 — підтвердження на руках", bold=True, color=PURPLE)
divider()

# CEL 2
add_heading("2️⃣  Переїзд 01.08: організувати машину", 2, PURPLE)
add_para("Ідеальна картина:", bold=True, color=ORANGE)
add_para("01.08 о 10:00 машина стоїть біля під'їзду, речі упаковані, за 3 години все у новій квартирі.")
add_para("Програма:", bold=True, color=GREEN)
add_checkbox("Оцінити обсяг речей (скільки коробок, меблів) — до 20.07")
add_checkbox("Визначити тип транспорту: van / вантажне таксі / переїзна компанія")
add_checkbox("Отримати 3 котирування (GoMore, Jem&Fix van, Facebook Marketplace, укр. чати)")
add_checkbox("Забронювати транспорт на 01.08 о 10:00 — до 25.07")
add_checkbox("Домовитися про 1–2 помічників для завантаження")
add_checkbox("Купити 20–30 коробок + скотч + маркер + бульбашкову плівку — до 22.07")
add_checkbox("За 3 дні до переїзду (29.07) — підтвердити з перевізником")
add_para("Дедлайн: 25.07 · Бюджет: 800–2000 крон", bold=True, color=PURPLE)
divider()

# CEL 3
add_heading("3️⃣  Зібрати та упакувати речі до 30.07", 2, PURPLE)
add_para("Ідеальна картина:", bold=True, color=ORANGE)
add_para("30.07 увечері всі речі в підписаних коробках, стоять у коридорі.")
add_para("Тиждень 1 (14.07–20.07) — підготовка:", bold=True, color=GREEN)
add_checkbox("Купити коробки, скотч, маркери, пакети для сміття")
add_checkbox("Роздрукувати наліпки «КУХНЯ / СПАЛЬНЯ / ВАННА / ГАРДЕРОБ / КАБІНЕТ»")
add_para("Тиждень 2 (21.07–27.07) — пакуємо все, крім щоденного:", bold=True, color=GREEN)
add_checkbox("Шафи / гардероб — сезонний одяг, взуття")
add_checkbox("Книги, документи, папки")
add_checkbox("Декор, картини, дрібниці")
add_checkbox("Посуд, крім щоденного")
add_checkbox("Побутова техніка, крім чайника/мікрохвильовки")
add_para("28.07–30.07 — пакуємо щоденне:", bold=True, color=GREEN)
add_checkbox("Одяг на найближчі 2 дні — окремо")
add_checkbox("Косметика, зубні щітки, ліки — в коробку «ПЕРШИЙ ДЕНЬ»")
add_checkbox("Постіль, рушники — окремо")
add_checkbox("Зарядки, документи, гроші — сумка «З СОБОЮ»")
add_para("Правило:", bold=True, color=ORANGE)
add_para("Підписуй кожну коробку з двох сторін + що всередині + куди в новій квартирі.", italic=True)
add_para("Дедлайн: 30.07 22:00", bold=True, color=PURPLE)
divider()

# CEL 4
add_heading("4️⃣  Викинути / роздати непотрібні речі", 2, PURPLE)
add_para("Ідеальна картина:", bold=True, color=ORANGE)
add_para("Мінус 20–30% речей. Тільки те, що потрібне і подобається.")
add_para("Правило «3 коробок»:", bold=True, color=GREEN)
add_bullet("🟢 ЛИШАЮ — використовую регулярно, люблю", GREEN)
add_bullet("🟡 ВІДДАТИ / ПРОДАТИ — хороший стан, не потрібне", ORANGE)
add_bullet("🔴 ВИКИНУТИ — зламане, старе", RGBColor(0xC0, 0x39, 0x2B))
add_para("Продати:", bold=True, color=GREEN)
add_bullet("DBA.dk (данський Avito) — меблі, техніка, одяг")
add_bullet("Facebook Marketplace — швидко")
add_bullet("Trendsales / Reshopper — одяг")
add_para("Віддати безкоштовно:", bold=True, color=GREEN)
add_bullet("Genbrug / Røde Kors / Kirkens Korshær")
add_bullet("Facebook «Ukrainere i Esbjerg»")
add_bullet("Facebook «Free / Bytte i Esbjerg»")
add_para("Викинути:", bold=True, color=GREEN)
add_bullet("Genbrugsplads Esbjerg (Måde) — безкоштовно за пропискою")
add_bullet("Storskrald — заявка на велике сміття біля будинку")
add_para("Дедлайн: 27.07 · Прибуток від продажу: 500–3000 крон", bold=True, color=PURPLE)
divider()

# CEL 5 — DEBTS
add_heading("5️⃣  Віддати борги за квартиру", 2, PURPLE)
add_para("Ідеальна картина:", bold=True, color=ORANGE)
add_para("Всі 4 борги закриті у строк. Кожен отримав підтвердження перекладу.")

tbl = doc.add_table(rows=6, cols=6)
tbl.style = 'Light Grid Accent 4'
tbl.autofit = True
headers = ["Дата", "Кому", "Сума DKK", "Сума EUR", "Спосіб", "☐"]
for i, h in enumerate(headers):
    cell = tbl.rows[0].cells[i]
    shade_cell(cell, "7B52AB")
    for p in cell.paragraphs:
        for r in p.runs:
            r.text = ""
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(11)

rows_data = [
    ["до 22.07", "Андерсен", "25 000", "3 400", "Банк / MobilePay", "☐"],
    ["до 23.07", "Соломко Володимир", "10 000", "1 340", "MobilePay", "☐"],
    ["до 31.07", "Галас Віктор", "10 000", "1 340", "MobilePay", "☐"],
    ["до 15.08", "Возна Тетяна", "—", "1 200", "Bank / Wise", "☐"],
    ["РАЗОМ", "", "45 000", "≈ 7 280", "", ""],
]
for i, row in enumerate(rows_data, start=1):
    for j, val in enumerate(row):
        cell = tbl.rows[i].cells[j]
        cell.text = ""
        p = cell.paragraphs[0]
        r = p.add_run(val)
        r.font.size = Pt(10)
        if i == 5:
            r.bold = True
            r.font.color.rgb = PURPLE
            shade_cell(cell, LIGHT_BG)

add_para("Програма:", bold=True, color=GREEN)
add_checkbox("15.07 — перевірити баланси на рахунках, порахувати звідки бере кожен транш")
add_checkbox("16.07 — якщо не вистачає: продати щось / відстрочка / позика")
add_checkbox("20.07 — переказати Андерсен 25 000 крон (квитанція!)")
add_checkbox("22.07 — переказати Соломко 10 000 крон + «долг за квартиру закрит»")
add_checkbox("30.07 — переказати Галасу 10 000 крон")
add_checkbox("10.08 — переказати Возній 1 200 євро")
add_checkbox("Створити файл «Долги.xlsx» (Кому/Сума/Дата план/Дата факт/Квитанція)")
add_para("Правило:", bold=True, color=ORANGE)
add_para("Одразу після переказу — скріншот у папку «Квитанції_переїзд».", italic=True)
divider()

# CEL 6
add_heading("6️⃣  Купити ліжка та постіль", 2, PURPLE)
add_para("Ідеальна картина:", bold=True, color=ORANGE)
add_para("01.08 увечері у спальні стоїть зібране ліжко з новим матрацом, свіжою постіллю. Можна лягти і виспатися.")
add_para("Список:", bold=True, color=GREEN)
add_bullet("Ліжко з рамою (або box spring)")
add_bullet("Матрац (правильна жорсткість)")
add_bullet("2 подушки")
add_bullet("Ковдра (літня + зимова)")
add_bullet("2 комплекти постільної білизни")
add_bullet("Наматрацник (обов'язково!)")
add_para("Де купувати:", bold=True, color=GREEN)
add_bullet("🟢 IKEA / JYSK / DBA (б/у рами) — до 3 000 крон")
add_bullet("🟡 IKEA + AGOTNES матрац + PUDDERVIVA — 5 000–10 000 крон")
add_bullet("🔴 JYSK Elite / Ilva / BoConcept — 15 000+")
add_para("Моя рекомендація (бюджет ~5 100 крон / 690 €):", bold=True, color=ORANGE)
add_bullet("Рама IKEA MALM 180×200 — 1 300 крон")
add_bullet("Матрац IKEA AGOTNES середньої жорсткості — 2 500 крон")
add_bullet("2 подушки IKEA — 200 крон")
add_bullet("Ковдра — 400 крон")
add_bullet("2 комплекти постелі — 500 крон")
add_bullet("Наматрацник — 200 крон")
add_para("Дедлайн замовлення: 25.07 · Збірка: 01.08 20:00", bold=True, color=PURPLE)
divider()

# CEL 7
add_heading("7️⃣  Купити все для облаштування квартири", 2, PURPLE)
add_para("Ідеальна картина:", bold=True, color=ORANGE)
add_para("Кухня функціонує, ванна укомплектована, є де сісти і поїсти.")
add_para("🔴 КРИТИЧНО (в перший день):", bold=True, color=RGBColor(0xC0, 0x39, 0x2B))
for x in [
    "Туалетний папір + миючі засоби",
    "Мило, зубна щітка/паста",
    "Рушники",
    "Постільна білизна",
    "Чайник",
    "Каструля + сковорідка",
    "Тарілка / кухоль / виделка / ложка (на кожного)",
    "Штори або тимчасові жалюзі",
]:
    add_checkbox(x)
add_para("🟡 ВАЖЛИВО (перший тиждень):", bold=True, color=ORANGE)
for x in [
    "Стіл + стільці (кухня)",
    "Дивани або крісла (вітальня)",
    "Люстри / світло",
    "Килимки у ванну / біля ліжка",
    "Пилосос",
    "Праска + дошка",
    "Кошики для сміття",
    "Сушарка для посуду",
    "Штори повноцінні",
]:
    add_checkbox(x)
add_para("🟢 БАЖАНО (протягом місяця):", bold=True, color=GREEN)
for x in [
    "Декор, картини, рослини",
    "Додаткові шафи / стелажі",
    "Килими",
    "Дзеркала",
]:
    add_checkbox(x)
add_para("Де купувати бюджетно:", bold=True, color=GREEN)
add_bullet("IKEA — базове")
add_bullet("Bilka, Rema1000, Netto — миючі, посуд")
add_bullet("JYSK — текстиль, штори, декор")
add_bullet("Jem & Fix — інструменти")
add_bullet("DBA / Facebook Marketplace — меблі б/у (-60–80%)")
add_bullet("Genbrug — посуд, декор за 5–20 крон")
add_para("Правило: купуй ТІЛЬКИ по списку. Не заходь у IKEA без списку.", bold=True, color=ORANGE, italic=True)
add_para("Бюджет: 5 000–10 000 крон (крім ліжка)", bold=True, color=PURPLE)
divider()

# CEL 8
add_heading("8️⃣  Змінити адресу реєстрації", 2, PURPLE)
add_para("Ідеальна картина:", bold=True, color=ORANGE)
add_para("У Borger.dk нова адреса, всі установи повідомлені, пошта приходить на нову адресу.")
add_para("01.08–05.08:", bold=True, color=GREEN)
add_checkbox("Borger.dk → Flytning — подати заявку (обов'язково в 5-денний термін!)")
add_checkbox("Отримати підтвердження на e-Boks")
add_para("05.08–15.08 — повідомити:", bold=True, color=GREEN)
add_checkbox("SKAT (автоматично, але перевір)")
add_checkbox("Банк (Lunar, Danske Bank та ін.)")
add_checkbox("Робота / роботодавець — HR")
add_checkbox("Kommune (якщо є виплати)")
add_checkbox("Лікар (egen læge)")
add_checkbox("Страхова компанія (Alka, Tryg, Topdanmark)")
add_checkbox("Amazon, IKEA, інтернет-магазини")
add_checkbox("Netflix, Spotify, підписки")
add_checkbox("Дитячий садок / школа")
add_checkbox("Українське консульство (якщо є реєстрація)")
add_para("Пошта:", bold=True, color=GREEN)
add_checkbox("PostNord — переадресація на 3 місяці (150 крон)")
add_para("Дедлайн Borger.dk: 05.08 (штрафи!) · Дедлайн повідомлень: 15.08", bold=True, color=PURPLE)

doc.add_page_break()

# ============ TIMELINE ============
add_heading("📅 КАЛЕНДАРНИЙ ПЛАН (Timeline)", 1, PURPLE)
divider()

add_heading("Тиждень 1 (14.07–20.07) — ПІДГОТОВКА", 3, GREEN)
add_bullet("Затвердити дату передачі ключів")
add_bullet("Купити коробки і матеріали")
add_bullet("Оцінити обсяг → замовити машину")
add_bullet("Виміряти нову квартиру → список меблів")
add_bullet("Почати сортувати речі (3 коробки)")
add_bullet("💰 Виплата: Андерсен 25 000 DKK", ORANGE)

add_heading("Тиждень 2 (21.07–27.07) — ПАКУВАННЯ + БОРГИ", 3, GREEN)
add_bullet("Упакувати все, крім щоденного")
add_bullet("Продати / роздати непотрібне")
add_bullet("Замовити машину на 01.08")
add_bullet("Замовити ліжко + матрац")
add_bullet("💰 Виплата: Соломко 10 000 DKK", ORANGE)
add_bullet("Купити критичне (посуд, туалетний папір)")

add_heading("Тиждень 3 (28.07–03.08) — ПЕРЕЇЗД 🚚", 3, GREEN)
add_bullet("28.07 — фінальне пакування")
add_bullet("29.07 — вивіз storskrald")
add_bullet("30.07 — все упаковано, підтвердити машину")
add_bullet("31.07 — передача ключів")
add_bullet("01.08 — ПЕРЕЇЗД. Ліжко зібрати першим!", PURPLE)
add_bullet("02.08 — розпакувати кухню і ванну")
add_bullet("03.08 — розпакувати решту")
add_bullet("💰 Виплата: Галас 10 000 DKK", ORANGE)

add_heading("Тиждень 4 (04.08–10.08) — ОБЛАШТУВАННЯ", 3, GREEN)
add_bullet("05.08 — подати зміну адреси в Borger.dk", PURPLE)
add_bullet("Купити важливе (стіл, стільці, штори, пилосос)")
add_bullet("Повідомити всі установи")
add_bullet("Замовити переадресацію пошти")

add_heading("Тиждень 5 (11.08–17.08) — ФІНАЛ", 3, GREEN)
add_bullet("Докупити бажане")
add_bullet("Декор, дрібниці")
add_bullet("💰 Виплата: Возна 1 200 EUR", ORANGE)
add_bullet("Внутрішня перевірка: чи все закрито?")

doc.add_page_break()

# ============ BUDGET ============
add_heading("💰 ЗАГАЛЬНИЙ БЮДЖЕТ", 1, PURPLE)
divider()

tbl = doc.add_table(rows=11, cols=3)
tbl.style = 'Light Grid Accent 4'
headers = ["Стаття", "Сума DKK", "Сума EUR"]
for i, h in enumerate(headers):
    cell = tbl.rows[0].cells[i]
    shade_cell(cell, "7B52AB")
    cell.text = ""
    r = cell.paragraphs[0].add_run(h)
    r.bold = True
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    r.font.size = Pt(11)

budget_data = [
    ["Борги (Андерсен + Соломко + Галас)", "45 000", "6 080"],
    ["Возна", "—", "1 200"],
    ["Транспорт", "1 500", "200"],
    ["Пакування", "500", "70"],
    ["Ліжко + постіль", "5 100", "690"],
    ["Облаштування критичне", "3 000", "400"],
    ["Облаштування важливе", "5 000", "670"],
    ["Переадресація пошти", "150", "20"],
    ["Мінус від продажу непотрібного", "−2 000", "−270"],
    ["РАЗОМ", "≈ 58 000 DKK + 1 200 EUR", "≈ 9 070 EUR"],
]
for i, row in enumerate(budget_data, start=1):
    for j, val in enumerate(row):
        cell = tbl.rows[i].cells[j]
        cell.text = ""
        r = cell.paragraphs[0].add_run(val)
        r.font.size = Pt(10)
        if i == len(budget_data):
            r.bold = True
            r.font.color.rgb = PURPLE
            shade_cell(cell, LIGHT_BG)

doc.add_page_break()

# ============ FINAL CHECKLIST ============
add_heading("✅ ФІНАЛЬНИЙ ЧЕК-ЛИСТ УСПІХУ 01.08 УВЕЧЕРІ", 1, PURPLE)
divider()

for x in [
    "Ключі від нової квартири на руках",
    "Всі речі в новій квартирі",
    "Стара квартира здана в належному стані",
    "Ліжко зібране, постіль постелена",
    "Кухня функціонує (чайник + посуд)",
    "Ванна укомплектована",
    "Борги 1–3 закриті",
    "Транспорт оплачено",
    "Ти виспалася 🙂",
]:
    add_checkbox(x)

divider()
add_heading("🎯 ПРАВИЛА, ЯКІ ЗЕКОНОМЛЯТЬ ЧАС І ГРОШІ", 2, ORANGE)
rules = [
    "Не купуй нове, поки не оглянула Genbrug і DBA",
    "Не купуй усе за раз — прожити тиждень, зрозуміти, чого справді бракує",
    "Не заходь у IKEA без списку",
    "Пакуй кожну кімнату окремо, підписуй коробки двічі",
    "Коробка «ПЕРШИЙ ДЕНЬ» — окремо (чайник, зубна щітка, ТП)",
    "Фотографуй речі перед пакуванням",
    "Всі квитанції в одну папку",
    "Не бери гроші в борг для облаштування — купуй поступово",
    "Проси допомоги — знайомі раді допомогти, якщо запросиш заздалегідь",
]
for i, r_txt in enumerate(rules, start=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    r1 = p.add_run(f"{i}. ")
    r1.bold = True
    r1.font.color.rgb = PURPLE
    r1.font.size = Pt(11)
    r2 = p.add_run(r_txt)
    r2.font.size = Pt(11)
    r2.font.color.rgb = DARK

doc.add_paragraph()
divider()
end = doc.add_paragraph()
end.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = end.add_run("💜 Ти впораєшся. Крок за кроком.")
r.bold = True
r.italic = True
r.font.color.rgb = PURPLE
r.font.size = Pt(14)

output = "/home/user/Soloviova/Адміншкала_Переїзд_01.08.docx"
doc.save(output)
print(f"Saved: {output}")
