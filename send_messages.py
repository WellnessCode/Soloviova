import asyncio
import random
import os
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import (
    FloodWaitError, UserPrivacyRestrictedError, UsernameNotOccupiedError,
    PeerFloodError, UserNotMutualContactError, InputUserDeactivatedError,
    UsernameInvalidError
)

load_dotenv('/root/my-bot/.env')

api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')

# Тільки @нікнейми — номера телефону не працюють без контактів
CONTACTS = [
  {"name": "Iring", "tg": "@kate2109"},
  {"name": "Виктория", "tg": "@veke_ceke_sweet"},
  {"name": "Mariia", "tg": "@Masha"},
  {"name": "Анастасия", "tg": "@n_n_d_s"},
  {"name": "Olga", "tg": "@Alegre"},
  {"name": "Ярослава", "tg": "@Yaroslava_Gonchar"},
  {"name": "Ольга", "tg": "@olgapotay"},
  {"name": "Victoria", "tg": "@Vita_iter"},
  {"name": "Svitlana", "tg": "@frefly"},
  {"name": "Валерия", "tg": "@Vallbas"},
  {"name": "Nadiia", "tg": "@Nadija91"},
  {"name": "Yulia", "tg": "@Yulia"},
  {"name": "Maryna", "tg": "@MarynaSolomka"},
  {"name": "Tetiana", "tg": "@Tanusia_barbara"},
  {"name": "Катерина", "tg": "@KaterynaBar"},
  {"name": "Марина", "tg": "@Umniashka5"},
  {"name": "Inna", "tg": "@InnaA"},
  {"name": "Світлана", "tg": "@Svitlana"},
  {"name": "Yuliia", "tg": "@Yuliia_sara"},
  {"name": "Руслана", "tg": "@Ruslana"},
  {"name": "Наталія", "tg": "@NataliiaPavlovych"},
  {"name": "Наталія", "tg": "@natalkaste"},
  {"name": "Svitlana", "tg": "@SvitLanajats"},
  {"name": "Iryna", "tg": "@IrynaPlichko"},
  {"name": "Alandara", "tg": "@alandaraj"},
  {"name": "Тетяна", "tg": "@manynatiktok"},
  {"name": "Olha", "tg": "@olyapolya5"},
  {"name": "Galyna", "tg": "@Galina_pelyak"},
  {"name": "Alex", "tg": "@Talcoconsulting"},
  {"name": "Ольга", "tg": "@olgaronski"},
  {"name": "Natalia", "tg": "@Natalia"},
  {"name": "Lenka", "tg": "@Lenka"},
  {"name": "Maryna", "tg": "@Maryna"},
  {"name": "Olha", "tg": "@Happyolja"},
  {"name": "Ольга", "tg": "@olha_hashyna"},
  {"name": "Надя", "tg": "@nadya_doky"},
  {"name": "Inna", "tg": "@Inna_Zagorodnya"},
  {"name": "Ірина", "tg": "@iriskall"},
  {"name": "Ярина", "tg": "@Yaryna_Carpenter_ua"},
  {"name": "Наталія", "tg": "@natalmaz"},
  {"name": "Марика", "tg": "@Marinich"},
  {"name": "Людмила", "tg": "@lyupante"},
  {"name": "Тетяна", "tg": "@Tetiana_shel"},
  {"name": "Sofiya", "tg": "@askerkoss"},
  {"name": "Світлана", "tg": "@svitlanavl"},
  {"name": "Tetiana", "tg": "@tatianacataldo"},
  {"name": "Светка", "tg": "@svets_rubanets"},
  {"name": "Олена", "tg": "@Helena_CHOICE"},
  {"name": "Olga", "tg": "@Olya_Kizyma"},
  {"name": "Yuliia", "tg": "@Yliialiaskavka"},
  {"name": "Tetiana", "tg": "@Tania"},
  {"name": "Ирина", "tg": "@aghu5"},
  {"name": "Ірина", "tg": "@irynaprudnikova"},
  {"name": "Mariana", "tg": "@Mariana"},
  {"name": "Світлана", "tg": "@svetarubanets"},
  {"name": "Людмила", "tg": "@Milla"},
  {"name": "Светка", "tg": "@svetarubsnets"},
  {"name": "Лілія", "tg": "@lilijazavalna"},
  {"name": "Наталія", "tg": "@tashik0101"},
  {"name": "Viktoriia", "tg": "@Viktoriia"},
  {"name": "Oksana", "tg": "@KonOksana04"},
  {"name": "Елена", "tg": "@Olenkafire78"}
]

