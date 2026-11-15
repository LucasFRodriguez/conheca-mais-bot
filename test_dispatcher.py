
import asyncio
from unittest.mock import AsyncMock, patch

from services.offer_dispatcher import dispatch_offers


async def main():

    bot = object()

    offers = [
        {
            "offer_id": "manual-001",
            "title": "Fone Bluetooth Sem Fio",
            "message": "Mensagem de teste"
        }
    ]

    with patch(
        "services.offer_dispatcher.publish_message",
        new_callable=AsyncMock
    ) as mock_publish:

        with patch(
            "services.offer_dispatcher.save_published_offer"
        ) as mock_save:

            with patch(
                "services.offer_dispatcher.logger.exception"
            ) as mock_logger:

                mock_publish.side_effect = RuntimeError(
                    "Erro simulado no Telegram"
                )

                await dispatch_offers(bot, offers)

                mock_publish.assert_awaited_once()
                mock_save.assert_not_called()
                mock_logger.assert_called_once()

    print("✅ Falha de publicação simulada!")
    print("✅ Oferta NÃO foi registrada como publicada!")
    print("✅ Sistema de tratamento de erros funcionando!")


if __name__ == "__main__":
    asyncio.run(main())
