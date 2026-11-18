
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

    # Busca e processa ofertas reais da Shopee.
    offers = process_offers()

    if not offers:
        print("Nenhuma oferta nova aprovada.")
        return

    # Seleciona somente a primeira oferta.
    selected = offers[:1]

    print("Oferta selecionada:", selected[0]["title"])
    print("Pontuação:", selected[0]["score"])

    # Confirmação manual antes do envio.
    confirmation = input(
        "\nDigite PUBLICAR para enviar ao Telegram: "
    )

    if confirmation != "PUBLICAR":
        print("Publicação cancelada.")
        return

    bot = Bot(token=token)

    async with bot:
        await dispatch_offers(bot, selected)

    print("\nTeste de publicação encerrado.")
    print("Confira o canal @conhecamaisofertas.")


if __name__ == "__main__":
    asyncio.run(main())
