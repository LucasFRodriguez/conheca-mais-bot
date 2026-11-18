
import logging

from marketplaces.shopee import get_offers as get_shopee_offers


logger = logging.getLogger(__name__)


def get_all_offers():
    """
    Coleta somente ofertas reais da Shopee.

    O JSON de testes não participa da publicação.
    """

    offers = []

    try:
        shopee_offers = get_shopee_offers(limit=10)

        offers.extend(shopee_offers)

        logger.info(
            "Shopee: %d ofertas coletadas.",
            len(shopee_offers)
        )

    except Exception as error:
        logger.error(
            "Falha ao buscar ofertas da Shopee: %s",
            type(error).__name__
        )

    return offers
