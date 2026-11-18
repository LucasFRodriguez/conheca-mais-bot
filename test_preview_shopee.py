
from services.offer_processor import process_offers


def main():
    print("Preparando prévia da oferta real...\n")

    offers = process_offers()

    if not offers:
        print("Nenhuma oferta aprovada pelo filtro.")
        return

    # Mostra somente a primeira oferta aprovada.
    offer = offers[0]

    print("=" * 45)
    print("PRÉVIA DA MENSAGEM DO TELEGRAM")
    print("=" * 45)

    print(offer["message"])

    print("=" * 45)
    print("Pontuação:", offer["score"])
    print("ID da oferta:", offer["offer_id"])

    print("\nPrévia concluída. Nada foi publicado.")


if __name__ == "__main__":
    main()
