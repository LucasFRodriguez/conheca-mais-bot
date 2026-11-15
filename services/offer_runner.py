
from services.offer_processor import process_offers
from services.offer_dispatcher import dispatch_offers


async def run_offer_cycle(bot):
    """
    Executa um ciclo completo de processamento
    e publicação de ofertas.
    """

    processed_offers = process_offers()

    if not processed_offers:
        print("Nenhuma oferta nova para publicar.")
        return

    await dispatch_offers(bot, processed_offers)
