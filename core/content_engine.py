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
    # PROMPT PROFISSIONAL DEFINITIVO
    # ==============================

    prompt = f"""
Escreva um artigo completo para blog sobre: "{tema}"

REGRAS OBRIGATÓRIAS:

- O artigo deve ter NO MÍNIMO 600 palavras.
- Ideal entre 700 e {tamanho} palavras.
- Nunca gerar menos de 600 palavras.
- Tom: {tom}
- Foco em SEO: {seo_foco}

ESTRUTURA OBRIGATÓRIA:

1. Introdução com 2 a 3 parágrafos.
2. Pelo menos 3 subtítulos.
3. Desenvolvimento consistente em cada subtítulo.
4. Conclusão estratégica com pelo menos 2 parágrafos.

FORMATAÇÃO:

- NÃO usar Markdown.
- NÃO usar #.
- NÃO usar ##.
- NÃO usar ###.
- NÃO usar *.
- NÃO usar - como marcador.
- NÃO usar emojis.
- NÃO usar hashtags.
- NÃO escrever HTML.
- Subtítulos devem ser escritos apenas como texto normal.
- Pode usar numeração simples (1, 2, 3) se desejar.

IMPORTANTE:
O texto deve ser limpo, profissional e pronto para ser formatado posteriormente.
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
        max_tokens=2500
    )

    texto = response.choices[0].message.content.strip()

    return texto
