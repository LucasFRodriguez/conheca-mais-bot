
from decimal import Decimal


def format_price(price):
    """Formata um valor para o padrão brasileiro."""
    value = Decimal(str(price))
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_offer(offer):
    """Recebe os dados de uma oferta e gera uma mensagem para o Telegram."""

    required_fields = [
        "title",
        "current_price",
        "marketplace",
        "affiliate_url"
    ]

    # Verifica se todos os campos obrigatórios foram informados
    for field in required_fields:
        if not offer.get(field):
            raise ValueError(f"Campo obrigatório não informado: {field}")

    title = offer["title"]
    current_price = Decimal(str(offer["current_price"]))
    marketplace = offer["marketplace"]
    affiliate_url = offer["affiliate_url"]

    if current_price <= 0:
        raise ValueError("O preço atual deve ser maior que zero.")

    # Monta a mensagem
    message = (
        f"🔥 OFERTA ESPECIAL!\n\n"
        f"🛍️ {title}\n\n"
    )

    original_price = offer.get("original_price")

    if original_price is not None:
        original_price = Decimal(str(original_price))

        if original_price <= 0:
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

    message += (
        f"🏪 Marketplace: {marketplace}\n\n"
        f"🛒 COMPRE AQUI:\n"
        f"{affiliate_url}\n\n"
        f"⚡ Aproveite enquanto estiver disponível!"
    )

    return message
