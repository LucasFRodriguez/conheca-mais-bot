
def classify_offer(score):
    """Classifica uma oferta de acordo com sua pontuação."""

    if score >= 60:
        return "Excelente"

    elif score >= 40:
        return "Boa"

    elif score >= 20:
        return "Regular"

    return "Baixa"


def filter_offers(offers, minimum_score=40):
    """
    Filtra ofertas pela pontuação mínima
    e mantém a ordem da maior para a menor pontuação.
    """

    approved_offers = []

    for offer in offers:

        score = offer.get("score", 0)

        if score >= minimum_score:
            approved_offers.append(offer)

    approved_offers.sort(
        key=lambda offer: offer.get("score", 0),
        reverse=True
    )

    return approved_offers
