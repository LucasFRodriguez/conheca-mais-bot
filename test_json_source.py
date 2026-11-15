
from services.offer_processor import process_offers


processed_offers = process_offers()

print("\n" + "=" * 40)
print("RESULTADO DO PROCESSAMENTO")
print("=" * 40)

for offer in processed_offers:
    print(f"\nProduto: {offer['title']}")
    print(f"ID: {offer['offer_id']}")
    print("\nMensagem:")
    print(offer["message"])
