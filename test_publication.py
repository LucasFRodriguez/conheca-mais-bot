
import os
import asyncio

from dotenv import load_dotenv
from telegram import Bot

from services.publisher import publish_message
from services.offer_formatter import format_offer

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def main():

    if not TOKEN:
        raise ValueError("Token não encontrado no arquivo .env")

    # Dados fictícios de uma oferta
    offer = {
        "title": "Fone Bluetooth Sem Fio",
        "current_price": 49.90,
        "original_price": 99.90,
        "marketplace": "Shopee",
        "affiliate_url": "https://example.com"
    }

    # Transforma os dados em uma mensagem
    message = format_offer(offer)

    # Conecta ao Telegram
    bot = Bot(token=TOKEN)

    await bot.initialize()

    try:
        # Publica a oferta no canal
        await publish_message(bot, message)

        print("Oferta publicada com sucesso!")

    finally:
        await bot.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
