
from decimal import Decimal


def score_offer(offer):
    """
    Calcula uma pontuação para identificar
    ofertas com maior potencial de divulgação.
    """

    score = 0

    commission_rate = offer.get("commission_rate")

    if commission_rate is not None:
        commission_rate = Decimal(str(commission_rate))

        if commission_rate >= 15:
            score += 30
        elif commission_rate >= 10:
            score += 20
        elif commission_rate >= 5:
            score += 10

    rating = offer.get("rating")

    if rating is not None:
        rating = Decimal(str(rating))

        if rating >= 4.5:
            score += 20
        elif rating >= 4.0:
            score += 10

    original_price = offer.get("original_price")
    current_price = offer.get("current_price")

    if original_price and current_price:
        original_price = Decimal(str(original_price))
        current_price = Decimal(str(current_price))

        if original_price > current_price > 0:
            discount = (
                (original_price - current_price)
                / original_price
            ) * 100

            if discount >= 30:
                score += 20
            elif discount >= 15:
                score += 10

    sales = offer.get("sales")

    if sales is not None and sales > 100:
        score += 10

    return score
