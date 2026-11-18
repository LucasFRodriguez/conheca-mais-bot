
import os
import json
import time
import hashlib
import requests

from dotenv import load_dotenv

from marketplaces.shopee_adapter import adapt_shopee_product
from services.offer_validator import validate_offer
from services.offer_scorer import score_offer


load_dotenv()

API_URL = "https://open-api.affiliate.shopee.com.br/graphql"

# Escolha a operação que deseja testar:
# "products" = busca produtos
# "campaigns" = busca campanhas
TEST_MODE = "products"


def make_request(query):
    """
    Envia uma consulta autenticada à Shopee Open API.
    """

    app_id = os.getenv("SHOPEE_APP_ID")
    secret = os.getenv("SHOPEE_SECRET")

    if not app_id or not secret:
        raise ValueError(
            "Credenciais da Shopee não encontradas no .env."
        )

    # O corpo utilizado na assinatura precisa ser
    # exatamente o mesmo enviado na requisição.
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

    print("Conectando à Shopee Open API...")

    response = requests.post(
        API_URL,
        headers=headers,
        data=payload.encode("utf-8"),
        timeout=30
    )

    print("Status HTTP:", response.status_code)

    response.raise_for_status()

    return response.json()


def get_query():
    """
    Retorna a consulta GraphQL escolhida.
    """

    if TEST_MODE == "campaigns":
        return """
        {
            shopeeOfferV2(
                page: 1
                limit: 1
            ) {
                nodes {
                    offerName
                    offerLink
                }
            }
        }
        """

    if TEST_MODE == "products":
        return """
        {
            productOfferV2(
                page: 1
                limit: 1
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
        """

    raise ValueError(
        "TEST_MODE inválido. Use 'products' ou 'campaigns'."
    )


def main():

    query = get_query()

    try:
        result = make_request(query)

    except requests.RequestException as error:
        print(
            "Falha de comunicação com a Shopee:",
            type(error).__name__
        )
        return

    except ValueError as error:
        print("Erro de configuração:", error)
        return

    # Verifica os erros GraphQL.
    if result.get("errors"):
        print("\nA Shopee retornou erros na consulta:")

        for error in result["errors"]:
            print(
                error.get("message", "Erro desconhecido")
            )

        return

    data = result.get("data") or {}

    if TEST_MODE == "campaigns":

        connection = data.get("shopeeOfferV2")

        if connection is None:
            print("Resposta sem dados de campanhas.")
            return

        campaigns = connection.get("nodes") or []

        print(
            f"\nCampanhas encontradas: {len(campaigns)}"
        )

        for campaign in campaigns:
            print("\n" + "=" * 45)
            print("CAMPANHA SHOPEE")
            print("=" * 45)

            print(
                "Nome:",
                campaign.get("offerName")
            )

            print(
                "Link disponível:",
                bool(campaign.get("offerLink"))
            )

    elif TEST_MODE == "products":

        connection = data.get("productOfferV2")

        if connection is None:
            print("Resposta sem dados de produtos.")
            return

        products = connection.get("nodes") or []

        print(
            f"\nProdutos encontrados: {len(products)}"
        )

        for product in products:

            try:
                offer = adapt_shopee_product(product)

                validate_offer(offer)

                score = score_offer(offer)

                print("\n" + "=" * 45)
                print("PRODUTO REAL DA SHOPEE")
                print("=" * 45)

                print("Produto:", offer["title"])
                print(
                    "Preço mínimo:",
                    offer["current_price"]
                )
                print(
                    "Comissão (%):",
                    offer["commission_rate"]
                )
                print("Avaliação:", offer["rating"])
                print("Vendas:", offer["sales"])
                print("Pontuação:", score)

                print(
                    "Link de afiliado disponível:",
                    bool(offer["affiliate_url"])
                )

            except (ValueError, TypeError) as error:
                print("Produto ignorado:", error)

    print("\nTeste finalizado.")


if __name__ == "__main__":
    main()
