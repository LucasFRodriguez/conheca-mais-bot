
import asyncio

from test_automation import main as run_automation


# Intervalo de 6 horas (em segundos)
INTERVAL = 6 * 60 * 60


async def scheduler():
    print("Conheça Mais: agendador iniciado!")

    while True:
        print("\nIniciando nova verificação de ofertas...")

        try:
            await run_automation()
            print("Verificação concluída!")

        except Exception as error:
            print(f"Erro durante a execução: {error}")

        print("Próxima execução em 6 horas.")

        await asyncio.sleep(INTERVAL)


if __name__ == "__main__":
    try:
        asyncio.run(scheduler())

    except KeyboardInterrupt:
        print("\nAgendador encerrado.")
