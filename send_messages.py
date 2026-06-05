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

CONTACTS = [
  {"name": "Iring", "tg": "@kate2109"},
  {"name": "Виктория", "tg": "+48794539534"},
  {"name": "Liudmyla", "tg": "+393466122712"},
  {"name": "Галина", "tg": "+3294766111"},
  {"name": "Nelia", "tg": "+3510424564"},
  {"name": "Svitlana", "tg": "+3899167058"},
  {"name": "Людмила", "tg": "+380964332455"},
  {"name": "", "tg": "@Diana"},
  {"name": "Виктория", "tg": "@veke_ceke_sweet"},
  {"name": "Mariia", "tg": "@Masha"},
  {"name": "Анастасия", "tg": "@n_n_d_s"},
  {"name": "Юля", "tg": "+380997684160"},
  {"name": "Аліна", "tg": "+353871943505"},
  {"name": "Ivanna", "tg": "+41798885669"},
  {"name": "Анастасия", "tg": "+134372993303"},
  {"name": "Ivanna", "tg": "+447476295217"},
  {"name": "Olga", "tg": "@Alegre"},
  {"name": "Nadi", "tg": "+4368120715537"},
  {"name": "Anna", "tg": "+19053346090"},
  {"name": "Марія", "tg": "+07739016873"},
  {"name": "Halyna", "tg": "+13475306858"},
  {"name": "Тетяна", "tg": "+16132181839"},
  {"name": "Oksana", "tg": "+7739460597"},
  {"name": "Marina", "tg": "+13126236121"},
  {"name": "Ольга", "tg": "+4916093459213"},
  {"name": "Ярослава", "tg": "@Yaroslava_Gonchar"},
  {"name": "Ольга", "tg": "@olgapotay"},
  {"name": "Victoria", "tg": "@Vita_iter"},
  {"name": "Iryna", "tg": "+17806046040"},
  {"name": "Чубук", "tg": "+380674100060"},
  {"name": "Andrey", "tg": "+420721352508"},
  {"name": "Julia", "tg": "+491774856243"},
  {"name": "Анна", "tg": "+34641863966"},
  {"name": "Nataliya", "tg": "+380672322452"},
  {"name": "Юлия", "tg": "+0665798787"},
  {"name": "Татьяна", "tg": "+420739818179"},
  {"name": "Irina", "tg": "+34671253226"},
  {"name": "Svitlana", "tg": "@frefly"},
  {"name": "Юлия", "tg": "+48881583562"},
  {"name": "Marina", "tg": "+380956098898"},
  {"name": "Валерия", "tg": "@Vallbas"},
  {"name": "Bohdana", "tg": "+16476423262"},
  {"name": "Nadiia", "tg": "@Nadija91"},
  {"name": "Svitlana", "tg": "+07365115633"},
  {"name": "Yulia", "tg": "@Yulia"},
  {"name": "Maryna", "tg": "@MarynaSolomka"},
  {"name": "Tetiana", "tg": "@Tanusia_barbara"},
  {"name": "Катерина", "tg": "@KaterynaBar"},
  {"name": "Марина", "tg": "@Umniashka5"},
  {"name": "Inna", "tg": "@InnaA"},
  {"name": "Світлана", "tg": "@Svitlana"},
  {"name": "Оксана", "tg": "+33764024532"},
  {"name": "Oksana", "tg": "+3127147021"},
  {"name": "Yuliia", "tg": "@Yuliia_sara"},
  {"name": "Руслана", "tg": "@Ruslana"},
  {"name": "Oksana", "tg": "+7804056292"},
  {"name": "Svitlana", "tg": "+14375537791"},
  {"name": "Наталія", "tg": "@NataliiaPavlovych"},
  {"name": "Светлана", "tg": "+48884940759"},
  {"name": "Наталія", "tg": "@natalkaste"},
  {"name": "Svitlana", "tg": "@SvitLanajats"},
  {"name": "Antonina", "tg": "+12497337211"},
  {"name": "Iryna", "tg": "@IrynaPlichko"},
  {"name": "", "tg": "+4917684108273"},
  {"name": "Alandara", "tg": "@alandaraj"},
  {"name": "Віка", "tg": "+4917684821025"},
  {"name": "Татьяна", "tg": "+4915125002615"},
  {"name": "Тетяна", "tg": "@manynatiktok"},
  {"name": "Olha", "tg": "@olyapolya5"},
  {"name": "Galyna", "tg": "@Galina_pelyak"},
  {"name": "Hanna", "tg": "+015161583880"},
  {"name": "Alex", "tg": "@Talcoconsulting"},
  {"name": "Овраменко", "tg": "+380502335726"},
  {"name": "Svitlana", "tg": "+4915172491127"},
  {"name": "Vira", "tg": "+48691677885"},
  {"name": "Ольга", "tg": "@olgaronski"},
  {"name": "Natalia", "tg": "@Natalia"},
  {"name": "Марія", "tg": "+380978935824"},
  {"name": "Nataliia", "tg": "+17132838311"},
  {"name": "Ирина", "tg": "+48794182732"},
  {"name": "Lenka", "tg": "@Lenka"},
  {"name": "Maryna", "tg": "@Maryna"},
  {"name": "Svitlana", "tg": "+380955763863"},
  {"name": "Olha", "tg": "@Happyolja"},
  {"name": "Halyna", "tg": "+015752670721"},
  {"name": "Ольга", "tg": "@olha_hashyna"},
  {"name": "Oksana", "tg": "+015120412375"},
  {"name": "Liudmyla", "tg": "+0663394515"},
  {"name": "Ivanna", "tg": "+48889189336"},
  {"name": "Alina", "tg": "+48735781541"},
  {"name": "Надя", "tg": "@nadya_doky"},
  {"name": "Inna", "tg": "@Inna_Zagorodnya"},
  {"name": "Ірина", "tg": "@iriskall"},
  {"name": "Ярина", "tg": "@Yaryna_Carpenter_ua"},
  {"name": "Наталія", "tg": "@natalmaz"},
  {"name": "Вика", "tg": "+0734931975"},
  {"name": "Марика", "tg": "@Marinich"},
  {"name": "Людмила", "tg": "@lyupante"},
  {"name": "Тетяна", "tg": "@Tetiana_shel"},
  {"name": "Лєна", "tg": "+380977911000"},
  {"name": "Sofiya", "tg": "@askerkoss"},
  {"name": "Світлана", "tg": "@svitlanavl"},
  {"name": "Tetiana", "tg": "@tatianacataldo"},
  {"name": "Светка", "tg": "@svets_rubanets"},
  {"name": "Оксана", "tg": "+1606610260"},
  {"name": "Олена", "tg": "@Helena_CHOICE"},
  {"name": "Olga", "tg": "@Olya_Kizyma"},
  {"name": "Anna", "tg": "+48880421080"},
  {"name": "Yuliia", "tg": "@Yliialiaskavka"},
  {"name": "Alla", "tg": "+491708091554"},
  {"name": "Natalia", "tg": "+491601743818"},
  {"name": "Tetiana", "tg": "@Tania"},
  {"name": "Тетяна", "tg": "+7208256430"},
  {"name": "Valeriia", "tg": "+48693307066"},
  {"name": "Ирина", "tg": "@aghu5"},
  {"name": "Ірина", "tg": "@irynaprudnikova"},
  {"name": "Julia", "tg": "+380503146619"},
  {"name": "Mariana", "tg": "@Mariana"},
  {"name": "Світлана", "tg": "@svetarubanets"},
  {"name": "Olga", "tg": "+0672336805"},
  {"name": "Alina", "tg": "+48792492304"},
  {"name": "Olena", "tg": "+48531433220"},
  {"name": "Аліна", "tg": "+380660019580"},
  {"name": "Кристина", "tg": "+380937252880"},
  {"name": "Roman", "tg": "+380933224169"},
  {"name": "Svitlana", "tg": "+48721386923"},
  {"name": "Татьяна", "tg": "+380669663466"},
  {"name": "Людмила", "tg": "@Milla"},
  {"name": "Светка", "tg": "@svetarubsnets"},
  {"name": "Anastasia", "tg": "+48728561528"},
  {"name": "Uliana", "tg": "+447467620013"},
  {"name": "Лілія", "tg": "@lilijazavalna"},
  {"name": "Наталія", "tg": "@tashik0101"},
  {"name": "Viktoriia", "tg": "@Viktoriia"},
  {"name": "Наталія", "tg": "+380965303530"},
  {"name": "Andrej", "tg": "+420775631154"},
  {"name": "Руслана", "tg": "+420775608418"},
  {"name": "Anna", "tg": "+447482866889"},
  {"name": "Oksana", "tg": "@KonOksana04"},
  {"name": "Елена", "tg": "@Olenkafire78"},
  {"name": "Наталия", "tg": "+380671735303"},
  {"name": "Inna", "tg": "+380677391232"}
]

