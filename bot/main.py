import asyncio
import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from bot.db import log_button_event, apply_migrations, get_today_stats
from bot.buttons import main_keyboard, BUTTON_TEXTS_SET

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    apply_migrations()
    await update.message.reply_text("Choose an option:", reply_markup=main_keyboard)


# Button handler
async def handle_button_press(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    button_text = update.message.text

    if button_text not in BUTTON_TEXTS_SET:
        await update.message.reply_text("Please use the buttons.")
        return

    # Run DB logging in thread
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, log_button_event, user_id, button_text)

    await update.message.reply_text(f"You pressed: {button_text}")


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    text = get_today_stats(user_id)
    await update.message.reply_text(text)


# App entry point
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_button_press))
    app.add_handler(CommandHandler("stats", stats_command))

    app.run_polling()


if __name__ == '__main__':
    main()
