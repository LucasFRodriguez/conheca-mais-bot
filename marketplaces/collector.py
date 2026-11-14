
from marketplaces.mock import get_offers as get_mock_offers


def get_all_offers():
    """
    Reúne ofertas de todos os marketplaces ativos.

    Por enquanto, utiliza apenas dados fictícios.
    """

    all_offers = []

    # Ofertas fictícias para testes
    mock_offers = get_mock_offers()
    all_offers.extend(mock_offers)

    return all_offers
