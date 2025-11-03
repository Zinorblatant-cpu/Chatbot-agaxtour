from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

TOKEN = 'SEU_TOKEN_AQUI'


# === /start ===
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


# === ESCOLHA DE OPÇÃO (1–4) ===
async def handle_text_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    if user_input == '1':
        await update.message.reply_text(
            (
                "Viva uma jornada **exclusiva e memorável** a bordo do **Explora III**! 🌍⚓\n\n"
                "📅 **Período**: 09 a 17 de setembro\n"
                "📍 **Destinos**: Inglaterra, Escócia, Irlanda e Islândia\n\n"
                "✨ Uma experiência *all inclusive premium*, com:\n"
                "• Atendimento personalizado Agaxtur Jardim Europa\n"
                "• Conforto refinado em cada cabine\n"
                "• Cultura, história e paisagens deslumbrantes em cada parada\n"
                "• Gastronomia gourmet e serviço impecável\n\n"
                "Perfeito para quem busca **elegância, exclusividade e aventura** em alto-mar."
            ),
            parse_mode="Markdown"
        )
        context.user_data['choice'] = 'Explora III'
        await ask_reservation(update, context)

    elif user_input == '2':
        await update.message.reply_text(
            (
                "Imagine uma semana de descanso verdadeiro em Alagoas no **Ritz Barra de São Miguel**:\n"
                "conforto e sofisticação à beira-mar. Ambientes pensados para seu bem-estar, "
                "gastronomia de alto nível e serviços impecáveis! Perfeito para casais, famílias ou "
                "quem busca tranquilidade com charme e praticidade.\n\n"
                "✅ **Pacote**: voos + 7 noites\n"
                "📅 **Saída**: 01/11/25 → 08/11/25"
            ),
            parse_mode="Markdown"
        )
        context.user_data['choice'] = 'Ritz Barra de São Miguel'
        await ask_reservation(update, context)

    elif user_input == '3':
        await update.message.reply_text(
            (
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
            ),
            parse_mode="Markdown"
        )
        context.user_data['choice'] = 'MSC Seaview'
        await ask_reservation(update, context)

    elif user_input == '4':
        await update.message.reply_text("Veja todas as opções em https://www.agaxtur.com.br/")
    else:
        await update.message.reply_text(
            "Por favor, envie apenas o número da opção desejada:\n"
            "1 → Explora III\n"
            "2 → São Miguel\n"
            "3 → MSC Seaview\n"
            "4 → Site"
        )



# === PERGUNTA: deseja reservar? ===
async def ask_reservation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Você gostaria de criar uma reserva para essa viagem? (responda com *sim* ou *não*)",
        parse_mode="Markdown"
    )
    context.user_data['next'] = 'reserve'


# === TRATA A PRÓXIMA MENSAGEM ===
async def handle_next_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get('next')
    text = update.message.text.strip().lower()

    if step == 'reserve':
        if text in ['sim', 's']:
            await update.message.reply_text(
                "Perfeito! ✨ Qual meio de transporte você prefere? (ônibus / avião / barco)"
            )
            context.user_data['next'] = 'transport'
        elif text in ['não', 'n']:
            await update.message.reply_text(
                "Tudo bem! 😊 Ficamos à disposição se quiser ver outras viagens."
            )
            context.user_data.clear()
        else:
            await update.message.reply_text("Responda apenas com *sim* ou *não*.", parse_mode="Markdown")

    elif step == 'transport':
        transport = text.lower()
        if transport in ['ônibus', 'onibus', 'avião', 'aviao', 'barco', 'cruzeiro']:
            context.user_data['transport'] = transport
            await update.message.reply_text(
                f"Excelente! Você escolheu viajar de *{transport}*. ✈️🚌🚢\n\n"
                "Agora, nos diga: *em qual data gostaria de viajar?* (ex: 15/11/2025)",
                parse_mode="Markdown"
            )
            context.user_data['next'] = 'date'
        else:
            await update.message.reply_text("Informe apenas: ônibus, avião ou barco.")

    elif step == 'date':
        date = text
        choice = context.user_data.get('choice', 'viagem não especificada')
        transport = context.user_data.get('transport', 'não especificado')
        await update.message.reply_text(
            f"Perfeito! 🎉\n\nResumo da sua intenção de reserva:\n"
            f"• Viagem: *{choice}*\n"
            f"• Transporte: *{transport}*\n"
            f"• Data desejada: *{date}*\n\n"
            "Um consultor Agaxtur entrará em contato para continuar o atendimento. Obrigado!",
            parse_mode="Markdown"
        )
        context.user_data.clear()
    else:
        # Caso o usuário envie algo fora do fluxo
        await handle_text_choice(update, context)


# === MAIN ===
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_next_step))

    print("✅ Bot Agaxtur (modo texto) iniciado!")
    app.run_polling()


if __name__ == "__main__":
    main()
