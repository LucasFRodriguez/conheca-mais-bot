
import logging
import time

from marketplaces.shopee import get_offers as get_shopee_offers


logger = logging.getLogger(__name__)


# Configuracoes da coleta.
PAGES_TO_SEARCH = [1, 2, 3]
PRODUCTS_PER_PAGE = 20
PAUSE_BETWEEN_REQUESTS = 2


def get_all_offers():
    """
    Busca ofertas reais da Shopee em varias paginas.

    - Consulta diferentes paginas de produtos.
    - Continua quando uma consulta falha.
    - Remove produtos repetidos pelo offer_id.
    - Nao utiliza ofertas ficticias do JSON.
    - Nao publica mensagens no Telegram.
    """

    offers = []
    seen_ids = set()
    successful_searches = 0

    for index, page in enumerate(PAGES_TO_SEARCH):

        if index > 0:
            # Pequena pausa entre consultas.
            time.sleep(PAUSE_BETWEEN_REQUESTS)

        logger.info(
            "Consultando Shopee: pagina %d",
            page
        )

        try:
            shopee_offers = get_shopee_offers(
                keyword=None,
                page=page,
                limit=PRODUCTS_PER_PAGE,
            )

            successful_searches += 1

            logger.info(
                "Pagina %d: %d produto(s) recebidos.",
                page,
                len(shopee_offers)
            )

            for offer in shopee_offers:
                offer_id = offer.get("offer_id")

                if not offer_id:
                    logger.warning(
                        "Produto ignorado: ID ausente."
                    )
                    continue

                if offer_id in seen_ids:
                    logger.debug(
                        "Produto repetido ignorado: %s",
                        offer_id
                    )
                    continue

                seen_ids.add(offer_id)
                offers.append(offer)

        except Exception as error:
            logger.warning(
                "Falha ao consultar a pagina %d: %s: %s",
                page,
                type(error).__name__,
                error
            )

            # Continua para a proxima pagina.
            continue

    if successful_searches == 0:
        raise RuntimeError(
            "Todas as consultas da Shopee falharam."
        )

    logger.info(
        "Shopee: %d oferta(s) unicas coletadas em "
        "%d pagina(s) consultada(s) com sucesso.",
        len(offers),
        successful_searches
    )

    return offers