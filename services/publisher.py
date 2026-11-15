
import asyncio

from telegram import Bot
from telegram.error import NetworkError, RetryAfter

from logger_config import logger

CHANNEL_ID = "@conhecamaisofertas"

MAX_ATTEMPTS = 3


async def publish_message(bot: Bot, message: str):
    """Publica uma mensagem no canal com tentativas automáticas."""

    for attempt in range(1, MAX_ATTEMPTS + 1):

        try:
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=message
            )

            return

        except RetryAfter as error:

            if attempt == MAX_ATTEMPTS:
                raise

            wait_time = float(error.retry_after) + 1

            logger.warning(
                f"Telegram solicitou espera. "
                f"Tentativa {attempt}/{MAX_ATTEMPTS}. "
                f"Aguardando {wait_time} segundos."
            )

            await asyncio.sleep(wait_time)

        except NetworkError:

            if attempt == MAX_ATTEMPTS:
                logger.exception(
                    "Falha de conexão após todas as tentativas."
                )
                raise

            wait_time = 2 ** attempt

            logger.warning(
                f"Falha de conexão. "
                f"Tentativa {attempt}/{MAX_ATTEMPTS}. "
                f"Nova tentativa em {wait_time} segundos."
            )

            await asyncio.sleep(wait_time)
