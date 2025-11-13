from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from modules.ask_reservation_intens import ask_reservation

pdf_path = "/home/zinor/Documents/programing/agaxtuor/modules/exploraitinerario_p7_17.pdf"

async def select_travel_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    if user_input == '1':
        await update.message.reply_text(
            (
                "Viva uma jornada exclusiva e memorável a bordo do Explora III! 🌍⚓\n\n"
                "📅 Período: 09 a 17 de setembro\n"
                "📍 Destinos: Inglaterra, Escócia, Irlanda e Islândia\n\n"
                "✨ Uma experiência all inclusive premium, com:\n"
                "• Atendimento personalizado Agaxtur Jardim Europa\n"
                "• Conforto refinado em cada cabine\n"
                "• Cultura, história e paisagens deslumbrantes em cada parada\n"
                "• Gastronomia gourmet e serviço impecável\n\n"
                "Perfeito para quem busca elegância, exclusividade e aventura em alto-mar."
            ),
            parse_mode="Markdown"
        )

        with open(pdf_path, "rb") as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename="ExploraIII_Agaxtur.pdf",
                caption="📎 Aqui está o catálogo completo da viagem Explora III 🌍⚓",
            )

        context.user_data['choice'] = 'Explora III'
        await ask_reservation(update, context)


    elif user_input == '2':
        await update.message.reply_text(
            (
                "Imagine uma semana de descanso verdadeiro em Alagoas no Ritz Barra de São Miguel:\n"
                "conforto e sofisticação à beira-mar. Ambientes pensados para seu bem-estar, "
                "gastronomia de alto nível e serviços impecáveis! Perfeito para casais, famílias ou "
                "quem busca tranquilidade com charme e praticidade.\n\n"
                "✅ Pacote: voos + 7 noites\n"
                "📅 Saída: 01/11/25 → 08/11/25"
            ),
            parse_mode="Markdown"
        )
        context.user_data['choice'] = 'Ritz Barra de São Miguel'
        await ask_reservation(update, context)

    elif user_input == '3':
        await update.message.reply_text(
            (
                "Comece 2026 a bordo do MSC Seaview! 🚢\n\n"
                "Embarque em Santos no dia 17/01/26 para 7 noites inesquecíveis, com paradas em "
                "Búzios, Salvador e Maceió.\n\n"
                "A bordo, desfrute de:\n"
                "🍽️ Restaurantes premiados\n"
                "🌅 Bares com vista para o mar\n"
                "🏊 Piscinas panorâmicas\n"
                "💆 Spa completo\n"
                "🎭 Teatro e lojas\n"
                "✨ Atrações exclusivas como a Infinity Bridge e o MSC Yacht Club\n\n"
                "✅ Cabine com varanda a partir de 12x de R$ 605,26 por pessoa."
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