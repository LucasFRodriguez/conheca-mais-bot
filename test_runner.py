
import asyncio
from unittest.mock import AsyncMock, patch

from services.offer_runner import run_offer_cycle


async def main():

    bot = object()

    with patch(
        "services.offer_runner.process_offers",
        return_value=[]
    ) as mock_processor:

        with patch(
            "services.offer_runner.dispatch_offers",
            new_callable=AsyncMock
        ) as mock_dispatcher:

            await run_offer_cycle(bot)

            mock_processor.assert_called_once()
            mock_dispatcher.assert_not_awaited()

    print("\n✅ Processamento executado!")
    print("✅ Nenhuma oferta nova encontrada!")
    print("✅ Distribuidor não foi chamado!")
    print("✅ Nenhuma publicação realizada!")


if __name__ == "__main__":
    asyncio.run(main())
