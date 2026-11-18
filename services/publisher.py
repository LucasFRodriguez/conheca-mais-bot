
import asyncio

from telegram import Bot
from telegram.error import NetworkError, RetryAfter

from logger_config import logger


CHANNEL_ID = "@conhecamaisofertas"

MAX_ATTEMPTS = 3


async def publish_message(bot: Bot, message: str):
    """Publica uma mensagem no Telegram."""

    for attempt in range(1, MAX_ATTEMPTS + 1):

        try:
            sent_message = await bot.send_message(
                chat_id=CHANNEL_ID,
                text=message
            )

            # Retorna a mensagem confirmada pelo Telegram.
            return sent_message

        except RetryAfter as error:

            if attempt == MAX_ATTEMPTS:
                raise

            wait_time = float(error.retry_after) + 1

            logger.warning(
                "Telegram solicitou espera. "
                "Tentativa %d/%d. Aguardando %.1f segundos.",
                attempt,
                MAX_ATTEMPTS,
                wait_time
            )

            await asyncio.sleep(wait_time)

        except NetworkError:

            # Não repetimos automaticamente porque
            # o Telegram pode ter recebido a mensagem.
            logger.exception(
                "Falha de conexão no envio. "
                "Resultado da publicação incerto; "
                "reenvio automático cancelado."
            )

            raise
