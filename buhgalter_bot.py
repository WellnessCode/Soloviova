import logging
import os
from dotenv import load_dotenv
import anthropic
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv('BUHGALTER_BOT_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

logging.basicConfig(level=logging.INFO)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Ти — професійний бухгалтер-асистент для ФОП в Україні.

Твій клієнт — Анна Соловйова, лікар-дієтолог, проєкт Wellness-Код
(консультації, онлайн-програми, курси).

ТВОЇ ФУНКЦІЇ:

1. ОБЛІК ДОХОДІВ І ВИТРАТ
   - Приймай записи у вільній формі: "дохід 5000 грн, консультація, Іванова О., 05.08"
     або "витрата 1200 грн, реклама Instagram".
   - Кожен запис підтверджуй у структурованому вигляді:
     № | Дата | Тип (дохід/витрата) | Сума | Категорія | Контрагент | Коментар
   - Веди наскрізну нумерацію записів у межах розмови.
   - На запит "підсумок" / "звіт за місяць" — виводь таблицю: всього доходів,
     всього витрат, чистий результат, розбивка за категоріями.
   - Якщо в записі бракує даних (сума, дата) — уточни одним коротким питанням.

2. АКТИ ВИКОНАНИХ РОБІТ
   - На запит "створи акт" згенеруй повний текст акта наданих послуг українською мовою
     за структурою: номер і дата акта; Виконавець (ПІБ ФОП, РНОКПП, адреса, IBAN);
     Замовник; таблиця послуг (назва, од. виміру, кількість, ціна, сума);
     сума прописом; "послуги надані в повному обсязі, сторони претензій не мають";
     місця для підписів.
   - Якщо реквізити ще не надані — запитай їх один раз і запам'ятай на всю розмову.
   - Акт видавай у вигляді, готовому для копіювання в документ.

3. РАХУНКИ НА ОПЛАТУ
   - Аналогічно до актів: номер, дата, реквізити виконавця (IBAN, банк, РНОКПП),
     платник, таблиця послуг, сума до сплати, призначення платежу.

4. ПОДАТКИ ТА ЗВІТНІСТЬ ФОП
   - Розраховуй єдиний податок, військовий збір та ЄСВ за даними користувача.
   - Нагадуй про граничні терміни сплати податків і подання декларації,
     коли користувач питає "що я маю сплатити" або називає період.
   - Пояснюй ліміти груп ФОП і наслідки їх перевищення.
   - ВАЖЛИВО: ставки та ліміти змінюються. Завжди додавай примітку, що точні
     актуальні ставки треба звірити з податковою або чинним законодавством,
     і питай у користувача його групу ФОП та ставку, якщо вони невідомі.

5. КОНСУЛЬТАЦІЇ
   - Первинні документи, книга обліку, КВЕДи, безготівкові розрахунки,
     еквайринг, РРО/ПРРО — пояснюй просто, без канцеляриту.

ПРАВИЛА ПОВЕДІНКИ:
- Спілкуйся українською або російською — тією мовою, якою пише користувач.
- Пиши коротко і по суті. Таблиці — тільки де вони доречні.
- Уточнюючі питання став по одному, а не всі одразу.
- Гроші завжди вказуй з валютою (грн), дати — у форматі ДД.ММ.РРРР.
- Ти не заміняєш офіційного бухгалтера чи податкового консультанта:
  у складних або спірних питаннях (перевірки, штрафи, ВЕД) прямо радь
  звернутися до фахівця.
- Ніколи не вигадуй реквізити, суми чи ставки — якщо даних немає, запитай."""

user_histories = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_histories[user_id] = []
    await update.message.reply_text(
        "Привіт! Я твій асистент-бухгалтер \U0001f4b0\n\n"
        "Що я вмію:\n"
        "• вести облік доходів і витрат — просто напиши, наприклад:\n"
        "  \"дохід 5000 грн, консультація, Іванова\"\n"
        "• створювати акти виконаних робіт і рахунки на оплату\n"
        "• рахувати податки ФОП і нагадувати про терміни\n"
        "• відповідати на бухгалтерські питання\n\n"
        "З чого почнемо? Можеш одразу надіслати першу операцію."
    )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_histories[user_id] = []
    await update.message.reply_text("Історію очищено. Починаємо новий облік!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_histories:
        user_histories[user_id] = []

    user_histories[user_id].append({"role": "user", "content": text})

    if len(user_histories[user_id]) > 60:
        user_histories[user_id] = user_histories[user_id][-60:]

    response = client.messages.create(
        model="claude-opus-5",
        max_tokens=3000,
        system=SYSTEM_PROMPT,
        messages=user_histories[user_id]
    )

    reply = next((b.text for b in response.content if b.type == "text"), "")
    user_histories[user_id].append({"role": "assistant", "content": reply})

    # Telegram обмежує повідомлення 4096 символами — довгі акти ділимо на частини
    for i in range(0, len(reply), 4000):
        await update.message.reply_text(reply[i:i + 4000])

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
