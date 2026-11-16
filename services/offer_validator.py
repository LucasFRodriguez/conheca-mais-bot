
from math import isfinite
from urllib.parse import urlparse


def validate_offer(offer):
    """
    Valida os dados essenciais e opcionais de uma oferta.
    """

    required_fields = [
        "offer_id",
        "title",
        "current_price",
        "marketplace",
        "affiliate_url"
    ]

    # Verifica os campos obrigatórios
    for field in required_fields:
        if field not in offer or offer[field] in (None, ""):
            raise ValueError(f"Campo obrigatório ausente: {field}")

    # Valida o preço atual
    try:
        current_price = float(offer["current_price"])
    except (TypeError, ValueError):
        raise ValueError("Preço atual inválido.")

    if not isfinite(current_price) or current_price <= 0:
        raise ValueError("Preço atual deve ser maior que zero.")

    # Valida o preço original, caso exista
    original_price = offer.get("original_price")

    if original_price is not None:
        try:
            original_price = float(original_price)
        except (TypeError, ValueError):
            raise ValueError("Preço original inválido.")

        if not isfinite(original_price) or original_price <= 0:
            raise ValueError("Preço original deve ser maior que zero.")

        if original_price < current_price:
            raise ValueError(
                "Preço original não pode ser menor que o preço atual."
            )

    # Valida os links
    for field in ["affiliate_url", "product_url", "image_url"]:
        url = offer.get(field)

        if url:
            parsed_url = urlparse(url)

            if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
                raise ValueError(f"URL inválida: {field}")

    # Valida campos numéricos opcionais
    numeric_fields = [
        "commission",
        "commission_rate",
        "sales",
        "rating"
    ]

    for field in numeric_fields:
        value = offer.get(field)

        if value is not None:
            try:
                value = float(value)
            except (TypeError, ValueError):
                raise ValueError(f"Valor inválido no campo: {field}")

            if not isfinite(value) or value < 0:
                raise ValueError(f"Valor inválido no campo: {field}")

    # Avaliação deve estar entre 0 e 5
    rating = offer.get("rating")

    if rating is not None and float(rating) > 5:
        raise ValueError("A avaliação deve estar entre 0 e 5.")

    # Comissão percentual deve estar entre 0 e 100
    commission_rate = offer.get("commission_rate")

    if commission_rate is not None and float(commission_rate) > 100:
        raise ValueError("A comissão percentual deve estar entre 0 e 100.")

    return True
