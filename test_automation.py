
import os
import asyncio

from dotenv import load_dotenv
from telegram import Bot

from marketplaces.collector import get_all_offers
from services.offer_formatter import format_offer
from services.publisher import publish_message
from services.offer_validator import validate_offer
from services.deduplicator import (
    is_already_published,
    save_published_offer
)

from logger_config import logger

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def main():
    logger.info("Iniciando automação do Conheça Mais.")

    if not TOKEN:
        logger.error("Token não encontrado no arquivo .env")
        raise ValueError("Token não encontrado no arquivo .env")

    offers = get_all_offers()

    logger.info(f"Total de ofertas encontradas: {len(offers)}")

    bot = Bot(token=TOKEN)
    await bot.initialize()

    try:
        for offer in offers:
            try:
                validate_offer(offer)

            except ValueError as error:
                logger.warning(
                    f"Oferta inválida: {offer.get('title', 'Sem título')} | Motivo: {error}"
                )
                continue

            offer_id = offer["offer_id"]

            if is_already_published(offer_id):
                logger.info(
                    f"Oferta ignorada (já publicada): {offer['title']}"
                )
                continue

            try:    

                message = format_offer(offer)

                await publish_message(bot, message)

                save_published_offer(offer_id)

                logger.info(
                    f"Oferta publicada com sucesso: {offer['title']}"
                )

            except Exception:
                logger.exception(
                    f"Erro ao processar oferta: {offer['title']}"
                )
                continue

    finally:
        await bot.shutdown()

    logger.info("Automação finalizada.")


if __name__ == "__main__":
    asyncio.run(main())
