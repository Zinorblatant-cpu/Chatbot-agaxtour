import time
from telegram import Update
from telegram.ext import ContextTypes
import requests

WEBHOOK_URL = "https://seilapora.app.n8n.cloud/webhook-test/PushInformationsOfBot"
TIME_LIMIT = 600  # 10 minutos

async def check_timeout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("session_finished"):
        return False

    start_time = context.user_data.get("start_time")
    if start_time is None:
        context.user_data["start_time"] = time.time()
        return False

    elapsed = time.time() - start_time
    if elapsed >= TIME_LIMIT:
        await update.message.reply_text(
            "⏰ Parece que você demorou muito pra finalizar, começe de novo com o /start."
        )
        
        phone = context.user_data.get("phone", "Não informado")
        data = {
            "lead": "NOT qualified lead",
            "phone": phone,
        }

        try:
            response = requests.post(WEBHOOK_URL, json=data, timeout=10)
            response.raise_for_status()
            print(f"✅ Dados enviados com sucesso: {response.status_code}")
        except requests.RequestException as e:
            print(f"❌ Erro ao enviar dados para o webhook: {e}")

        # limpa tudo, exceto token
        for key in list(context.user_data.keys()):
            if key not in ("session_finished", "token"):
                del context.user_data[key]

        return True

    return False
