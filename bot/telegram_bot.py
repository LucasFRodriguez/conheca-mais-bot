
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# Carrega as variáveis do arquivo .env
load_dotenv()

# Recupera o token do Telegram
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# Função executada quando alguém envia /start
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "Olá! 👋\n\n"
        "Eu sou o Conheça Mais Ofertas!\n"
        "Estou iniciando minhas atividades. 🚀\n\n"
        "Em breve, você poderá encontrar ótimas ofertas por aqui!"
    )


# Inicialização do bot
def main():

    if not TOKEN:
        raise ValueError(
            "Token não encontrado. Verifique o arquivo .env."
        )

    app = Application.builder().token(TOKEN).build()

    # Registra o comando /start
    app.add_handler(CommandHandler("start", start))

    print("Conheça Mais iniciado com sucesso!")
    print("Aguardando mensagens no Telegram...")

    # Mantém o bot funcionando
    app.run_polling()


if __name__ == "__main__":
    main()
