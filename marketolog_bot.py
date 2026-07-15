import logging
import os
from dotenv import load_dotenv
import anthropic
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv('MARKETOLOG_BOT_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

logging.basicConfig(level=logging.INFO)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Ти — експерт з маркетингу в Instagram і особистий брендингу для лікарів.

Твій клієнт — Анна Соловйова, лікар-дієтолог, проєкт Wellness-Код.

Твоє завдання:
1. Поставляти чіткі запитання щоб зрозуміти поточну ситуацію, цілі та аудиторію
2. Побудувати покрокову стратегію просування в Instagram
3. Давати конкретні рекомендації по:
   - Контент-план (рубрики, формати, частота)
   - Оформлення профілю
   - Реелси, сторіз, пости
   - Залучення аудиторії
   - Монетизація

Спочатку збери потрібну інформацію задаючи питання по одному, не бомбардуючи всіма відразу.
Відповідай зрозуміло, по суті, без зайвих слів.
Мова: українська або російська — відповідай тією ж мовою, якою пишуть."""

user_histories = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_histories[user_id] = []
    await update.message.reply_text(
        "Привіт! Я твій AI-маркетолог \U0001f4ca\n\n"
        "Побудуюмо стратегію просування в Instagram спеціально під тебе.\n\n"
        "Спочатку скажи: скільки зараз підписників в твоєму Instagram і яка головна мета на наступні 3 місяці?"
    )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_histories[user_id] = []
    await update.message.reply_text("Починаємо знову!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_histories:
        user_histories[user_id] = []

    user_histories[user_id].append({"role": "user", "content": text})

    if len(user_histories[user_id]) > 40:
        user_histories[user_id] = user_histories[user_id][-40:]

    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=user_histories[user_id]
    )

    reply = response.content[0].text
    user_histories[user_id].append({"role": "assistant", "content": reply})

    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
