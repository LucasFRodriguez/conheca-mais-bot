
import os
import json
import time
import hashlib
import logging

import requests
from dotenv import load_dotenv

from marketplaces.shopee_adapter import adapt_shopee_product


load_dotenv()

logger = logging.getLogger(__name__)

API_URL = "https://open-api.affiliate.shopee.com.br/graphql"


def get_offers(keyword=None, limit=10, page=1):
    """
    Busca produtos reais na Shopee Open API.

    keyword: palavra-chave opcional
    limit: quantidade máxima de produtos
    page: página solicitada

    Retorna ofertas adaptadas ao Conheça Mais.
    """

    app_id = os.getenv("SHOPEE_APP_ID")
    secret = os.getenv("SHOPEE_SECRET")

    if not app_id or not secret:
        raise ValueError(
            "Credenciais da Shopee não encontradas no .env."
        )

    if type(limit) is not int or not 1 <= limit <= 20:
        raise ValueError(
            "O limite deve estar entre 1 e 20."
        )

    if type(page) is not int or page < 1:
        raise ValueError(
            "A página deve ser um número inteiro positivo."
        )

    # Monta os parâmetros da consulta GraphQL.
    if keyword is not None:
        if not isinstance(keyword, str) or not keyword.strip():
            raise ValueError(
                "Informe uma palavra-chave válida."
            )

        if len(keyword) > 100:
            raise ValueError(
                "A palavra-chave deve ter até 100 caracteres."
            )

        keyword_value = json.dumps(
            keyword.strip(),
            ensure_ascii=False
        )

        search_parameters = (
            f"keyword: {keyword_value}\n"
            f"            sortType: 1\n"
            f"            page: {page}\n"
            f"            limit: {limit}"
        )

    else:
        # Sem palavra-chave, fazemos a consulta mais simples.
        # Ela já funcionou nos nossos testes anteriores.
        search_parameters = (
            f"page: {page}\n"
            f"            limit: {limit}"
        )

    query = """
    {
        productOfferV2(
            %s
        ) {
            nodes {
                itemId
                shopId
                productName
                priceMin
                priceMax
                commissionRate
                ratingStar
                sales
                priceDiscountRate
                imageUrl
                productLink
                offerLink
            }
            pageInfo {
                hasNextPage
            }
        }
    }
    """ % search_parameters

    # O corpo enviado deve ser exatamente o mesmo
    # usado no cálculo da assinatura SHA256.
    payload = json.dumps(
        {"query": query},
        separators=(",", ":"),
        ensure_ascii=False
    )

    timestamp = str(int(time.time()))

    signature_text = (
        app_id + timestamp + payload + secret
    )

    signature = hashlib.sha256(
        signature_text.encode("utf-8")
    ).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "Authorization": (
            f"SHA256 Credential={app_id}, "
            f"Timestamp={timestamp}, "
            f"Signature={signature}"
        )
    }

    # Consulta a API da Shopee.
    response = requests.post(
        API_URL,
        headers=headers,
        data=payload.encode("utf-8"),
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    # Não trata erros GraphQL como listas vazias.
    if result.get("errors"):
        messages = [
            error.get("message", "Erro desconhecido")
            for error in result["errors"]
        ]

        raise RuntimeError(
            "Erro na Shopee Open API: "
            + "; ".join(messages)
        )

    connection = (
        result.get("data") or {}
    ).get("productOfferV2")

    if connection is None:
        raise RuntimeError(
            "A Shopee não retornou productOfferV2."
        )

    products = connection.get("nodes") or []

    # Informações de paginação retornadas pela Shopee.
    page_info = connection.get("pageInfo") or {}

    print("Página solicitada:", page)
    print(
        "Próxima página disponível:",
        page_info.get("hasNextPage")
    )
    print("Produtos recebidos:", len(products))

    offers = []

    for product in products:
        try:
            offer = adapt_shopee_product(product)

            affiliate_url = offer.get("affiliate_url")

            if (
                not isinstance(affiliate_url, str)
                or not affiliate_url.startswith("https://")
            ):
                logger.warning(
                    "Produto ignorado: link de afiliado inválido."
                )
                continue

            offers.append(offer)

        except (ValueError, TypeError) as error:
            logger.warning(
                "Produto ignorado: %s",
                error
            )

    return offers
