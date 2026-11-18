
import asyncio
import os

from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError
from telegram.request import HTTPXRequest

from services.offer_processor import process_offers
from services.offer_dispatcher import dispatch_offers


async def main():
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        print("Token do Telegram não encontrado no .env.")
        return

    # Busca as ofertas reais da Shopee
    offers = process_offers()

    if not offers:
        print("\nNenhuma oferta nova para publicar.")
        return

    # Limite máximo de 3 ofertas
    selected = offers[:3]

    print("\n" + "=" * 50)
    print("OFERTAS SELECIONADAS PARA PUBLICAÇÃO")
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

    # Exige autorização antes de publicar
    confirmation = input(
        "\nDigite PUBLICAR para enviar as ofertas: "
    )

    if confirmation != "PUBLICAR":
        print("\nPublicação cancelada.")
        return

    # Configuração de conexão com tempo ampliado
    request = HTTPXRequest(
        connect_timeout=30.0,
        read_timeout=30.0,
        write_timeout=30.0
    )

    bot = Bot(
        token=token,
        request=request
    )

    try:
        async with bot:
            # Publica pelo sistema existente
            await dispatch_offers(bot, selected)

    except TelegramError as error:
        print("\nFalha de comunicação com o Telegram.")
        print("Tipo do erro:", type(error).__name__)
        print(
            "Confira o canal antes de tentar novamente."
        )
        return

    print("\nExecução do publicador encerrada.")
    print(
        "Confira as mensagens no @conhecamaisofertas."
    )


if __name__ == "__main__":
    asyncio.run(main())
