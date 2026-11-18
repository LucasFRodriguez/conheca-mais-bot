
import tempfile
from pathlib import Path

import services.deduplicator as deduplicator


def main():
    original_path = deduplicator.FILE_PATH

    try:
        with tempfile.TemporaryDirectory() as directory:
            deduplicator.FILE_PATH = (
                Path(directory) / "published_offers.json"
            )

            test_id = "teste-gravacao-001"

            print("Histórico inicial:")
            print(deduplicator.get_published_offers())

            deduplicator.save_published_offer(test_id)

            print("\nHistórico após gravação:")
            print(deduplicator.get_published_offers())

            assert deduplicator.is_already_published(test_id)

            # Salvar novamente não deve duplicar.
            deduplicator.save_published_offer(test_id)

            assert deduplicator.get_published_offers() == [
                test_id
            ]

            print("\nTeste de gravação aprovado!")

    finally:
        deduplicator.FILE_PATH = original_path


if __name__ == "__main__":
    main()
