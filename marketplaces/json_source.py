
import json
from pathlib import Path


FILE_PATH = Path("data/offers.json")


def get_offers():
    """Lê as ofertas cadastradas no arquivo JSON."""

    if not FILE_PATH.exists():
        return []

    with open(FILE_PATH, "r", encoding="utf-8") as file:
        offers = json.load(file)

    return offers
