import random
from twilio.rest import Client

def enviar_mensagem_lead():
    """
    Envia uma mensagem SMS para um dos consultores escolhidos aleatoriamente,
    informando que há um novo lead disponível.
    """

    # Lista de consultores (números no formato internacional)
    consultores = ["+5511970205186", "+5511940592829"]

    # Credenciais Twilio (token exposto — apenas para ambiente local)
    account_sid = "AC961f9c4ebe2f017aab6f0166096691e2"
    auth_token = "4f1df1896f61b38b2749f14381bcb05d"

    # Inicializa o cliente Twilio
    client = Client(account_sid, auth_token)

    # Escolhe aleatoriamente um dos consultores
    destinatario = random.choice(consultores)

    # Envia a mensagem
    message = client.messages.create(
        from_="+19152882006",
        to=destinatario,
        body="📞 Novo lead disponível para atendimento!"
    )

    print(f"✅ Mensagem enviada para {destinatario}: {message.sid}")
