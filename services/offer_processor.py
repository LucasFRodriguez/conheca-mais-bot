
from marketplaces.collector import get_all_offers

from services.offer_validator import validate_offer
from services.offer_formatter import format_offer
from services.deduplicator import is_already_published
from services.offer_scorer import score_offer
from services.offer_filter import filter_offers


# Quantidade máxima de ofertas selecionadas por ciclo
MAX_OFFERS_PER_CYCLE = 3


def process_offers():
    """Busca, valida, classifica e prepara ofertas."""

    offers = get_all_offers()

    processed_offers = []

    print(f"Total de ofertas encontradas: {len(offers)}")

    for offer in offers:

        try:
            # Valida as informações da oferta
            validate_offer(offer)

            offer_id = offer["offer_id"]

            # Impede ofertas duplicadas
            if is_already_published(offer_id):
                print(
                    f"Oferta já publicada: {offer['title']}"
                )
                continue

            # Calcula a pontuação
            score = score_offer(offer)

            # Formata a mensagem
            message = format_offer(offer)

            processed_offers.append({
                "offer_id": offer_id,
                "title": offer["title"],
                "score": score,
                "message": message
            })

            print(
                f"Oferta processada: {offer['title']} "
                f"| Pontuação: {score}"
            )

        except (ValueError, TypeError) as error:
            print(
                f"Oferta inválida: "
                f"{offer.get('title', 'Sem título')} | {error}"
            )

    # Filtra ofertas com pontuação mínima de 40
    approved_offers = filter_offers(
        processed_offers,
        minimum_score=40
    )

    print(
        f"Ofertas aprovadas pelo filtro: "
        f"{len(approved_offers)}"
    )

    # Seleciona no máximo 3 ofertas por execução
    selected_offers = approved_offers[
        :MAX_OFFERS_PER_CYCLE
    ]

    print(
        f"Ofertas selecionadas para o ciclo: "
        f"{len(selected_offers)}"
    )

    return selected_offers
