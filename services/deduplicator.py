
import json
import os
import tempfile

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

FILE_PATH = PROJECT_ROOT / "data" / "published_offers.json"


def get_published_offers():
    """Retorna os IDs das ofertas já publicadas."""

    if not FILE_PATH.exists():
        return []

    try:
        with open(FILE_PATH, "r", encoding="utf-8-sig") as file:
            published = json.load(file)

    except (json.JSONDecodeError, UnicodeError) as error:
        raise ValueError(
            "O histórico de ofertas publicadas está inválido."
        ) from error

    if not isinstance(published, list):
        raise ValueError(
            "O histórico precisa conter uma lista de IDs."
        )

    if not all(
        isinstance(offer_id, str) and offer_id
        for offer_id in published
    ):
        raise ValueError(
            "O histórico contém identificadores inválidos."
        )

    return published


def save_published_offer(offer_id):
    """Registra uma oferta após sua publicação."""

    if not isinstance(offer_id, str) or not offer_id:
        raise ValueError("ID da oferta não informado.")

    published = get_published_offers()

    if offer_id in published:
        return

    updated = published + [offer_id]

    FILE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temp_path = None

    try:
        # Cria um arquivo temporário no mesmo diretório.
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".tmp",
            prefix="published_",
            dir=FILE_PATH.parent,
            delete=False
        ) as file:

            temp_path = Path(file.name)

            json.dump(
                updated,
                file,
                indent=4,
                ensure_ascii=False
            )

            file.flush()
            os.fsync(file.fileno())

        # Substituição atômica do histórico.
        os.replace(temp_path, FILE_PATH)

    finally:
        # Remove o temporário se houve falha.
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def is_already_published(offer_id):
    """Verifica se uma oferta já foi publicada."""

    return offer_id in get_published_offers()
