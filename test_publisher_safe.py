
import asyncio
from unittest.mock import AsyncMock

from telegram.error import NetworkError

from services.publisher import publish_message


async def main():
    # Simula um bot do Telegram.
    fake_bot = AsyncMock()

    # Simula falha de conexão.
    fake_bot.send_message.side_effect = NetworkError(
        "Falha simulada de conexão"
    )

    print("Simulando falha de conexão...")

    try:
        await publish_message(
            fake_bot,
            "Mensagem de teste"
        )

    except NetworkError:
        print("Falha de conexão detectada corretamente.")

    # Confirma que não tentou enviar novamente.
    assert fake_bot.send_message.await_count == 1, (
        "Erro: houve mais de uma tentativa de envio."
    )

    print("Tentativas de envio:", fake_bot.send_message.await_count)
    print("Teste aprovado: nenhum reenvio automático!")


if __name__ == "__main__":
    asyncio.run(main())
