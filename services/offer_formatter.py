
from decimal import Decimal, InvalidOperation


def format_price(price):
    """Formata um valor para o padrão brasileiro."""

    try:
        value = Decimal(str(price))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Valor inválido para formatação de preço.")

    if not value.is_finite() or value <= 0:
        raise ValueError("O preço deve ser um número positivo.")

    return (
        f"R$ {value:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def format_offer(offer):
    """Recebe os dados de uma oferta e gera uma mensagem para o Telegram."""

    required_fields = [
        "title",
        "current_price",
        "marketplace",
        "affiliate_url"
    ]

    # Verifica os campos obrigatórios
    for field in required_fields:
        if offer.get(field) in (None, ""):
            raise ValueError(f"Campo obrigatório não informado: {field}")

    title = str(offer["title"]).strip()
    marketplace = str(offer["marketplace"]).strip()
    affiliate_url = offer["affiliate_url"]

    if not title or not marketplace:
        raise ValueError("Título e marketplace não podem estar vazios.")

    current_price = Decimal(str(offer["current_price"]))

    if not current_price.is_finite() or current_price <= 0:
        raise ValueError("O preço atual deve ser maior que zero.")

    # Início da mensagem
    message = (
        "🔥 OFERTA ESPECIAL!\n\n"
        f"🛍️ {title}\n\n"
    )

    original_price = offer.get("original_price")

    # Exibe desconto somente quando os dois preços permitem calculá-lo
    if original_price is not None:

        try:
            original_price = Decimal(str(original_price))
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError("O preço original é inválido.")

        if not original_price.is_finite() or original_price <= 0:
            raise ValueError("O preço original deve ser maior que zero.")

        if original_price > current_price:

            discount = (
                (original_price - current_price)
                / original_price
            ) * 100

            message += (
                f"De: {format_price(original_price)}\n"
                f"Por: {format_price(current_price)}\n"
                f"💥 Desconto de {discount:.0f}%!\n\n"
            )

        else:
            message += (
                f"💰 Preço: {format_price(current_price)}\n\n"
            )

    else:
        message += (
            f"💰 Preço: {format_price(current_price)}\n\n"
        )

    # Finalização da mensagem
    message += (
        f"🏪 Marketplace: {marketplace}\n\n"
        "🛒 COMPRE AQUI:\n"
        f"{affiliate_url}\n\n"
        "⚡ Aproveite enquanto estiver disponível!"
    )

    return message
