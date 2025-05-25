import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Setup logging supaya mudah debug
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Setup OpenAI API key dari environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Handler untuk command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hai! Saya Kasmera, bot AI awak. Apa khabar?")

# Handler untuk mesej biasa (balas guna OpenAI)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        # Call OpenAI ChatCompletion API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_text}],
            max_tokens=150
        )
        bot_reply = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        bot_reply = "Maaf, saya ada masalah sambungan sekarang."

    await update.message.reply_text(bot_reply)

def main():
    # Ambil token Telegram dari environment variable
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not telegram_token:
        logger.error("Telegram bot token tidak dijumpai dalam environment variable TELEGRAM_BOT_TOKEN")
        return

    app = ApplicationBuilder().token(telegram_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
