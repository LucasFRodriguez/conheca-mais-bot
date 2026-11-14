
from telegram import Bot

CHANNEL_ID = "@conhecamaisofertas"


async def publish_message(bot: Bot, message: str):
    """Publica uma mensagem no canal do Conheça Mais."""
    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=message
    )
