
import json
from pathlib import Path


# Localiza a raiz do projeto
PROJECT_ROOT = Path(__file__).resolve().parents[1]

FILE_PATH = PROJECT_ROOT / "data" / "published_offers.json"


def get_published_offers():
    """Retorna a lista de ofertas já publicadas."""

    if not FILE_PATH.exists():
        return []

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            published = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            "O histórico de ofertas publicadas está inválido."
        ) from error

    if not isinstance(published, list):
        raise ValueError(
            "O histórico precisa conter uma lista de IDs."
        )

    return published


def save_published_offer(offer_id):
    """Registra uma oferta após sua publicação."""

    if not offer_id:
        raise ValueError("ID da oferta não informado.")

    published = get_published_offers()

    if offer_id in published:
        return

    published.append(offer_id)

    FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

    temp_path = FILE_PATH.with_suffix(".tmp")

    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(
            published,
            file,
            indent=4,
            ensure_ascii=False
        )

    temp_path.replace(FILE_PATH)


def is_already_published(offer_id):
    """Verifica se uma oferta já foi publicada."""

    published = get_published_offers()

    return offer_id in published
