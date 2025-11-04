from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from modules.travel_selection import select_travel_option

async def collect_reservation_intent(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            await update.message.reply_text("Responda apenas com sim ou não.", parse_mode="Markdown")

    elif step == 'transport':
        transport = text.lower()
        if transport in ['ônibus', 'onibus', 'avião', 'aviao', 'barco', 'cruzeiro']:
            context.user_data['transport'] = transport
            await update.message.reply_text(
                f"Excelente! Você escolheu viajar de {transport}. ✈️🚌🚢\n\n"
                "Agora, nos diga: em qual acomodação gostaria de viajar? (single / duplo / triplo / quádruplo / suíte / cabine com varanda)",
                parse_mode="Markdown"
            )
            context.user_data['next'] = 'accommodation'
        else:
            await update.message.reply_text("Informe apenas: ônibus, avião ou barco.")

    elif step ==  'accommodation':
        accommodation = text.lower()
        if accommodation in ['single', 'duplo','triplo', 'quádruplo', 'suíte', 'cabine com varanda']:
            context.user_data['accommodation'] = accommodation
            await update.message.reply_text(
                f'Excelete Você escolheu a acomodação {accommodation}. 🛏️🏨\n\n'
                'Agora me diga: Agora, nos diga: em qual data gostaria de viajar? (ex: 15/11/2025)',
                parse_mode='Markdown'
            )
            context.user_data['next'] = 'date'

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
        await select_travel_option(update, context)