LOG_FILE = '/root/my-bot/send_log.txt'

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
    log(f'Всього контактів: {len(CONTACTS)}')

    # Build set of existing dialog IDs
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
            entity = await client.get_entity(tg)

            if entity.id in existing_ids:
                log(f'[{i+1}/{len(CONTACTS)}] ПРОПУСК (вже є діалог): {name} {tg}')
                skipped += 1
                continue

            await client.send_message(entity, msg)
            log(f'[{i+1}/{len(CONTACTS)}] ВІДПРАВЛЕНО: {name} {tg}')
            sent += 1

            delay = random.randint(45, 90)
            log(f'Пауза {delay} сек...')
            await asyncio.sleep(delay)

        except FloodWaitError as e:
            log(f'FloodWait {e.seconds} сек — чекаю...')
            await asyncio.sleep(e.seconds + 5)
        except (UserPrivacyRestrictedError, UserNotMutualContactError):
            log(f'[{i+1}/{len(CONTACTS)}] ПРИВАТНІСТЬ: {name} {tg}')
            failed += 1
        except (UsernameNotOccupiedError, UsernameInvalidError):
            log(f'[{i+1}/{len(CONTACTS)}] НЕ ЗНАЙДЕНО: {name} {tg}')
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
    log(f'Помилки: {failed}')
    await client.disconnect()

asyncio.run(main())
