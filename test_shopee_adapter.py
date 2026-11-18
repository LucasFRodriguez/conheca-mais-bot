
from marketplaces.shopee_adapter import adapt_shopee_product


# Produto fictício no formato da Shopee
product = {
    "itemId": 123456,
    "shopId": 78910,
    "productName": "Fone Bluetooth de Teste",
    "priceMin": "49.90",
    "priceMax": "59.90",
    "commissionRate": "0.19",
    "ratingStar": "4.8",
    "sales": 150,
    "priceDiscountRate": 20,
    "imageUrl": "https://example.com/imagem.jpg",
    "productLink": "https://example.com/produto",
    "offerLink": "https://example.com/afiliado"
}

offer = adapt_shopee_product(product)

print("\nOFERTA ADAPTADA")
print("-" * 40)

for key, value in offer.items():
    print(f"{key}: {value}")

# Verificações automáticas
assert offer["offer_id"] == "shopee-78910-123456"
assert offer["current_price"] == 49.90
assert offer["original_price"] is None
assert offer["commission_rate"] == 19.0
assert offer["rating"] == 4.8
assert offer["marketplace"] == "Shopee"

print("\nTodos os testes do adaptador foram aprovados!")
