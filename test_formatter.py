
from services.offer_formatter import format_offer


offer = {
    "title": "Fone Bluetooth Sem Fio",
    "current_price": 49.90,
    "original_price": 99.90,
    "marketplace": "Shopee",
    "affiliate_url": "https://example.com"
}

message = format_offer(offer)

print(message)
