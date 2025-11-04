import time
from telegram import Update
from telegram.ext import ContextTypes

TIME_LIMIT = 600

async def check_timeout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = context.user_data.get("start_time")

    if start_time is None:
        context.user_data["start_time"] = time.time()
        return False

    elapsed = time.time() - start_time
    if elapsed >= TIME_LIMIT:
        await update.message.reply_text(
            "⏰ Parece que você demorou muito pra finalizar, começe de novo com o /start."
        )
        context.user_data.clear()
        return True
    return False
