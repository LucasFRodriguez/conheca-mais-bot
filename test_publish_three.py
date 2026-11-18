
import asyncio
import os

from dotenv import load_dotenv
from telegram import Bot

from services.offer_processor import process_offers
from services.offer_dispatcher import dispatch_offers


async def main():
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise ValueError("Token do Telegram não encontrado.")

    # Busca ofertas novas e aprovadas pela pontuação
    offers = process_offers()

    if not offers:
        print("\nNenhuma oferta nova para publicar.")
        return

    # Proteção adicional: no máximo 3
    selected = offers[:3]

    print("\n" + "=" * 50)
    print("OFERTAS QUE SERÃO PUBLICADAS")
    print("=" * 50)

    for number, offer in enumerate(selected, start=1):
        print(f"\nOFERTA {number}")
        print("Produto:", offer["title"])
        print("Pontuação:", offer["score"])
        print("ID:", offer["offer_id"])

        print("\nMensagem:")
        print(offer["message"])
        print("-" * 50)

    print(
        f"\nTotal selecionado: {len(selected)} oferta(s)"
    )

    confirmation = input(
        "\nDigite PUBLICAR para enviar as ofertas: "
    )

    if confirmation != "PUBLICAR":
        print("Publicação cancelada.")
        return

    # Envio pelo publicador existente
    bot = Bot(token=token)

    async with bot:
        await dispatch_offers(bot, selected)

    print("\nExecução encerrada.")
    print("Confira as mensagens no @conhecamaisofertas.")


if __name__ == "__main__":
    asyncio.run(main())
