
import tempfile
from pathlib import Path
from unittest.mock import patch

from services.deduplicator import (
    get_published_offers,
    save_published_offer,
    is_already_published
)


def main():

    # Cria um arquivo temporário para não alterar
    # o histórico real do projeto.
    with tempfile.TemporaryDirectory() as temp_dir:

        test_file = Path(temp_dir) / "published_offers.json"

        with patch(
            "services.deduplicator.FILE_PATH",
            test_file
        ):

            offer_id = "manual-002"

            # Inicialmente, a oferta não foi publicada.
            assert not is_already_published(offer_id)

            print("1. Oferta ainda não publicada: OK")

            # Registra a publicação.
            save_published_offer(offer_id)

            assert is_already_published(offer_id)

            print("2. Registro da publicação: OK")

            # Tenta registrar novamente.
            save_published_offer(offer_id)

            published = get_published_offers()

            assert published.count(offer_id) == 1

            print("3. Prevenção de duplicidade: OK")

            # Verifica persistência do registro.
            assert test_file.exists()

            print("4. Arquivo de histórico criado: OK")

    print("\nTodos os testes foram aprovados!")


if __name__ == "__main__":
    main()
