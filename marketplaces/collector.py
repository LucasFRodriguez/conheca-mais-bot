
import logging
import time

from marketplaces.shopee import get_offers as get_shopee_offers


logger = logging.getLogger(__name__)


# Consultas da Shopee que vamos utilizar.
SEARCHES = [
    {
        "name": "Produtos gerais",
        "keyword": None,
        "page": 1,
        "limit": 20,
    },
    {
        "name": "Fones - pagina 1",
        "keyword": "fone",
        "page": 1,
        "limit": 5,
    },
    {
        "name": "Fones - pagina 2",
        "keyword": "fone",
        "page": 2,
        "limit": 5,
    },
]


def get_all_offers():
    """
    Busca ofertas reais da Shopee em diferentes consultas.

    - Continua caso uma consulta falhe.
    - Remove produtos repetidos pelo offer_id.
    - Nao utiliza ofertas ficticias do JSON.
    """

    offers = []
    seen_ids = set()
    successful_searches = 0

    for index, search in enumerate(SEARCHES):

        if index > 0:
            # Pequena pausa entre consultas da API.
            time.sleep(2)

        logger.info(
            "Consultando Shopee: %s",
            search["name"]
        )

        try:
            shopee_offers = get_shopee_offers(
                keyword=search["keyword"],
                page=search["page"],
                limit=search["limit"],
            )

            successful_searches += 1

            logger.info(
                "%s: %d produto(s) recebidos.",
                search["name"],
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
                    continue

                seen_ids.add(offer_id)
                offers.append(offer)

        except Exception as error:
            logger.warning(
                "Falha na consulta '%s': %s",
                search["name"],
                type(error).__name__
            )

            # Continua com a proxima consulta.
            continue

    # Se todas as consultas falharem, sinaliza o problema.
    if successful_searches == 0:
        raise RuntimeError(
            "Todas as consultas da Shopee falharam."
        )

    logger.info(
        "Shopee: %d oferta(s) unicas coletadas.",
        len(offers)
    )

    return offers
