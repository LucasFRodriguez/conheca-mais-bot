
from marketplaces.collector import get_all_offers

from services.offer_validator import validate_offer
from services.offer_formatter import format_offer
from services.deduplicator import is_already_published


def process_offers():
    """Busca, valida e prepara ofertas para publicação."""

    offers = get_all_offers()

    processed_offers = []

    print(f"Total de ofertas encontradas: {len(offers)}")

    for offer in offers:

        try:
            validate_offer(offer)

            offer_id = offer["offer_id"]

            if is_already_published(offer_id):
                print(f"Oferta já publicada: {offer['title']}")
                continue

            message = format_offer(offer)

            processed_offers.append({
                "offer_id": offer_id,
                "title": offer["title"],
                "message": message
            })

            print(f"Oferta processada: {offer['title']}")

        except ValueError as error:
            print(
                f"Oferta inválida: "
                f"{offer.get('title', 'Sem título')} | {error}"
            )

    return processed_offers
