from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)
import requests

from modules.queue.token import generate_user_token
from modules.gerenciamentoDeConsultores import enviar_mensagem_lead

WEBHOOK_URL = "https://seilapora.app.n8n.cloud/webhook-test/PushInformationsOfBot"

async def collect_reservation_intent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get('next')
    text = update.message.text.strip().lower()

    if step == 'reserve':
        if text in ['sim', 's']:
            choice = context.user_data.get('choice')

            await update.message.reply_text(
                    "Perfeito! ✨ Agora nos diga: em qual acomodação gostaria de viajar? "
                    "(single / duplo / triplo / quádruplo / suíte / cabine com varanda)"
                )
            context.user_data['next'] = 'accommodation'
            
        elif text in ['não', 'n']:
            await update.message.reply_text(
                "Tudo bem! 😊 Ficamos à disposição se quiser ver outras viagens."
            )
            context.user_data.clear()
        else:
            await update.message.reply_text(
                "Responda apenas com sim ou não.", parse_mode="Markdown"
            )

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

        message += (
            f"• Data desejada: *{date}*\n\n"
            "Um consultor Agaxtur entrará em contato para continuar o atendimento. Obrigado!"
        )

        await update.message.reply_text(message, parse_mode="Markdown")

        # 🔹 monta o JSON incluindo o telefone
        data = {
            "choice": choice,
            "date": date,
            "lead": "qualified lead",
            **({"transport": transport} if transport else {}),
            **({"phone": phone} if phone else {})
        }

        try:
            response = requests.post(WEBHOOK_URL, json=data, timeout=10)
            response.raise_for_status()
            print(f"✅ Dados enviados com sucesso: {response.status_code}")
        except requests.RequestException as e:
            print(f"❌ Erro ao enviar dados para o webhook: {e}")

        # limpa o contexto (mantendo apenas token)
        for key in list(context.user_data.keys()):
            if key not in ("session_finished", "token"):
                del context.user_data[key]
            
        enviar_mensagem_lead()