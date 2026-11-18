
from marketplaces.shopee import get_offers
from services.offer_validator import validate_offer
from services.offer_scorer import score_offer


def main():
    print("Buscando produtos reais da Shopee...")

    offers = get_offers(limit=1)

    print(f"\nOfertas recebidas: {len(offers)}")

    for offer in offers:
        validate_offer(offer)

        score = score_offer(offer)

        print("\n" + "-" * 40)
        print("Produto:", offer["title"])
        print("Preço mínimo:", offer["current_price"])
        print("Comissão (%):", offer["commission_rate"])
        print("Pontuação:", score)
        print("Link de afiliado:", bool(offer["affiliate_url"]))

    print("\nTeste de integração concluído!")


if __name__ == "__main__":
    main()
