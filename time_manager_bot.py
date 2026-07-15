import asyncio
import datetime
import json
import logging
import os

from dotenv import load_dotenv
import anthropic
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import google_calendar as gcal

load_dotenv()

BOT_TOKEN = os.getenv('TIME_MANAGER_BOT_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
MODEL = 'claude-sonnet-5'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

OWNER_FILE = 'owner.json'
SENT_FILE = 'sent_reminders.json'

SYSTEM_PROMPT = """Ти — особистий тайм-менеджер Анни Соловйової, лікаря-дієтолога (проєкт Wellness-Код).
Ти ведеш її Google Календар: створюєш зустрічі та задачі, показуєш розклад.

Правила:
- Якщо це онлайн-зустріч із людиною — став add_meet=true, щоб створити посилання Google Meet.
- Якщо Анна дала email учасника — додай його в attendees, щоб він отримав запрошення.
- Якщо тривалість не вказана — став зустріч на 1 годину, задачу можна на 30 хвилин.
- Перед створенням, якщо бракує дати чи часу — коротко перепитай.
- Після дії коротко підтверди людською мовою (час, назва, посилання Meet якщо є).
- Мова: українська або російська — відповідай тією ж, якою пишуть.
"""

TOOLS = [
    {
        "name": "create_event",
        "description": "Створити подію (зустріч або задачу) в Google Календарі Анни.",
        "input_schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string", "description": "Назва події"},
                "start": {"type": "string", "description": "Початок у ISO 8601, напр. 2026-07-16T15:00:00 (локальний час)"},
                "end": {"type": "string", "description": "Кінець у ISO 8601. Якщо не вказано — +1 година"},
                "description": {"type": "string", "description": "Опис/нотатки"},
                "attendees": {"type": "array", "items": {"type": "string"}, "description": "Email учасників"},
                "add_meet": {"type": "boolean", "description": "true — створити посилання Google Meet"},
            },
            "required": ["summary", "start"],
        },
    },
    {
        "name": "list_events",
        "description": "Показати найближчі події з календаря Анни.",
        "input_schema": {
            "type": "object",
            "properties": {
                "days_ahead": {"type": "integer", "description": "На скільки днів вперед (за замовчуванням 7)"},
            },
        },
    },
]


# ---------- допоміжне збереження стану ----------

def _load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)


def get_owner_chat():
    env = os.getenv('OWNER_CHAT_ID')
    if env:
        return int(env)
    return _load_json(OWNER_FILE, {}).get('chat_id')


# ---------- виконання інструментів календаря ----------

def execute_tool(name, inp):
    try:
        if name == 'create_event':
            start = gcal.parse_dt(inp['start'])
            end = gcal.parse_dt(inp['end']) if inp.get('end') else None
            add_meet = inp.get('add_meet', bool(inp.get('attendees')))
            ev = gcal.create_event(
                summary=inp['summary'], start_dt=start, end_dt=end,
                description=inp.get('description', ''),
                attendees=inp.get('attendees'), add_meet=add_meet,
            )
            res = f"Створено подію «{inp['summary']}» на {start:%d.%m %H:%M}."
            if ev.get('hangoutLink'):
                res += f" Google Meet: {ev['hangoutLink']}"
            if ev.get('htmlLink'):
                res += f" Календар: {ev['htmlLink']}"
            return res
        if name == 'list_events':
            days = inp.get('days_ahead', 7)
            now = gcal.now_local()
            evs = gcal.list_events(now, now + datetime.timedelta(days=days))
            if not evs:
                return "Найближчих подій немає."
            lines = []
            for e in evs:
                s = e['start'].get('dateTime', e['start'].get('date'))
                dt = gcal.parse_dt(s)
                line = f"- {dt:%d.%m %H:%M} — {e.get('summary', '(без назви)')}"
                if e.get('hangoutLink'):
                    line += f" | Meet: {e['hangoutLink']}"
                lines.append(line)
            return "\n".join(lines)
    except Exception as ex:  # noqa: BLE001
        logger.exception("tool error")
        return f"Помилка при роботі з календарем: {ex}"
    return "Невідома дія."


