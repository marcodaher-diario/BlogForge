import os
import json
from groq import Groq
from datetime import datetime

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def caminho_ideias(blog_nome):
    return f"blogs/{blog_nome}/ideias.json"


def carregar_ideias(blog_nome):
    caminho = caminho_ideias(blog_nome)

    if not os.path.exists(caminho):
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_ideias(blog_nome, ideias):
    caminho = caminho_ideias(blog_nome)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(ideias, f, indent=2, ensure_ascii=False)


def gerar_novas_ideias(nicho, quantidade=20):
    prompt = f"""
    Gere {quantidade} ideias de títulos altamente atrativos e profissionais
    para um blog sobre {nicho}.

    Apenas liste os títulos, um por linha.
    Não numere.
    """

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
    )

    texto = response.choices[0].message.content

    ideias = [
        linha.strip()
        for linha in texto.split("\n")
        if linha.strip()
    ]

    return ideias


def garantir_estoque_ideias(blog_nome, nicho, minimo=10):
    ideias = carregar_ideias(blog_nome)

    if len(ideias) < minimo:
        novas = gerar_novas_ideias(nicho, 30)
        ideias.extend(novas)
        ideias = list(dict.fromkeys(ideias))  # remove duplicadas
        salvar_ideias(blog_nome, ideias)

    return ideias


def pegar_ideia_disponivel(blog_nome, nicho):
    ideias = garantir_estoque_ideias(blog_nome, nicho)

    if not ideias:
        return None

    ideia = ideias[0]
    ideias.pop(0)
    salvar_ideias(blog_nome, ideias)

    return ideia

