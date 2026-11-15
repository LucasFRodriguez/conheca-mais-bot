
from marketplaces.json_source import get_offers as get_json_offers


def get_all_offers():
    """
    Reúne ofertas cadastradas nas fontes disponíveis.
    """

    all_offers = []

    # Ofertas cadastradas manualmente no JSON
    json_offers = get_json_offers()
    all_offers.extend(json_offers)

    return all_offers
