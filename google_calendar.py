"""Модуль роботи з Google Календарем: створення подій (з Google Meet) і перегляд."""
import os
import json
import datetime
from zoneinfo import ZoneInfo

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID', 'primary')
TZ_NAME = os.getenv('TZ_NAME', 'Europe/Kyiv')
TZ = ZoneInfo(TZ_NAME)


def now_local():
    """Поточний час у локальному часовому поясі."""
    return datetime.datetime.now(TZ)


def parse_dt(value):
    """Парсить ISO-рядок у datetime. Наївний час вважається локальним."""
    if len(value) == 10:  # тільки дата (подія на весь день)
        d = datetime.date.fromisoformat(value)
        return datetime.datetime(d.year, d.month, d.day, tzinfo=TZ)
    dt = datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=TZ)
    return dt


def _credentials():
    info = None
    token_json = os.getenv('GOOGLE_TOKEN_JSON')
    if token_json:
        info = json.loads(token_json)
    elif os.path.exists('token.json'):
        with open('token.json') as f:
            info = json.load(f)
    if not info:
        raise RuntimeError(
            "Google Календар не налаштовано: немає GOOGLE_TOKEN_JSON. "
            "Запусти auth_google.py один раз (див. SETUP_GOOGLE.md)."
        )
    creds = Credentials.from_authorized_user_info(info, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds


def _service():
    return build('calendar', 'v3', credentials=_credentials(), cache_discovery=False)


def create_event(summary, start_dt, end_dt=None, description='', attendees=None, add_meet=False):
    """Створює подію. Якщо add_meet=True — додає посилання Google Meet.
    Якщо вказано attendees (email) — надсилає їм запрошення."""
    if end_dt is None:
        end_dt = start_dt + datetime.timedelta(hours=1)
    body = {
        'summary': summary,
        'description': description or '',
        'start': {'dateTime': start_dt.replace(microsecond=0).isoformat(), 'timeZone': TZ_NAME},
        'end': {'dateTime': end_dt.replace(microsecond=0).isoformat(), 'timeZone': TZ_NAME},
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 60},
            ],
        },
    }
    if attendees:
        body['attendees'] = [{'email': e} for e in attendees]
    params = {'calendarId': CALENDAR_ID, 'body': body, 'sendUpdates': 'all'}
    if add_meet:
        body['conferenceData'] = {
            'createRequest': {
                'requestId': f"meet-{int(start_dt.timestamp())}",
                'conferenceSolutionKey': {'type': 'hangoutsMeet'},
            }
        }
        params['conferenceDataVersion'] = 1
    return _service().events().insert(**params).execute()


def list_events(time_min=None, time_max=None, max_results=25):
    """Повертає список подій у заданому діапазоні (за замовчуванням — від зараз)."""
    if time_min is None:
        time_min = now_local()
    params = {
        'calendarId': CALENDAR_ID,
        'timeMin': time_min.isoformat(),
        'singleEvents': True,
        'orderBy': 'startTime',
        'maxResults': max_results,
    }
    if time_max is not None:
        params['timeMax'] = time_max.isoformat()
    return _service().events().list(**params).execute().get('items', [])
