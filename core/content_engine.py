import os
from groq import Groq


def gerar_conteudo(tema, config_blog):
    """
    Gera conteúdo usando Groq API
    """

    # ==============================
    # PROTEÇÕES CONTRA ERROS
    # ==============================
    tom = config_blog.get("tom", "educativo")
    tamanho = config_blog.get("tamanho_artigo", 900)
    seo_foco = config_blog.get("seo_foco", tema)

    # ==============================
    # CLIENTE GROQ
    # ==============================
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise Exception("GROQ_API_KEY não encontrada nas variáveis de ambiente.")

    client = Groq(api_key=api_key)

    # ==============================
    # PROMPT PROFISSIONAL
    # ==============================
    prompt = f"""
    Escreva um artigo completo para blog sobre: "{tema}"

    Requisitos:
    - Tom: {tom}
    - Aproximadamente {tamanho} palavras
    - Foco em SEO: {seo_foco}
    - Estrutura com:
        - Introdução
        - Subtítulos claros
        - Listas quando necessário
        - Conclusão estratégica
    - Linguagem natural
    - Não usar emojis
    - Não usar hashtags
    - Não escrever HTML
    - Texto limpo
    """

    # ==============================
    # CHAMADA DA IA
    # ==============================
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Você é um redator profissional especialista em SEO e blogs."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )

    texto = response.choices[0].message.content.strip()

    return texto
