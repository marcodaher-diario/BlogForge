import os
import requests
import random
import json

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def carregar_imagens_usadas():
    with open("data/imagens_usadas.json", "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_imagens_usadas(lista):
    with open("data/imagens_usadas.json", "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2)

def eh_16_9(width, height, tolerancia=0.05):
    proporcao = width / height
    return abs(proporcao - (16/9)) <= tolerancia

def buscar_imagens_16_9(tema, quantidade=2):
    if not PEXELS_API_KEY:
        raise ValueError("PEXELS_API_KEY não encontrada.")

    url = f"https://api.pexels.com/v1/search?query={tema}&per_page=30"
    headers = {"Authorization": PEXELS_API_KEY}

    response = requests.get(url, headers=headers)
    data = response.json()

    imagens_usadas = carregar_imagens_usadas()
    imagens_validas = []

    for foto in data.get("photos", []):
        if eh_16_9(foto["width"], foto["height"]):
            url_img = foto["src"]["large2x"]

            if url_img not in imagens_usadas:
                imagens_validas.append(url_img)

    if not imagens_validas:
        return []

    selecionadas = random.sample(
        imagens_validas,
        min(len(imagens_validas), quantidade)
    )

    imagens_usadas.extend(selecionadas)
    salvar_imagens_usadas(imagens_usadas)

    return selecionadas

