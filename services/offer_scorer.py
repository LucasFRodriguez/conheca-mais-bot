
from decimal import Decimal, InvalidOperation


def safe_decimal(value):
    """
    Converte valores numericos sem deixar dados
    invalidos interromperem a pontuacao.
    """

    if value is None or isinstance(value, bool):
        return None

    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None

    if not number.is_finite():
        return None

    return number


def score_offer(offer):
    """
    Calcula a pontuacao de uma oferta.

    Prioridades:
    - Comissao: ate 35 pontos
    - Desconto: ate 30 pontos
    - Avaliacao: ate 20 pontos
    - Vendas: ate 15 pontos

    Pontuacao maxima: 100.
    """

    score = 0

    # 1. COMISSAO DE AFILIADO
    # O adaptador da Shopee fornece a taxa em %.
    commission_rate = safe_decimal(
        offer.get("commission_rate")
    )

    if commission_rate is not None:
        if 0 <= commission_rate <= 100:

            if commission_rate >= 20:
                score += 35
            elif commission_rate >= 15:
                score += 30
            elif commission_rate >= 10:
                score += 20
            elif commission_rate >= 5:
                score += 10

    # 2. DESCONTO
    # Primeiro, usa o percentual informado pela API.
    discount_rate = safe_decimal(
        offer.get("discount_rate")
    )

    # Se nao houver percentual valido, tenta calcular
    # usando um preco original confirmado.
    if (
        discount_rate is None
        or not 0 <= discount_rate <= 100
    ):
        discount_rate = None

        original_price = safe_decimal(
            offer.get("original_price")
        )

        current_price = safe_decimal(
            offer.get("current_price")
        )

        if (
            original_price is not None
            and current_price is not None
            and original_price > current_price > 0
        ):
            discount_rate = (
                (original_price - current_price)
                / original_price
            ) * 100

    if discount_rate is not None:

        if discount_rate >= 50:
            score += 30
        elif discount_rate >= 30:
            score += 25
        elif discount_rate >= 20:
            score += 15
        elif discount_rate >= 10:
            score += 5

    # 3. AVALIACAO
    rating = safe_decimal(
        offer.get("rating")
    )

    if rating is not None:
        if 0 <= rating <= 5:

            if rating >= Decimal("4.8"):
                score += 20
            elif rating >= Decimal("4.5"):
                score += 15
            elif rating >= Decimal("4.0"):
                score += 10

    # 4. QUANTIDADE DE VENDAS
    sales = safe_decimal(
        offer.get("sales")
    )

    if sales is not None and sales >= 0:

        if sales >= 1000:
            score += 15
        elif sales >= 500:
            score += 10
        elif sales >= 100:
            score += 5

    return score
