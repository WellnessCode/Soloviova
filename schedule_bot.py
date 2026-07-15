import logging
import os
import uuid
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)

load_dotenv()

BOT_TOKEN = os.getenv('SCHEDULE_BOT_TOKEN')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REFRESH_TOKEN = os.getenv('GOOGLE_REFRESH_TOKEN')
CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID', 'primary')

TIMEZONE = ZoneInfo('Europe/Kyiv')
WORK_START = time(10, 0)
WORK_END = time(18, 0)
SLOT_MINUTES = 60
DAYS_AHEAD = 7
MAX_SLOTS_SHOWN = 8

WEEKDAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд']

logging.basicConfig(level=logging.INFO)

# user_id -> list of (start, end) currently offered, so a button tap can be resolved
pending_slots = {}


def get_calendar_service():
    creds = Credentials(
        token=None,
        refresh_token=GOOGLE_REFRESH_TOKEN,
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        token_uri='https://oauth2.googleapis.com/token',
    )
    return build('calendar', 'v3', credentials=creds)


def format_slot(start):
    return f'{WEEKDAYS[start.weekday()]} {start.strftime("%d.%m")} {start.strftime("%H:%M")}'


def _overlaps(start, end, busy_ranges):
    return any(start < b_end and end > b_start for b_start, b_end in busy_ranges)


def find_free_slots():
    service = get_calendar_service()
    now = datetime.now(TIMEZONE)
    today = now.date()
    time_min = datetime.combine(today, time(0, 0), TIMEZONE)
    time_max = datetime.combine(today + timedelta(days=DAYS_AHEAD), time(0, 0), TIMEZONE)

    freebusy = service.freebusy().query(body={
        'timeMin': time_min.isoformat(),
        'timeMax': time_max.isoformat(),
        'timeZone': 'Europe/Kyiv',
        'items': [{'id': CALENDAR_ID}],
    }).execute()
    busy_ranges = [
        (datetime.fromisoformat(b['start']), datetime.fromisoformat(b['end']))
        for b in freebusy['calendars'][CALENDAR_ID]['busy']
    ]

    slots = []
    for d in range(DAYS_AHEAD):
        day = today + timedelta(days=d)
        if day.weekday() >= 5:
            continue
        slot_start = datetime.combine(day, WORK_START, TIMEZONE)
        day_end = datetime.combine(day, WORK_END, TIMEZONE)
        while slot_start + timedelta(minutes=SLOT_MINUTES) <= day_end:
            slot_end = slot_start + timedelta(minutes=SLOT_MINUTES)
            if slot_start > now and not _overlaps(slot_start, slot_end, busy_ranges):
                slots.append((slot_start, slot_end))
                if len(slots) >= MAX_SLOTS_SHOWN:
                    return slots
            slot_start = slot_end
    return slots


async def show_slots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    slots = find_free_slots()
    if not slots:
        await update.effective_message.reply_text(
            'На жаль, вільних вікон найближчим часом немає. Спробуй пізніше.'
        )
        return

    pending_slots[update.effective_user.id] = slots
    keyboard = [
        [InlineKeyboardButton(format_slot(start), callback_data=str(i))]
        for i, (start, _) in enumerate(slots)
    ]
    await update.effective_message.reply_text(
        'Привіт! Я Розклад — допоможу підібрати зручний час для зустрічі з Анною '
        'і одразу згенерую посилання на Google Meet.\n\n'
        'Обери вільне вікно:',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_slots(update, context)


async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    slots = pending_slots.get(user_id)
    if not slots:
        await query.edit_message_text('Ці вікна вже неактуальні, напиши /start ще раз.')
        return

    start_dt, end_dt = slots[int(query.data)]

    service = get_calendar_service()
    event = {
        'summary': f'Консультація з Анною ({query.from_user.full_name})',
        'description': f'Заброньовано через Telegram-бот Розклад. @{query.from_user.username or "без юзернейму"}',
        'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'Europe/Kyiv'},
        'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'Europe/Kyiv'},
        'conferenceData': {
            'createRequest': {
                'requestId': str(uuid.uuid4()),
                'conferenceSolutionKey': {'type': 'hangoutsMeet'},
            }
        },
    }
    created = service.events().insert(
        calendarId=CALENDAR_ID, body=event, conferenceDataVersion=1
    ).execute()
    meet_link = created.get('hangoutLink', 'посилання не вдалося згенерувати')

    await query.edit_message_text(
        f'Готово! Зустріч заплановано на {format_slot(start_dt)}.\n\n'
        f'Посилання на Google Meet:\n{meet_link}'
    )
    del pending_slots[user_id]


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('slots', show_slots))
    app.add_handler(CallbackQueryHandler(handle_choice))
    app.run_polling()


if __name__ == '__main__':
    main()
