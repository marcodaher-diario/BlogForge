import json
from datetime import datetime

def carregar_historico(blog_key):
    caminho = f"historico/{blog_key}.json"

    if not os.path.exists(caminho):
        return {
            "temas_usados": [],
            "datas_publicadas": [],
            "categorias_recentemente_usadas": []
        }

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_historico(blog_key, dados):
    caminho = f"historico/{blog_key}.json"

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)

