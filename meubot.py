import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from datetime import datetime
import pytz
from cachetools import TTLCache

# Configuração de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis globais
TOKEN = "6942272197:AAG_caCl5wdbYAHbu2tf1yUP7lXNSslVuwk"

# Informações específicas de localização
localizacao = {
    "PAIS": "Brasil",
    "ESTADO": "Alagoas",
    "MUNICIPIO": "Maceió",
}

# Criação do cache com uma capacidade de 1 item e tempo de vida de 60 segundos
cache = TTLCache(maxsize=1, ttl=60)

# Função para enviar mensagens
def enviar_mensagem(chat_id, mensagem):
    context.bot.send_message(chat_id, mensagem)

# Função para exibir a hora e o fuso horário atual
def handle_horario(update, context):
    chat_id = update.effective_chat.id
    name = update.effective_user.first_name

    # Verifica se a resposta está em cache
    if "horario" in cache:
        response = cache["horario"]
    else:
        # Obtém a hora e o fuso horário atual
        now = datetime.now()
        user_location = update.effective_user.location
        tz = pytz.timezone(user_location.timezone) if user_location else pytz.timezone('America/Maceio')
        hora_atual = now.astimezone(tz).strftime("%H:%M:%S")
        periodo_dia = get_periodo_dia(now.hour)

        # Monta a resposta
        response = f"{name}, agora são {hora_atual} {periodo_dia} do {localizacao['PAIS']}, {localizacao['ESTADO']}, {localizacao['MUNICIPIO']}."

        # Armazena a resposta no cache
        cache["horario"] = response

    # Envia a mensagem com a hora e o fuso horário
    enviar_mensagem(chat_id, response)

# Funções de saudação e ajuda
def handle_greeting(update, context):
    chat_id = update.effective_chat.id
    name = update.effective_user.first_name

    # Mensagem de saudação
    saudacao = f"Oi {name}, se você está me acionando é porque precisa de algo, não é mesmo?"

    # Mensagens de opções
    opcoes = [
        "/ajuda - Tô ferrado(a)",
        "/contato - Quero falar com o boss",
        "/horario - Tô perdido na hora",
    ]

    # Envia as mensagens
    enviar_mensagem(chat_id, saudacao)
    for opcao in opcoes:
        enviar_mensagem(chat_id, opcao)

# Função de boas-vindas
def handle_start(update, context):
    chat_id = update.effective_chat.id
    name = update.effective_user.first_name

    # Mensagem de boas-vindas
    boas_vindas = f"Oi {name}! Eu sou o seu assistente virtual. Aqui estão algumas coisas que eu posso fazer por você:"
    opcoes = [
        "/ajuda - Mostra as opções de ajuda",
        "/contato - Envia uma mensagem para o administrador",
        "/horario - Mostra a hora atual",
    ]

    # Envia a mensagem de boas-vindas
    enviar_mensagem(chat_id, boas_vindas)
    for opcao in opcoes:
        enviar_mensagem(chat_id, opcao)

# Função de ajuda
def handle_help(update, context):
    chat_id = update.effective_chat.id
    enviar_mensagem(chat_id, "Então você quer uma ajudinha, não é mesmo?")

# Função de contato
def handle_contact(update, context):
    chat_id = update.effective_chat.id
    enviar_mensagem(chat_id, "Poxa, tente lá e veja se o chefe te responde: @arinelson")

# Função para obter o período do dia
def get_periodo_dia(hour):
    if 5 <= hour < 12:
        return "da manhã"
    elif 12 <= hour < 18:
        return "da tarde"
    else:
        return "da noite"

# Inicia o bot
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# Adiciona os handlers
dispatcher.add_handler(CommandHandler("start", handle_start))
dispatcher.add_handler(CommandHandler("ajuda", handle_help))
dispatcher.add_handler(CommandHandler("contato", handle_contact))
dispatcher.add_handler(CommandHandler("horario", handle_horario))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_greeting))

# Inicia o polling
updater.start_polling()
updater.idle()
