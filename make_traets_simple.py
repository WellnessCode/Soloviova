from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

for section in doc.sections:
    section.top_margin    = Pt(60)
    section.bottom_margin = Pt(60)
    section.left_margin   = Pt(72)
    section.right_margin  = Pt(72)

def para(text='', bold=False, italic=False, size=11, align=None, color=None, space_before=0, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    if align:
        p.alignment = align
    if text:
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.size = Pt(size)
        run.font.name = 'Arial'
        if color:
            run.font.color.rgb = RGBColor(*color)
    return p

def highlight_heading(text, hex_color='F4B942'):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(6)
    run = p.add_run(text)
    run.bold = True
    run.italic = True
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    rPr = run._r.get_or_add_rPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    rPr.append(shd)
    return p

def sys_title(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(3)
    run = p.add_run(text.upper())
    run.bold = True
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    return p

def bullet(text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(3)
    r = p.add_run(text)
    r.font.size = Pt(11)
    r.font.name = 'Arial'
    return p

# ── Заголовок ──
para('Заключение по тестированию', bold=True, size=14,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
para('13.06.2026', size=11, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=6)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(4)
r = p.add_run('Traets Magdalena, 12.05.1962')
r.bold = True; r.font.size = Pt(11); r.font.name = 'Arial'
para('Биологический возраст — 69 лет', italic=True, size=11, space_after=12)

# ── Раздел ──
highlight_heading('Что происходит в организме:')

# ── Нервная система ──
sys_title('Нервная система и самочувствие')
bullet('Нервная система истощена — быстрая утомляемость, сложно восстановиться после нагрузок')
bullet('Вегетативная нервная система работает нестабильно — возможны перепады давления, самочувствия, температуры тела')
bullet('Снижен мелатонин — возможны нарушения сна и трудности с засыпанием')

# ── Позвоночник и суставы ──
sys_title('Позвоночник и суставы')
bullet('Два верхних позвонка в шее смещены — пережимают сосуды и нервы. Это может вызывать головные боли, головокружение, онемение рук, ухудшение слуха и зрения')
bullet('Позвоночник изношен — диски истончены и испытывают повышенную нагрузку')
bullet('Таз стоит неровно, сустав между крестцом и тазовой костью работает неправильно')
bullet('Свод стопы уплощён — плоскостопие')
bullet('Суставы изношены — хрящ постепенно истончается')

# ── Сердце и сосуды ──
sys_title('Сердце и сосуды')
bullet('На стенках сосудов оседают жировые отложения — сосуды постепенно сужаются')
bullet('Вены на ногах начинают расширяться')
bullet('Расширение вен в области прямой кишки')

# ── Живот и пищеварение ──
sys_title('Живот и пищеварение')
bullet('В кишечнике избыточное количество бактерий — возможно вздутие, дискомфорт и нарушение всасывания питательных веществ')
bullet('Организм плохо перерабатывает сахар — уровень глюкозы может повышаться')
bullet('Желчь вытекает медленно и плохо выводится — застой желчи, риск образования камней')
bullet('Поджелудочная железа работает с перегрузкой и раздражена')

# ── Гормоны ──
sys_title('Гормоны и обмен веществ')
bullet('Щитовидная железа работает нестабильно')
bullet('Возможно, иммунная система воздействует на щитовидную железу (требует дополнительной проверки у врача)')
bullet('Надпочечники вырабатывают гормон стресса в недостаточном или нестабильном количестве')

# ── Зубы ──
sys_title('Зубы и дёсны')
bullet('Дёсны воспалены, ткань вокруг зубов постепенно разрушается')

# ── Глаза ──
sys_title('Глаза')
bullet('Боковое зрение справа снижено')
bullet('Трудно видеть вблизи — возрастное изменение зрения')

# ── Инфекции ──
sys_title('Инфекции')
bullet('В организме активны вирусы герпеса нескольких типов (1, 3 и 7)')
bullet('Обнаружен вирус папилломы человека')
bullet('В организме присутствуют паразиты')

# ── Дефициты ──
sys_title('Чего не хватает организму')
bullet('Не хватает витаминов: A, D, PP (B3), B2, B5, B6')
bullet('Не хватает строительного материала для клеток — аминокислот: аспарагин, глютамин, глицин, пролин, таурин, цитрулин, ГАМК, орнитин, карнитин, глутатион, лейцин, треонин, фенилаланин')

# ── Непереносимости ──
sys_title('Что плохо переносит организм')
bullet('Плохо реагирует на: бобовые, орехи, рыбу жирных сортов, сладкое и сахар, дрожжи, искусственные красители')
bullet('Чувствительность к запахам: парфюмерия, химические вещества, летучие соединения')

# ── Подвал ──
doc.add_paragraph()
for line in [
    'С заботой и верой в Вас,',
    'ваш Health-coach Anna Soloviova',
    'и команда проекта WELLNESS CODE by Anna Soloviova',
]:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(line)
    run.italic = True
    run.font.size = Pt(11)
    run.font.name = 'Arial'
    run.font.color.rgb = RGBColor(0x2E, 0x74, 0xB5)

doc.save('/home/user/Soloviova/Traets_Magdalena_zak_simple.docx')
print('Done')
