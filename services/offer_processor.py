
import re
import unicodedata

from marketplaces.collector import get_all_offers

from services.offer_validator import validate_offer
from services.offer_formatter import format_offer
from services.deduplicator import is_already_published
from services.offer_scorer import score_offer
from services.offer_filter import filter_offers


# Quantidade maxima de ofertas por ciclo
MAX_OFFERS_PER_CYCLE = 2


# Palavras usadas para identificar nichos.
CATEGORY_KEYWORDS = {
    "Suplementos": [
        "creatina",
        "whey",
        "suplemento",
        "proteina",
        "pre treino",
        "coqueteleira",
    ],
    "Eletronicos": [
        "fone",
        "headset",
        "bluetooth",
        "mouse",
        "teclado",
        "smartwatch",
        "power bank",
        "carregador",
        "memoria ram",
        "iphone",
        "capinha",
        "cabo usb",
        "caixa de som",
    ],
    "Cozinha": [
        "marmita",
        "marmitas",
        "potestravas",
        "pote",
        "panela",
        "frigideira",
        "omeleteira",
        "processador",
        "triturador",
        "tempero",
        "caneca",
        "copo termico",
        "garrafa termica",
        "utensilio",
        "cozinha",
    ],
    "Beleza": [
        "shampoo",
        "hidratante",
        "perfume",
        "body splash",
        "maquina de cortar cabelo",
        "aparador de barba",
        "maquiagem",
        "skincare",
    ],
    "Moda": [
        "regata",
        "cropped",
        "short",
        "bermuda",
        "calca",
        "jaqueta",
        "chinelo",
        "sandalia",
        "bota",
        "vestido",
        "oculos de sol",
        "relogio",
        "macaquinho fitness",
    ],
    "Ferramentas": [
        "parafusadeira",
        "furadeira",
        "chave catraca",
        "soquete",
        "jogo de ferramentas",
        "kit de ferramentas",
        "compressor",
        "calibrador",
    ],
    "Automotivo": [
        "vonixx",
        "lavagem automotiva",
        "estetica automotiva",
        "pneu pretinho",
        "limpeza automotiva",
    ],
    "Casa e decoracao": [
        "cortina",
        "espelho",
        "arvore de natal",
        "led decoracao",
        "organizadora",
        "organizadores",
    ],
    "Pets": [
        "comedouro",
        "bebedouro",
        "gatos",
        "caes",
        "racao",
        "pet",
    ],
    "Brinquedos": [
        "brinquedo",
        "squishy",
        "boneca",
        "carrinho infantil",
    ],
}


def normalize_text(text):
    """Remove acentos e padroniza o texto."""

    text = unicodedata.normalize(
        "NFKD",
        str(text).lower()
    )

    text = "".join(
        char for char in text
        if not unicodedata.combining(char)
    )

    return re.sub(
        r"\s+",
        " ",
        re.sub(r"[^a-z0-9]+", " ", text)
    ).strip()


def identify_category(title):
    """
    Identifica uma categoria aproximada pelo titulo.

    Essa classificacao nao e uma categoria oficial
    da Shopee.
    """

    normalized_title = normalize_text(title)

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            normalized_keyword = normalize_text(keyword)

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(normalized_keyword)
                + r"(?![a-z0-9])"
            )

            if re.search(pattern, normalized_title):
                return category

    return "Outros"


def select_diverse_offers(approved_offers, limit):
    """
    Seleciona ofertas com boa pontuacao e variedade.

    Primeiro tenta escolher categorias diferentes.
    Depois completa as vagas, caso necessario.
    """

    selected = []
    selected_ids = set()
    used_categories = set()

    # Primeira passagem: categorias diferentes.
    for offer in approved_offers:

        if len(selected) >= limit:
            break

        category = offer.get("category", "Outros")

        if category in used_categories:
            continue

        selected.append(offer)
        selected_ids.add(offer["offer_id"])
        used_categories.add(category)

    # Segunda passagem: completa as vagas
    # se nao houver categorias suficientes.
    for offer in approved_offers:

        if len(selected) >= limit:
            break

        if offer["offer_id"] in selected_ids:
            continue

        selected.append(offer)
        selected_ids.add(offer["offer_id"])

    return selected


def process_offers():
    """Busca, valida, pontua e prepara ofertas."""

    offers = get_all_offers()
    processed_offers = []

    print(
        f"Total de ofertas encontradas: {len(offers)}"
    )

    for offer in offers:

        try:
            validate_offer(offer)

            offer_id = offer["offer_id"]

            if is_already_published(offer_id):
                print(
                    f"Oferta ja publicada: {offer['title']}"
                )
                continue

            score = score_offer(offer)
            message = format_offer(offer)

            category = identify_category(
                offer["title"]
            )

            processed_offers.append({
                "offer_id": offer_id,
                "title": offer["title"],
                "score": score,
                "message": message,
                "category": category,
                "marketplace": offer.get("marketplace"),
                "current_price": offer.get("current_price"),
                "original_price": offer.get("original_price"),
                "commission_rate": offer.get("commission_rate"),
                "discount_rate": offer.get("discount_rate"),
                "rating": offer.get("rating"),
                "sales": offer.get("sales"),
            })

            print(
                f"Oferta processada: {offer['title']} "
                f"| Nicho: {category} "
                f"| Pontuacao: {score}"
            )

        except (ValueError, TypeError) as error:
            print(
                f"Oferta invalida: "
                f"{offer.get('title', 'Sem titulo')} "
                f"| {error}"
            )

    # Filtra e ordena da maior para a menor pontuacao.
    approved_offers = filter_offers(
        processed_offers,
        minimum_score=40
    )

    print(
        "Ofertas aprovadas pelo filtro:",
        len(approved_offers)
    )

    # Prioriza categorias diferentes.
    selected_offers = select_diverse_offers(
        approved_offers,
        MAX_OFFERS_PER_CYCLE
    )

    print(
        "Ofertas selecionadas para o ciclo:",
        len(selected_offers)
    )

    for offer in selected_offers:
        print(
            f"SELECIONADA: {offer['title']} "
            f"| Nicho: {offer['category']} "
            f"| Pontuacao: {offer['score']}"
        )

    return selected_offers
