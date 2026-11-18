
from decimal import Decimal, InvalidOperation


def optional_decimal(value):
    """Converte números opcionais com segurança."""
    if value is None or value == "":
        return None

    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None

    if not result.is_finite():
        return None

    return result


def adapt_shopee_product(product):
    """Converte um produto da Shopee para o padrão Conheça Mais."""

    item_id = product.get("itemId")
    shop_id = product.get("shopId")

    if not item_id or not shop_id:
        raise ValueError("Produto sem identificadores da Shopee.")

    price = optional_decimal(product.get("priceMin"))

    if price is None or price <= 0:
        raise ValueError("Produto sem preço válido.")

    # A Shopee retorna comissão como fração:
    # 0.19 corresponde a 19%.
    rate = optional_decimal(product.get("commissionRate"))

    commission_rate = (
        float(rate * 100)
        if rate is not None
        else None
    )

    rating = optional_decimal(product.get("ratingStar"))

    # priceDiscountRate representa um percentual.
    discount_rate = product.get("priceDiscountRate")

    # Não inventamos o preço original com base
    # na faixa priceMin / priceMax.
    return {
        "offer_id": f"shopee-{shop_id}-{item_id}",
        "title": product.get("productName", ""),
        "current_price": float(price),
        "original_price": None,
        "marketplace": "Shopee",
        "affiliate_url": product.get("offerLink", ""),
        "product_url": product.get("productLink", ""),
        "image_url": product.get("imageUrl", ""),
        "commission": None,
        "commission_rate": commission_rate,
        "sales": product.get("sales"),
        "rating": float(rating) if rating is not None else None,
        "discount_rate": discount_rate
    }
