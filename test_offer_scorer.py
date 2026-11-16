
from services.offer_scorer import score_offer


# Oferta com todos os critérios positivos
offer_1 = {
    "commission_rate": 15,
    "rating": 4.5,
    "original_price": 100,
    "current_price": 70,
    "sales": 150
}

# Oferta sem informações opcionais
offer_2 = {
    "commission_rate": None,
    "rating": None,
    "original_price": None,
    "current_price": 50,
    "sales": None
}

# Oferta com pontuação intermediária
offer_3 = {
    "commission_rate": 10,
    "rating": 4.0,
    "original_price": 100,
    "current_price": 85,
    "sales": 100
}


print("RESULTADOS DO CLASSIFICADOR")
print("-" * 35)

print(f"Oferta 1: {score_offer(offer_1)} pontos")
print(f"Oferta 2: {score_offer(offer_2)} pontos")
print(f"Oferta 3: {score_offer(offer_3)} pontos")


# Verificação automática dos resultados
assert score_offer(offer_1) == 80
assert score_offer(offer_2) == 0
assert score_offer(offer_3) == 40

print("\nTodos os testes foram aprovados!")
