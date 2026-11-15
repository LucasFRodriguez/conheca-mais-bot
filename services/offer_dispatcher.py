
from services.publisher import publish_message
from services.deduplicator import save_published_offer

from logger_config import logger


async def dispatch_offers(bot, processed_offers):
    """Publica ofertas processadas e registra as publicações."""

    for offer in processed_offers:

        try:
            await publish_message(
                bot,
                offer["message"]
            )

            save_published_offer(offer["offer_id"])

            logger.info(
                f"Oferta publicada: {offer['title']}"
            )

        except Exception:
            logger.exception(
                f"Erro ao publicar: {offer['title']}"
            )
