import json
import os
import random
from datetime import datetime, timedelta

JANELA_DIAS_REPETICAO = 60


def carregar_temas(caminho_blog):
    caminho = os.path.join(caminho_blog, "temas.json")
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def carregar_historico(caminho_blog):
    caminho = os.path.join(caminho_blog, "historico_temas.json")
    
    if not os.path.exists(caminho):
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_historico(caminho_blog, historico):
    caminho = os.path.join(caminho_blog, "historico_temas.json")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=4, ensure_ascii=False)


def filtrar_temas_validos(temas, historico):
    agora = datetime.now()
    bloqueio = agora - timedelta(days=JANELA_DIAS_REPETICAO)

    usados_recentemente = {
        item["tema"]
        for item in historico
        if datetime.fromisoformat(item["data"]) > bloqueio
    }

    temas_validos = [t for t in temas if t not in usados_recentemente]

    if not temas_validos:
        # Se todos bloqueados, libera o mais antigo
        print("⚠ Todos os temas bloqueados. Liberando o mais antigo.")
        return temas

    return temas_validos


def escolher_tema(caminho_blog):
    temas = carregar_temas(caminho_blog)
    historico = carregar_historico(caminho_blog)

    temas_validos = filtrar_temas_validos(temas, historico)

    tema_escolhido = random.choice(temas_validos)

    historico.append({
        "tema": tema_escolhido,
        "data": datetime.now().isoformat()
    })

    salvar_historico(caminho_blog, historico)

    return tema_escolhido

