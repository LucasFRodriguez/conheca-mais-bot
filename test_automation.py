
import asyncio
import os

from dotenv import load_dotenv
from telegram import Bot
from telegram.request import HTTPXRequest

from services.offer_processor import process_offers
from services.offer_runner import run_offer_cycle

from logger_config import logger


load_dotenv()


async def main():

    logger.info("Iniciando automação do Conheça Mais.")

    # Consulta a configuração em cada execução.
    publishing_enabled = (
        os.getenv(
            "ENABLE_TELEGRAM_PUBLISHING",
            "false"
        ).strip().lower() == "true"
    )

    # Modo seguro: processa, mas não publica.
    if not publishing_enabled:

        offers = process_offers()

        logger.info(
            "Modo seguro ativado. %d oferta(s) processada(s).",
            len(offers)
        )

        logger.info("Nenhuma publicação foi realizada.")

        return

    # Só busca o token quando a publicação está habilitada.
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise ValueError(
            "Token do Telegram não encontrado no .env."
        )

    # Configuração que funcionou no teste manual.
    request = HTTPXRequest(
        connect_timeout=30.0,
        read_timeout=30.0,
        write_timeout=30.0
    )

    bot = Bot(
        token=token,
        request=request
    )

    # Inicializa o bot e encerra a conexão corretamente.
    async with bot:
        await run_offer_cycle(bot)

    logger.info("Automação finalizada.")


if __name__ == "__main__":
    asyncio.run(main())
