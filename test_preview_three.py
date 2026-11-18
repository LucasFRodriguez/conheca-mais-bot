
from services.offer_processor import process_offers


def main():
    print("\nBuscando ofertas reais da Shopee...\n")

    offers = process_offers()

    if not offers:
        print("Nenhuma oferta nova aprovada.")
        return

    print("\n" + "=" * 50)
    print("PRÉVIA DAS OFERTAS SELECIONADAS")
    print("=" * 50)

    for number, offer in enumerate(offers, start=1):
        print(f"\n{'=' * 50}")
        print(f"OFERTA {number}")
        print(f"{'=' * 50}")

        # Oculta o link apenas na saída do terminal.
        # A mensagem original permanece inalterada.
        message = offer["message"]

        lines = message.splitlines()
        safe_lines = []

        for line in lines:
            if "http://" in line or "https://" in line:
                safe_lines.append("[LINK DE AFILIADO]")
            else:
                safe_lines.append(line)

        print("\n".join(safe_lines))

        print("\nPontuação:", offer["score"])
        print("ID:", offer["offer_id"])

    print("\nPrévia concluída.")
    print("Nenhuma oferta foi publicada.")


if __name__ == "__main__":
    main()
