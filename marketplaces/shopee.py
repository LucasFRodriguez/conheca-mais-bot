
import os
import json
import time
import hashlib
import requests

from dotenv import load_dotenv
from marketplaces.shopee_adapter import adapt_shopee_product


load_dotenv()

API_URL = "https://open-api.affiliate.shopee.com.br/graphql"


def get_offers(keyword=None, limit=3):
    """
    Busca produtos reais na Shopee Open API.

    Retorna uma lista de ofertas adaptadas
    para o padrão utilizado pelo Conheça Mais.

    O parâmetro keyword fica reservado para
    futuras pesquisas por palavra-chave.
    """

    # 1. Verificar as credenciais
    app_id = os.getenv("SHOPEE_APP_ID")
    secret = os.getenv("SHOPEE_SECRET")

    if not app_id or not secret:
        raise ValueError(
            "Credenciais da Shopee não encontradas no .env."
        )

    # 2. Validar o limite da consulta
    if type(limit) is not int or not 1 <= limit <= 20:
        raise ValueError(
            "O limite deve ser um número entre 1 e 20."
        )

    # 3. Consulta GraphQL
    # Usamos o formato simples que já funcionou.
    query = """
    {
        productOfferV2(
            page: 1
            limit: %d
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
        }
    }
    """ % limit

    # 4. Preparar o corpo da requisição
    payload = json.dumps(
        {"query": query},
        separators=(",", ":"),
        ensure_ascii=False
    )

    # 5. Criar o timestamp
    timestamp = str(int(time.time()))

    # 6. Gerar assinatura SHA256
    signature_text = (
        app_id + timestamp + payload + secret
    )

    signature = hashlib.sha256(
        signature_text.encode("utf-8")
    ).hexdigest()

    # 7. Preparar os cabeçalhos
    headers = {
        "Content-Type": "application/json",
        "Authorization": (
            f"SHA256 Credential={app_id}, "
            f"Timestamp={timestamp}, "
            f"Signature={signature}"
        )
    }

    # 8. Consultar a API
    response = requests.post(
        API_URL,
        headers=headers,
        data=payload.encode("utf-8"),
        timeout=30
    )

    # 9. Verificar erros HTTP
    response.raise_for_status()

    # 10. Interpretar a resposta JSON
    result = response.json()

    # 11. Verificar erros GraphQL
    if result.get("errors"):
        messages = [
            error.get(
                "message",
                "Erro desconhecido"
            )
            for error in result["errors"]
        ]

        raise RuntimeError(
            "Erro na Shopee Open API: "
            + "; ".join(messages)
        )

    # 12. Extrair os produtos
    data = result.get("data") or {}

    connection = data.get("productOfferV2")

    if connection is None:
        raise RuntimeError(
            "A Shopee não retornou productOfferV2."
        )

    products = connection.get("nodes") or []

    # 13. Adaptar os produtos
    offers = []

    for product in products:
        try:
            offer = adapt_shopee_product(product)

            # Não aceitar ofertas sem link de afiliado
            affiliate_url = offer.get("affiliate_url")

            if (
                not isinstance(affiliate_url, str)
                or not affiliate_url.startswith(
                    ("https://", "http://")
                )
            ):
                print(
                    "Produto ignorado: "
                    "link de afiliado inválido."
                )
                continue

            offers.append(offer)

        except (ValueError, TypeError) as error:
            print(
                f"Produto ignorado: {error}"
            )

    # 14. Devolver as ofertas ao sistema
    return offers
