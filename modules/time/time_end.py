import time
from telegram import Update
from telegram.ext import ContextTypes

TIME_LIMIT = 600  # 10 minutos

async def check_timeout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Se a sessão foi finalizada, não checa mais o tempo
    if context.user_data.get("session_finished"):
        return False

    start_time = context.user_data.get("start_time")

    # Inicializa o tempo de início se ainda não existir
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
