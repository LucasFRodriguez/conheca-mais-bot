
import time

from marketplaces.shopee import get_offers


KEYWORDS = [
    "ferramentas",
]


def main():
    print("\nTestando categorias da Shopee...\n")

    for keyword in KEYWORDS:
        print("=" * 45)
        print("Pesquisa:", keyword)

        try:
            offers = get_offers(
                keyword=keyword,
                limit=3
            )

            print("Produtos encontrados:", len(offers))

            for offer in offers:
                print("-", offer["title"])

        
        except Exception as error:
            print("Falha na pesquisa:")
            print("Tipo:", type(error).__name__)
            print("Detalhes:", str(error))


        # Evita consultas consecutivas muito rápidas.
        time.sleep(2)

    print("\nTeste concluido. Nada foi publicado.")


if __name__ == "__main__":
    main()
