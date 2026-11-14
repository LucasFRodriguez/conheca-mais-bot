
import json
from pathlib import Path

FILE_PATH = Path("data/published_offers.json")


def get_published_offers():
    if not FILE_PATH.exists():
        return []

    with open(FILE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def save_published_offer(offer_id):
    published = get_published_offers()

    if offer_id not in published:
        published.append(offer_id)

    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(published, file, indent=4)


def is_already_published(offer_id):
    published = get_published_offers()
    return offer_id in published
