from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# Margins
for section in doc.sections:
    section.top_margin    = Pt(60)
    section.bottom_margin = Pt(60)
    section.left_margin   = Pt(72)
    section.right_margin  = Pt(72)

def add_paragraph(text='', bold=False, italic=False, size=12, align=None, color=None, space_before=0, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    if align:
        p.alignment = align
    if text:
        run = p.add_run(text)
        run.bold   = bold
        run.italic = italic
        run.font.size = Pt(size)
        if color:
            run.font.color.rgb = RGBColor(*color)
    return p

def add_highlighted_heading(text, hex_color='F4B942'):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(4)
    run = p.add_run(text)
    run.bold   = True
    run.italic = True
    run.font.size = Pt(12)
    # highlight via shading the run
    rPr = run._r.get_or_add_rPr()
    highlight = OxmlElement('w:highlight')
    # map hex to word highlight name
    colors = {
        'F4B942': 'yellow',
        'A8D08D': 'green',
    }
    highlight.set(qn('w:val'), colors.get(hex_color, 'yellow'))
    rPr.append(highlight)
    return p

def add_system_title(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(text.upper())
    run.bold = True
    run.font.size = Pt(12)
    return p

def add_bullet(bold_text, normal_text='', italic_note=''):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(3)
    r1 = p.add_run(bold_text)
    r1.bold = True
    r1.font.size = Pt(11)
    if normal_text:
        r2 = p.add_run(normal_text)
        r2.font.size = Pt(11)
    if italic_note:
        r3 = p.add_run(italic_note)
        r3.italic = True
        r3.font.size = Pt(11)
    return p

# ── Title ──
add_paragraph('Заключение по тестированию', bold=True, size=14,
              align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)

# ── Date ──
add_paragraph('06.06.2026', size=12,
              align=WD_ALIGN_PARAGRAPH.RIGHT, space_before=0, space_after=10)

# ── Patient info ──
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(16)
r = p.add_run('Лобель Илана, 19.12.1947')
r.bold = True
r.font.size = Pt(12)
p.add_run('\n+972543939238').font.size = Pt(12)

# ── Section header ──
add_highlighted_heading('Выявленные нарушения:', 'F4B942')

# ── Нервная система ──
add_system_title('Нервная система')
add_bullet('Напряжение нервной системы 1-й степени')
add_bullet('Признаки снижения уровня мелатонина')

# ── Опорно-двигательный аппарат ──
add_system_title('Опорно-двигательный аппарат')
add_bullet('Защемление позвоночных артерий на уровне Ц1, Ц2 со склонностью к скачкам артериального давления')
add_bullet('Признаки грыжи в поясничном отделе позвоночника')
add_bullet('Признаки выраженного остеохондроза')
add_bullet('Признаки смещения межпозвоночных дисков')
add_bullet('Признаки кифоза в шейном и грудном отделе позвоночника')
add_bullet('Признаки нарушения осанки')
add_bullet('Признаки изменения свода стопы')
add_bullet('Признаки воспаления мелких суставов', italic_note=' (подагра — под вопросом)')
add_bullet('Остеопороз')

# ── Сердечно-сосудистая система ──
add_system_title('Сердечно-сосудистая система')
add_bullet('Миокардиосклероз')
add_bullet('Признаки атеросклероза')
add_bullet('Признаки липидемии')
add_bullet('Признаки склонности к повышению артериального давления и тахикардии')

# ── Пищеварительная система ──
add_system_title('Пищеварительная система')
add_bullet('Признаки жировой инфильтрации печени')
add_bullet('Признаки хронического холецистита со склонностью к камнеобразованию')
add_bullet('Признаки сужения желчевыводящих путей по гипокинетическому типу')
add_bullet('Признаки недостаточности пищеварения')
add_bullet('Признаки избыточного процесса брожения в толстом кишечнике')
add_bullet('Признаки изменения кислотности желудочного сока')

# ── Эндокринная и репродуктивная система ──
add_system_title('Эндокринная и репродуктивная система')
add_bullet('Признаки выраженных климактерических изменений в яичниках')
add_bullet('Выраженная гипоэстрогенемия')
add_bullet('Признаки нарушения глюкокортикоидной функции яичников')
add_bullet('Признаки нарушения обмена веществ')

# ── Мочевыделительная система ──
add_system_title('Мочевыделительная система')
add_bullet('Признаки нарушения сократительной функции / тонуса мочевого пузыря')

# ── Органы зрения ──
add_system_title('Органы зрения')
add_bullet('Признаки снижения остроты зрения, повышения внутриглазного давления, помутнения хрусталика правого глаза')

# ── Иммунная система и инфекции ──
add_system_title('Иммунная система и инфекции')
add_bullet('Признаки изменений лимфатических узлов средостения')
add_bullet('Признаки изменений селезёнки', italic_note=' (негемолитический тип — под вопросом)')
add_bullet('Признаки изменений бронхов, миндалин и носовых ходов')
add_bullet('Признаки хронического тонзиллита')
add_bullet('Папилломавирус')
add_bullet('Герпес 2-го, 3-го, 7-го типа')
add_bullet('Паразитоз')

# ── Дефициты питательных веществ ──
add_system_title('Дефициты питательных веществ')
add_bullet('Признаки глубокого дефицита всех витаминов')
add_bullet('Признаки дефицита витамина D')
add_bullet('Признаки дефицита кальция')
add_bullet('Признаки дефицита минералов')
add_bullet('Признаки дефицита аминокислот: ', 'цистина, глицина, карнитина, глутаминовой кислоты, таурина, лизина, триптофана, фенилаланина')
add_bullet('Признаки интоксикации микотоксинами')

# ── Пищевая непереносимость ──
add_system_title('Пищевая непереносимость')
add_bullet('Признаки непереносимости: ', 'дрожжей, риса, глютена, злаковых, домашней пыли, кофе, чая, шоколада и какао')
add_bullet('Непереносимость листовых и зелёных овощей и фруктов')

# ── Footer ──
doc.add_paragraph()
for line in [
    'Поздравляю!',
    'Благодарю за доверие.',
    '',
    'Я рада приветствовать Вас на Вашей программе коррекции веса и здоровья.',
    '',
    'Моя цель — помочь Вам справиться с Вашей проблемой и научиться осознанно управлять своим здоровьем.',
    '',
    'С заботой и верой в Вас, ваш Health-coach Anna Soloviova и команда проекта WELLNESS CODE by Anna Soloviova',
]:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(line)
    run.italic = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0x2E, 0x74, 0xB5)

doc.save('/home/user/Soloviova/Lobel_Ilana_zak.docx')
print('Done')
