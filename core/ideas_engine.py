import json
import os
import random
from datetime import datetime
from core.content_engine import gerar_conteudo

def caminho_ideias(blog_nome):
    return f"blogs/{blog_nome}/ideias.json"

def carregar_ideias(blog_nome):
    caminho = caminho_ideias(blog_nome)

    if not os.path.exists(caminho):
        return {"ideias_disponiveis": [], "ideias_usadas": []}

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_ideias(blog_nome, dados):
    with open(caminho_ideias(blog_nome), "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def gerar_novas_ideias(blog_nome, config, quantidade=20):
    prompt = f"""
    Gere {quantidade} ideias de títulos altamente estratégicos para blog.
    Nicho: {config.get("nicho")}
    Tom: {config.get("tom")}
    Foco SEO: {config.get("seo_foco")}
    
    Retorne apenas lista simples, uma ideia por linha.
    """

    resposta = gerar_conteudo(prompt, config)

    ideias = []
    for linha in resposta.split("\n"):
        linha = linha.strip("- ").strip()
        if len(linha) > 10:
            ideias.append(linha)

    return ideias

def obter_tema(blog_nome, config):
    dados = carregar_ideias(blog_nome)

    # Se estoque baixo → gera novas ideias
    if len(dados["ideias_disponiveis"]) < 5:
        novas = gerar_novas_ideias(blog_nome, config, quantidade=30)
        dados["ideias_disponiveis"].extend(novas)

    if not dados["ideias_disponiveis"]:
        raise ValueError("Não foi possível gerar ideias.")

    tema = random.choice(dados["ideias_disponiveis"])

    dados["ideias_disponiveis"].remove(tema)
    dados["ideias_usadas"].append({
        "titulo": tema,
        "data": datetime.now().isoformat()
    })

    salvar_ideias(blog_nome, dados)

    return tema
