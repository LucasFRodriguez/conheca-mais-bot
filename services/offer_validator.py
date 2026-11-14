
from decimal import Decimal, InvalidOperation
from urllib.parse import urlparse


def validate_offer(offer):
    required_fields = [
        "offer_id",
        "title",
        "current_price",
        "marketplace",
        "affiliate_url"
    ]

    for field in required_fields:
        if field not in offer or offer[field] is None or offer[field] == "":
            raise ValueError(f"Campo obrigatório ausente: {field}")

    try:
        current_price = Decimal(str(offer["current_price"]))

        if not current_price.is_finite() or current_price <= 0:
            raise ValueError("Preço atual inválido.")

        original_price = offer.get("original_price")

        if original_price is not None:
            original_price = Decimal(str(original_price))

            if not original_price.is_finite() or original_price <= 0:
                raise ValueError("Preço original inválido.")

    except InvalidOperation:
        raise ValueError("Preço informado não é válido.")

    url = urlparse(offer["affiliate_url"])

    if url.scheme not in ("http", "https") or not url.netloc:
        raise ValueError("Link de afiliado inválido.")

    return True
