# Подключение Google Календаря к боту (разовая настройка)

Бот ведёт ваш Google Календарь и создаёт встречи со ссылками Google Meet.
Чтобы дать ему доступ, нужно один раз выполнить шаги ниже.

## Шаг 1. Создать проект в Google Cloud
1. Откройте https://console.cloud.google.com
2. Вверху нажмите на выбор проекта → **New Project** → назовите, например, `time-manager` → **Create**.

## Шаг 2. Включить Google Calendar API
1. В поиске вверху введите **Google Calendar API** → откройте → **Enable**.

## Шаг 3. Настроить экран согласия (OAuth consent screen)
1. Слева: **APIs & Services → OAuth consent screen**.
2. Тип — **External** → **Create**.
3. Заполните название приложения и свой email → сохраните (остальное можно пропустить, **Save and continue**).
4. На шаге **Test users** нажмите **Add users** и добавьте **свой Gmail** (тот, чей календарь ведём). Сохраните.

## Шаг 4. Создать OAuth-ключ (credentials.json)
1. Слева: **APIs & Services → Credentials**.
2. **Create Credentials → OAuth client ID**.
3. Application type — **Desktop app** → **Create**.
4. Нажмите **Download JSON** — сохраните файл и **переименуйте его в `credentials.json`**.

## Шаг 5. Получить token.json (авторизация)
На своём компьютере (нужен установленный Python):
```
pip install google-auth-oauthlib google-api-python-client
python auth_google.py
```
1. Положите `credentials.json` в ту же папку, где `auth_google.py`.
2. Откроется браузер — войдите своим Gmail и разрешите доступ к календарю.
   (Если покажет предупреждение «app not verified» — это нормально для своего приложения:
   **Advanced → Go to … (unsafe) → Continue**.)
3. Появится файл **`token.json`**.

## Шаг 6. Вставить token.json на хостинг
1. Откройте `token.json`, скопируйте **весь** его текст.
2. На Railway → вкладка **Variables** → создайте переменную:
   - `GOOGLE_TOKEN_JSON` = (вставьте весь скопированный текст token.json)
3. Заодно проверьте, что заданы `TIME_MANAGER_BOT_TOKEN` и `ANTHROPIC_API_KEY`.

Готово! После перезапуска бот сможет вести ваш календарь и создавать встречи с Google Meet.

> ⚠️ Безопасность: `credentials.json` и `token.json` — секретные, они защищены `.gitignore`
> и НЕ попадают в публичный репозиторий. Никому их не пересылайте.
