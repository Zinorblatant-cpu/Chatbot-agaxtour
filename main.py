import time
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from modules.travel_selection import select_travel_option
from modules.ask_reservation_intens import ask_reservation
from modules.reservation_flow import collect_reservation_intent
from modules.time.reset_time import reset_time
from modules.time.time_end import check_timeout

TOKEN = '8536310042:AAFjWY5tPS-qJXL0016tJB5AO40mMUtR3QQ'

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reset_time(context)
    await update.message.reply_text(
        "Olá! Nós somos a Agaxtur — mais de 70 anos transformando sonhos em viagens reais. 🌍✈️\n\n"
        "Este chat foi criado para mostrar nossas viagens disponíveis."
    )

    travel_text = (
        "✨ Três experiências incríveis te esperam!\n\n"
        "⚓ Explora III: jornada exclusiva por destinos deslumbrantes.\n"
        "🏖️ Ritz Barra de São Miguel: conforto e sofisticação à beira-mar.\n"
        "🚢 MSC Seaview: comece 2026 navegando com estilo e diversão.\n\n"
        "Digite o número da opção desejada:\n"
        "1 → Explora III\n"
        "2 → São Miguel\n"
        "3 → MSC Seaview\n"
        "4 → Ver todas as opções no site"
    )
    await update.message.reply_text(travel_text, parse_mode="Markdown")

# === Handler principal de mensagens ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. Verifica se o tempo expirou
    if await check_timeout(update, context):
        return

    # 2. Atualiza o tempo do usuário
    reset_time(context)

    # 3. Continua o fluxo normal
    step = context.user_data.get('next')
    if step:
        await collect_reservation_intent(update, context)
    else:
        await select_travel_option(update, context)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot Agaxtur iniciado!")
    app.run_polling()

if __name__ == "__main__":
    main()
