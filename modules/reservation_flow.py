from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters)


from modules.queue.token import generate_user_token


async def collect_reservation_intent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get('next')
    text = update.message.text.strip().lower()

    if step == 'reserve':
        if text in ['sim', 's']:
            # pega a escolha feita anteriormente
            choice = context.user_data.get('choice')

            # se for 1 ou 3, pula direto para a acomodação
            if choice in ['Explora III', 'MSC Seaview']:
                await update.message.reply_text(
                    "Perfeito! ✨ Agora nos diga: em qual acomodação gostaria de viajar? "
                    "(single / duplo / triplo / quádruplo / suíte / cabine com varanda)"
                )
                context.user_data['next'] = 'accommodation'

            # caso contrário, pergunta o transporte
            else:
                await update.message.reply_text(
                    "Perfeito! ✨ Qual meio de transporte você gostaria de reservar? (carro / moto)"
                )
                context.user_data['next'] = 'transport'

        elif text in ['não', 'n']:
            await update.message.reply_text(
                "Tudo bem! 😊 Ficamos à disposição se quiser ver outras viagens."
            )
            context.user_data.clear()
        else:
            await update.message.reply_text(
                "Responda apenas com sim ou não.", parse_mode="Markdown"
            )

    elif step == 'transport':
        transport = text.lower()
        if transport in ['carro', 'moto']:
            context.user_data['transport'] = transport
            await update.message.reply_text(
                f"Excelente! Você escolheu viajar de {transport}. ✈️🚌🚢\n\n"
                "Agora, nos diga: em qual acomodação gostaria de viajar? "
                "(single / duplo / triplo / quádruplo / suíte / cabine com varanda)",
                parse_mode="Markdown"
            )
            context.user_data['next'] = 'accommodation'
        else:
            await update.message.reply_text("Informe apenas: carro ou moto.")

    elif step == 'accommodation':
        accommodation = text.lower()
        if accommodation in ['single', 'duplo', 'triplo', 'quádruplo', 'suíte', 'cabine com varanda']:
            context.user_data['accommodation'] = accommodation
            await update.message.reply_text(
                f"Excelente! Você escolheu a acomodação {accommodation}. 🛏️🏨\n\n"
                "Agora nos diga: em qual data gostaria de viajar? (ex: 15/11/2025)",
                parse_mode='Markdown'
            )
            context.user_data['next'] = 'date'

    elif step == 'date':
        date = text
        choice = context.user_data.get('choice', 'viagem não especificada')
        transport = context.user_data.get('transport', 'não especificado')
        phone = context.user_data.get('phone')

        if phone:
            token = generate_user_token(phone)
            context.user_data['token'] = token
            print(f"Token gerado para {phone}: {token}")
        else:
            token = None
            print("⚠️ Nenhum número de telefone encontrado — token não gerado")

        context.user_data["session_finished"] = True

        message = (
            f"Perfeito! 🎉\n\nResumo da sua intenção de reserva:\n"
            f"• Viagem: *{choice}*\n"
        )

        if transport:
            message += f"• Transporte: *{transport}*\n"
        message += (
            f"• Data desejada: *{date}*\n\n"
            "Um consultor Agaxtur entrará em contato para continuar o atendimento. Obrigado!"
        )

        await update.message.reply_text(message, parse_mode="Markdown")

        for key in list(context.user_data.keys()):
            if key not in ("session_finished", "token"):
                del context.user_data[key]
