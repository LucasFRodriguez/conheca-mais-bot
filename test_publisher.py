
import asyncio

from telegram.error import NetworkError
from services.publisher import publish_message


class FakeBot:
    def __init__(self):
        self.attempts = 0

    async def send_message(self, chat_id, text):
        self.attempts += 1

        print(f"Executando tentativa {self.attempts}...")

        if self.attempts < 3:
            raise NetworkError("Falha de conexão simulada")

        print("Mensagem enviada com sucesso (simulação)!")


async def main():
    bot = FakeBot()

    await publish_message(
        bot,
        "Oferta de teste do Conheça Mais"
    )

    print(f"\nTotal de tentativas: {bot.attempts}")


if __name__ == "__main__":
    asyncio.run(main())
