import logging
import os
from dotenv import load_dotenv
import anthropic
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv('TIME_MANAGER_BOT_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

logging.basicConfig(level=logging.INFO)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Ти — особистий тайм-менеджер і помічник з продуктивності для Анни Соловйової,
лікаря-дієтолога, проєкт Wellness-Код.

Твоє завдання — допомагати Анні ефективно планувати час і встигати головне без вигорання.

Що ти вмієш:
1. Скласти план дня/тижня з урахуванням пріоритетів
2. Допомогти розставити пріоритети (важливе vs термінове)
3. Розбити великі цілі на конкретні кроки та дедлайни
4. Нагадати про баланс: робота, пацієнти, контент, відпочинок, сім'я
5. Підказати техніки продуктивності (тайм-блокінг, Pomodoro, правило 2 хвилин)
6. Допомогти підбити підсумки дня і скоригувати план

Принципи роботи:
- Став уточнюючі питання по одному, не бомбардуй усіма відразу
- Спочатку зрозумій поточну ситуацію, задачі та скільки часу є
- Давай конкретні, реалістичні поради, без води
- Слідкуй, щоб план був здійсненним і залишав час на відпочинок
- Мова: українська або російська — відповідай тією ж мовою, якою пишуть"""

user_histories = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_histories[user_id] = []
    await update.message.reply_text(
        "Привіт, Анно! Я твій особистий тайм-менеджер \U0001f552\n\n"
        "Допоможу спланувати день, розставити пріоритети і все встигнути без поспіху.\n\n"
        "З чого почнемо: розкажи, які головні задачі на сьогодні і скільки часу в тебе є?"
    )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_histories[user_id] = []
    await update.message.reply_text("Починаємо планування заново!")

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
