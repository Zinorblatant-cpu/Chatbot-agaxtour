from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,  # ← FALTAVA ESSA LINHA
    filters
)


# Substitua pelo seu token do BotFather (nunca compartilhe publicamente!)
TOKEN = 'SEU_TOKEN_AQUI'

# === COMANDO /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Nós somos a **Agaxtur** — mais de 70 anos transformando sonhos em viagens reais. 🌍✈️\n\n"
        "Este chat foi criado para mostrar nossas viagens disponíveis."
    )
    travel_text = (
        "✨ **Três experiências incríveis te esperam!**\n\n"
        "⚓ **Explora III**: jornada exclusiva por destinos deslumbrantes.\n"
        "🏖️ **Ritz Barra de São Miguel**: conforto e sofisticação à beira-mar.\n"
        "🚢 **MSC Seaview**: comece 2026 navegando com estilo e diversão.\n\n"
        "Digite o número da opção desejada:\n"
        "1 → Explora III\n"
        "2 → São Miguel\n"
        "3 → MSC Seaview\n"
        "4 → Ver todas as opções no site"
    )
    await update.message.reply_text(travel_text, parse_mode="Markdown")

# === ESCOLHA DA VIAGEM (1, 2, 3, 4) ===
async def handle_text_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    match user_input:
        case '1':
            text = (
                "Viva uma jornada **exclusiva e memorável** a bordo do **Explora III**! 🌍⚓\n\n"
                "📅 **Período**: 09 a 17 de setembro\n"
                "📍 **Destinos**: Inglaterra, Escócia, Irlanda e Islândia\n\n"
                "✨ Uma experiência *all inclusive premium*, com:\n"
                "• Atendimento personalizado Agaxtur Jardim Europa\n"
                "• Conforto refinado em cada cabine\n"
                "• Cultura, história e paisagens deslumbrantes em cada parada\n"
                "• Gastronomia gourmet e serviço impecável\n\n"
                "Perfeito para quem busca **elegância, exclusividade e aventura** em alto-mar."
            )
            await update.message.reply_text(text, parse_mode="Markdown")
            await create_reserve(update, context)

        case '2':
            text = (
                "Imagine uma semana de descanso verdadeiro em Alagoas no **Ritz Barra de São Miguel**:\n"
                "conforto e sofisticação à beira-mar. Ambientes pensados para seu bem-estar, "
                "gastronomia de alto nível e serviços impecáveis! Perfeito para casais, famílias ou "
                "quem busca tranquilidade com charme e praticidade.\n\n"
                "✅ **Pacote**: voos + 7 noites\n"
                "📅 **Saída**: 01/11/25 → 08/11/25"
            )
            await update.message.reply_text(text, parse_mode="Markdown")
            await create_reserve(update, context)

        case '3':
            text = (
                "Comece 2026 a bordo do **MSC Seaview**! 🚢\n\n"
                "Embarque em Santos no dia 17/01/26 para 7 noites inesquecíveis, com paradas em "
                "Búzios, Salvador e Maceió.\n\n"
                "A bordo, desfrute de:\n"
                "🍽️ Restaurantes premiados\n"
                "🌅 Bares com vista para o mar\n"
                "🏊 Piscinas panorâmicas\n"
                "💆 Spa completo\n"
                "🎭 Teatro e lojas\n"
                "✨ Atrações exclusivas como a Infinity Bridge e o MSC Yacht Club\n\n"
                "✅ **Cabine com varanda** a partir de 12x de R$ 605,26 por pessoa."
            )
            await update.message.reply_text(text, parse_mode="Markdown")
            await create_reserve(update, context)

        case '4':
            await update.message.reply_text(
                "Veja todas as nossas opções em: https://www.agaxtur.com.br/"
            )
        case _:
            await update.message.reply_text(
                "Por favor, envie apenas o número da opção desejada:\n"
                "1 → Explora III\n"
                "2 → São Miguel\n"
                "3 → MSC Seaview\n"
                "4 → Site"
            )

async def create_reserve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ Enviando botões de reserva...")  # ← ADICIONE ISSO
    keyboard = [
        [
            InlineKeyboardButton("✅ Sim, quero reservar", callback_data='reserve_yes'),
            InlineKeyboardButton("❌ Não, obrigado", callback_data='reserve_no')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Você gostaria de criar uma reserva?",
        reply_markup=reply_markup,
    )


# === RESPOSTA DA CONFIRMAÇÃO ===
async def handle_reserve_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🔍 Callback de reserva recebido!")  # ← ADICIONE ISSO
    query = update.callback_query
    await query.answer()

    if query.data == 'reserve_yes':
        await query.message.reply_text(
            "Ótimo! 🎉\n"
            "Vamos começar a planejar sua viagem dos sonhos com a Agaxtur! "
            "Seu atendimento será feito com todo o carinho e expertise de quem tem mais de 70 anos transformando sonhos em viagens reais. ✈️🌊🏨"
        )
        # Pergunta transporte com BOTÕES
        keyboard = [
            [InlineKeyboardButton("🚌 Ônibus", callback_data='transport_bus')],
            [InlineKeyboardButton("✈️ Avião", callback_data='transport_plane')],
            [InlineKeyboardButton("🚢 Barco / Cruzeiro", callback_data='transport_boat')]
        ]
        await query.message.reply_text(
            "Escolha seu meio de transporte:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == 'reserve_no':
        await query.message.reply_text(
            "Tudo bem! 😊\n"
            "Se precisar de ajuda no futuro, estamos sempre por aqui. A Agaxtur tem mais de 70 anos de experiência para tornar suas viagens inesquecíveis!"
        )

# === PERGUNTA: MEIO DE TRANSPORTE ===
async def ask_transport_by_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚌 Ônibus", callback_data='transport_bus')],
        [InlineKeyboardButton("✈️ Avião", callback_data='transport_plane')],
        [InlineKeyboardButton("🚢 Barco / Cruzeiro", callback_data='transport_boat')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Para personalizar sua reserva com a excelência Agaxtur, escolha seu meio de transporte:",
        reply_markup=reply_markup
    )

# === RESPOSTA DO TRANSPORTE ===
async def handle_transport_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    transport_map = {
        'transport_bus': 'Ônibus',
        'transport_plane': 'Avião',
        'transport_boat': 'Barco / Cruzeiro'
    }

    chosen = transport_map.get(query.data, "Não especificado")
    context.user_data['transport'] = chosen

    await query.message.reply_text(
        f"Ótimo! Você escolheu viajar de **{chosen}**. 🌟\n\n"
        "Agora, nos diga: **em qual data você gostaria de viajar?**\n"
        "(Ex: 15/11/2025)"
    )

async def debug_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"⚠️ Callback não tratado: {update.callback_query.data}")

# === INICIALIZAÇÃO ===
def main():
    app = Application.builder().token(TOKEN).build()

    # === Handlers de callback ===
    app.add_handler(CallbackQueryHandler(handle_transport_callback, pattern='^transport_'))
    app.add_handler(CallbackQueryHandler(handle_reserve_callback, pattern='^reserve_'))
    app.add_handler(CallbackQueryHandler(debug_callback))  # captura qualquer outro

    # === Handlers de texto e comando ===
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_choice))
    app.add_handler(CommandHandler("start", start))

    print("✅ Bot Agaxtur iniciado!")
    app.run_polling()



if __name__ == '__main__':
    main()