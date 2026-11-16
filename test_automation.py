
import os

from dotenv import load_dotenv
from telegram import Bot

from services.offer_processor import process_offers
from services.offer_runner import run_offer_cycle

from logger_config import logger


load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Publicação desativada por padrão.
ENABLE_TELEGRAM_PUBLISHING = (
    os.getenv("ENABLE_TELEGRAM_PUBLISHING", "false").lower() == "true"
)


async def main():

    logger.info("Iniciando automação do Conheça Mais.")

    # Modo seguro: processa as ofertas, mas não publica.
    if not ENABLE_TELEGRAM_PUBLISHING:

        offers = process_offers()

        logger.info(
            f"Modo seguro ativado. {len(offers)} oferta(s) processada(s)."
        )

        logger.info("Nenhuma publicação foi realizada.")

        return

    # Verifica o token somente quando a publicação estiver habilitada.
    if not TOKEN:
        raise ValueError("Token não encontrado no arquivo .env")

    bot = Bot(token=TOKEN)

    await bot.initialize()

    try:
        await run_offer_cycle(bot)

    finally:
        await bot.shutdown()

    logger.info("Automação finalizada.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
