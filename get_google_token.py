"""
Одноразовий скрипт: отримати GOOGLE_REFRESH_TOKEN для schedule_bot.py.

1. У Google Cloud Console створи OAuth Client ID (тип "Desktop app"),
   увімкни Google Calendar API, і поклади client_id / client_secret в .env
   як GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET.
2. Запусти цей скрипт локально (де є браузер), увійди під акаунтом Анни
   і дозволь доступ до календаря.
3. Скрипт виведе GOOGLE_REFRESH_TOKEN — додай його в .env поруч з іншими
   змінними для schedule_bot.py.
"""
import os

from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_config(
    {
        'installed': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'redirect_uris': ['http://localhost'],
        }
    },
    SCOPES,
)

creds = flow.run_local_server(port=0)
print('\nGOOGLE_REFRESH_TOKEN=' + creds.refresh_token)
