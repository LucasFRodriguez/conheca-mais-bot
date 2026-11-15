
from marketplaces.collector import get_all_offers
from services.offer_validator import validate_offer


offers = get_all_offers()

print("Total de ofertas:", len(offers))

for offer in offers:
    try:
        validate_offer(offer)

        print(f"✅ Oferta válida: {offer['title']}")

    except ValueError as error:
        print(f"❌ Oferta inválida: {error}")