LOG_FILE = '/root/my-bot/send_log2.txt'

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    line = f'[{ts}] {msg}'
    print(line)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

def build_message(name):
    greeting = f'Вітаю, {name}!' if name.strip() else 'Вітаю!'
    return (
        f'{greeting}\n\n'
        f'Я Анна, головний лікар-дієтолог і мама проєкту WELLNESS CODE.\n\n'
        f'Ви якось залишали заявку на мою консультацію.\n\n'
        f'Нам так і не вдалось з вами поспілкуватись.\n\n'
        f'Як ваші справи?\n\n'
        f'Вам вдалось схуднути?\n'
        f'Чи можливо вам потрібна допомога?'
    )

async def main():
    client = TelegramClient('/root/my-bot/user_session', api_id, api_hash)
    await client.start()

    if not await client.is_user_authorized():
        log('ПОМИЛКА: сесія не авторизована!')
        return

    me = await client.get_me()
    log(f'Авторизовано як {me.first_name} (@{me.username})')
    log(f'Всього @-контактів: {len(CONTACTS)}')

    log('Завантажую список діалогів...')
    existing_ids = set()
    async for dialog in client.iter_dialogs():
        existing_ids.add(dialog.entity.id)
    log(f'Діалогів знайдено: {len(existing_ids)}')

    sent = 0
    failed = 0
    skipped = 0

    for i, contact in enumerate(CONTACTS):
        name = contact['name']
        tg = contact['tg']
        msg = build_message(name)

        try:
            # Пауза перед пошуком entity — захист від FloodWait
            await asyncio.sleep(random.randint(3, 6))

            entity = await client.get_entity(tg)

            if entity.id in existing_ids:
                log(f'[{i+1}/{len(CONTACTS)}] ПРОПУСК (вже є діалог): {name} {tg}')
                skipped += 1
                continue

            await client.send_message(entity, msg)
            log(f'[{i+1}/{len(CONTACTS)}] ВІДПРАВЛЕНО: {name} {tg}')
            sent += 1

            delay = random.randint(60, 120)
            log(f'Пауза {delay} сек...')
            await asyncio.sleep(delay)

        except FloodWaitError as e:
            log(f'FloodWait {e.seconds} сек — чекаю...')
            await asyncio.sleep(e.seconds + 10)
        except (UserPrivacyRestrictedError, UserNotMutualContactError):
            log(f'[{i+1}/{len(CONTACTS)}] ПРИВАТНІСТЬ: {name} {tg}')
            failed += 1
        except (UsernameNotOccupiedError, UsernameInvalidError):
            log(f'[{i+1}/{len(CONTACTS)}] НЕ ІСНУЄ: {name} {tg}')
            failed += 1
        except InputUserDeactivatedError:
            log(f'[{i+1}/{len(CONTACTS)}] ДЕАКТИВОВАНО: {name} {tg}')
            failed += 1
        except PeerFloodError:
            log('СТОП: Telegram заблокував розсилку. Спробуйте завтра.')
            break
        except Exception as e:
            log(f'[{i+1}/{len(CONTACTS)}] ПОМИЛКА {name} {tg}: {e}')
            failed += 1

    log(f'\n=== РЕЗУЛЬТАТ ===')
    log(f'Відправлено: {sent}')
    log(f'Пропущено (вже є діалог): {skipped}')
    log(f'Не знайдено/Помилки: {failed}')
    await client.disconnect()

asyncio.run(main())
