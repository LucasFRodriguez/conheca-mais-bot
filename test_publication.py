
import os
import asyncio

from dotenv import load_dotenv
from telegram import Bot

from services.publisher import publish_message

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def main():
    if not TOKEN:
        raise ValueError("Token não encontrado no arquivo .env")

    bot = Bot(token=TOKEN)

    await bot.initialize()

    try:
        message = (
            "🔥 OFERTA DE TESTE — CONHEÇA MAIS!\n\n"
            "Produto: Fone Bluetooth\n"
            "Preço: R$ 49,90\n\n"
            "🛒 Confira a oferta:\n"
            "https://example.com\n\n"
            "⚠️ Esta é uma publicação fictícia para testar o bot."
        )

        await publish_message(bot, message)

        print("Mensagem publicada com sucesso!")

    finally:
        await bot.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
