
from services.offer_filter import classify_offer, filter_offers


offers = [
    {"title": "Produto A", "score": 20},
    {"title": "Produto B", "score": 80},
    {"title": "Produto C", "score": 40},
    {"title": "Produto D", "score": 10},
    {"title": "Produto E", "score": 60}
]


print("CLASSIFICAÇÃO DAS OFERTAS")
print("-" * 35)

for offer in offers:
    classification = classify_offer(offer["score"])

    print(
        f"{offer['title']}: "
        f"{offer['score']} pontos - {classification}"
    )


approved = filter_offers(offers)

print("\nOFERTAS APROVADAS")
print("-" * 35)

for offer in approved:
    print(f"{offer['title']}: {offer['score']} pontos")


# Testes automáticos
assert classify_offer(80) == "Excelente"
assert classify_offer(40) == "Boa"
assert classify_offer(20) == "Regular"
assert classify_offer(10) == "Baixa"

assert len(approved) == 3
assert approved[0]["score"] == 80
assert approved[1]["score"] == 60
assert approved[2]["score"] == 40

print("\nTodos os testes foram aprovados!")