def run_agent_sync(history):
    now_str = gcal.now_local().strftime('%A, %d.%m.%Y %H:%M')
    system = SYSTEM_PROMPT + f"\n\nПоточна дата і час ({gcal.TZ_NAME}): {now_str}."
    messages = list(history)
    for _ in range(6):
        resp = client.messages.create(
            model=MODEL, max_tokens=1500, system=system, tools=TOOLS, messages=messages,
        )
        if resp.stop_reason == 'tool_use':
            messages.append({"role": "assistant", "content": resp.content})
            results = []
            for block in resp.content:
                if block.type == 'tool_use':
                    out = execute_tool(block.name, block.input)
                    results.append({"type": "tool_result", "tool_use_id": block.id, "content": out})
            messages.append({"role": "user", "content": results})
            continue
        texts = [b.text for b in resp.content if b.type == 'text']
        return "\n".join(texts) if texts else "Готово."
    return "Забагато кроків — спробуй сформулювати простіше."


# ---------- напоминания ----------

async def check_reminders(context: ContextTypes.DEFAULT_TYPE):
    owner = get_owner_chat()
    if not owner:
        return
    now = gcal.now_local()
    try:
        evs = await asyncio.to_thread(gcal.list_events, now, now + datetime.timedelta(hours=25))
    except Exception:  # noqa: BLE001
        logger.exception("reminders: cannot read calendar")
        return
    sent = _load_json(SENT_FILE, {})
    changed = False
    for e in evs:
        s = e['start'].get('dateTime')
        if not s:
            continue  # подія на весь день — пропускаємо
        start = gcal.parse_dt(s)
        delta = (start - now).total_seconds()
        eid = e['id']
        title = e.get('summary', '(без назви)')
        meet = f"\nMeet: {e['hangoutLink']}" if e.get('hangoutLink') else ""
        if 5400 < delta <= 24 * 3600 and not sent.get(f"{eid}:day"):
            await context.bot.send_message(owner, f"⏰ Нагадування: {start:%d.%m о %H:%M} — «{title}».{meet}")
            sent[f"{eid}:day"] = True
            changed = True
        if 0 < delta <= 3600 and not sent.get(f"{eid}:hour"):
            await context.bot.send_message(owner, f"⏰ Через годину, о {start:%H:%M} — «{title}».{meet}")
            sent[f"{eid}:hour"] = True
            changed = True
    if changed:
        _save_json(SENT_FILE, sent)


# ---------- команди та повідомлення ----------

user_histories = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _save_json(OWNER_FILE, {'chat_id': update.effective_chat.id})
    user_histories[update.effective_user.id] = []
    await update.message.reply_text(
        "Привіт, Анно! Я твій тайм-менеджер \U0001f552\n\n"
        "Я веду твій Google Календар. Можеш просто написати, наприклад:\n"
        "• «Постав зустріч з клієнткою завтра о 15:00, онлайн»\n"
        "• «Що в мене на цьому тижні?»\n"
        "• «Додай задачу: подзвонити в лабораторію сьогодні о 12:00»\n\n"
        "Я нагадаю за день і за годину до кожної зустрічі. Команда /reset — почати заново."
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_histories[update.effective_user.id] = []
    await update.message.reply_text("Гаразд, почнемо заново!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    hist = user_histories.setdefault(uid, [])
    hist.append({"role": "user", "content": update.message.text})
    if len(hist) > 30:
        del hist[:-30]
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    reply = await asyncio.to_thread(run_agent_sync, hist)
    hist.append({"role": "assistant", "content": reply})
    await update.message.reply_text(reply, disable_web_page_preview=True)


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    # перевіряти нагадування кожні 5 хвилин
    app.job_queue.run_repeating(check_reminders, interval=300, first=15)
    app.run_polling()


if __name__ == '__main__':
    main()
