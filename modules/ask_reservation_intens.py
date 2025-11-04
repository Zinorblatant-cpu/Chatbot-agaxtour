from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# === PERGUNTA: deseja reservar? ===
async def ask_reservation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Você gostaria de criar uma reserva para essa viagem? (responda com sim ou não)",
        parse_mode="Markdown"
    )
    context.user_data['next'] = 'reserve'