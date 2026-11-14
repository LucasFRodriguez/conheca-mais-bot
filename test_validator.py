from services.offer_validator import validate_offer

offer = {
    "offer_id": "teste-001",
    "title": "Produto de teste",
    "current_price": -10,
    "original_price": 50,
    "marketplace": "Shopee",
    "affiliate_url": "https://example.com"
}

try:
    validate_offer(offer)
    print("Oferta válida!")

except ValueError as error:
    print(f"Oferta rejeitada: {error}")