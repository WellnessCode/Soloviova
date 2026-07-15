"""Разовий скрипт авторизації Google Календаря.

Запусти ОДИН РАЗ на своєму комп'ютері:
    1) поклади поруч файл credentials.json (OAuth-ключ з Google Cloud, див. SETUP_GOOGLE.md)
    2) виконай:  python auth_google.py
    3) у браузері дозволь доступ до календаря
    4) з'явиться файл token.json — скопіюй ВЕСЬ його вміст
       у змінну GOOGLE_TOKEN_JSON на Railway.
"""
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/calendar']

if __name__ == '__main__':
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as f:
        f.write(creds.to_json())
    print("\n✅ Готово! Створено token.json")
    print("Скопіюй ВЕСЬ вміст файлу token.json у змінну GOOGLE_TOKEN_JSON на Railway.")
