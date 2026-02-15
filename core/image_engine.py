import os
import requests
import random
import json
import re

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
DATA_FILE = "data/imagens_usadas.json"


# ==========================================
# UTILITÁRIOS
# ==========================================

def carregar_imagens_usadas():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_imagens_usadas(lista):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2)


def eh_horizontal(width, height):
    return width > height


def limpar_titulo(titulo):
    titulo = re.sub(r"^\d+\.\s*", "", titulo)
    titulo = re.sub(r"Aqui estão.*", "", titulo)
    return titulo.strip()


# ==========================================
# QUERY INTELIGENTE POR NICHO
# ==========================================

def gerar_query_inteligente(tema, nicho):

    tema = limpar_titulo(tema).lower()

    if nicho == "saude":
        return random.choice([
            "healthy lifestyle",
            "weight loss healthy",
            "fitness motivation",
            "healthy food",
            "exercise routine"
        ])

    elif nicho == "automodelismo":
        return random.choice([
            "RC car racing",
            "remote control car",
            "RC buggy dirt track",
            "RC drift car",
            "RC car maintenance"
        ])

    elif nicho == "fotografia":
        return random.choice([
            "professional photography",
            "camera equipment",
            "low light photography",
            "portrait photography",
            "photo editing"
        ])

    elif nicho == "noticias":
        return random.choice([
            "Brazil congress",
            "Brazil economy",
            "international diplomacy",
            "political meeting",
            "financial market"
        ])

    else:
        return tema


# ==========================================
# BUSCA PRINCIPAL DE IMAGENS
# ==========================================

def buscar_imagens_16_9(tema, quantidade=2, nicho=None):

    if not PEXELS_API_KEY:
        print("PEXELS_API_KEY não encontrada.")
        return []

    query = gerar_query_inteligente(tema, nicho)

    url = f"https://api.pexels.com/v1/search?query={query}&per_page=40"
    headers = {"Authorization": PEXELS_API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Erro na API Pexels: {e}")
        return []

    imagens_usadas = carregar_imagens_usadas()
    imagens_validas = []

    for foto in data.get("photos", []):
        width = foto.get("width")
        height = foto.get("height")

        if not width or not height:
            continue

        if eh_horizontal(width, height):
            url_img = foto["src"]["large2x"]

            if url_img not in imagens_usadas:
                imagens_validas.append(url_img)

    if not imagens_validas:
        print("Nenhuma imagem horizontal encontrada.")
        return []

    selecionadas = random.sample(
        imagens_validas,
        min(len(imagens_validas), quantidade)
    )

    imagens_usadas.extend(selecionadas)
    salvar_imagens_usadas(imagens_usadas)

    return selecionadas
