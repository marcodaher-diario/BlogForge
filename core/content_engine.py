import os
from groq import Groq

def gerar_conteudo(tema, config_blog):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY não encontrada.")

    client = Groq(api_key=api_key)

    prompt = f"""
    Escreva um artigo profissional sobre: {tema}.
    Use tom {config_blog['tom']}.
    Tamanho aproximado: {config_blog['tamanho_artigo']} palavras.
    Foque em SEO para: {config_blog['seo_foco']}.
    Estruture com introdução, subtítulos e conclusão.
    Linguagem natural e original.
    """

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "Você é um redator profissional especialista em criação de artigos para blog."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )

    return response.choices[0].message.content
