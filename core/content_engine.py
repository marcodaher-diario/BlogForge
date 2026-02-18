import os
from groq import Groq


def gerar_conteudo(tema, config_blog):
    """
    Gera conteúdo estruturado profissional
    com marcação interna controlada.
    """

    # ==========================================
    # CONFIGURAÇÕES
    # ==========================================

    tom = config_blog.get("tom", "educativo")
    tamanho_minimo = 600
    tamanho_maximo = config_blog.get("tamanho_artigo", 900)
    seo_foco = config_blog.get("seo_foco", tema)

    # ==========================================
    # API KEY
    # ==========================================

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise Exception("GROQ_API_KEY não encontrada nas variáveis de ambiente.")

    client = Groq(api_key=api_key)

    # ==========================================
    # PROMPT PROFISSIONAL CONTROLADO
    # ==========================================

    prompt = f"""
Escreva um artigo completo para blog sobre o tema: "{tema}"

REGRAS OBRIGATÓRIAS:

1) O artigo deve ter NO MÍNIMO {tamanho_minimo} palavras.
2) Pode chegar até aproximadamente {tamanho_maximo} palavras.
3) Nunca escreva menos que {tamanho_minimo} palavras.
4) Linguagem natural, fluida e profissional.
5) Tom: {tom}
6) Foco SEO principal: {seo_foco}
7) NÃO use:
   - hashtags
   - emojis
   - markdown (#, ##, ###)
   - asteriscos (*)
   - HTML
8) Não use listas com marcadores como * ou -.
9) Pode usar listas numeradas apenas se necessário.

ESTRUTURA OBRIGATÓRIA:

INTRODUÇÃO:
(2 a 3 parágrafos)

SUBTITULO:
(parágrafos de desenvolvimento)

SUBTITULO:
(parágrafos de desenvolvimento)

(opcionalmente mais um)
SUBTITULO:
(parágrafos)

CONSIDERAÇÕES FINAIS:
(parágrafo final estratégico e conclusivo)

Escreva exatamente seguindo essa estrutura textual.
Não explique a estrutura.
Não use títulos decorativos.
Apenas produza o artigo.
"""

    # ==========================================
    # CHAMADA GROQ
    # ==========================================

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Você é um redator profissional especialista em SEO e blogs."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=3000
    )

    texto = response.choices[0].message.content.strip()

    # ==========================================
    # GARANTIA DE TAMANHO MÍNIMO
    # ==========================================

    if len(texto.split()) < tamanho_minimo:
        print("Conteúdo abaixo do mínimo. Gerando complemento...")

        complemento_prompt = f"""
O texto anterior ficou abaixo de {tamanho_minimo} palavras.
Continue desenvolvendo o artigo mantendo a mesma estrutura
e aprofundando os subtítulos já criados.
Não reinicie o texto.
"""

        complemento = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Você é um redator profissional especialista em SEO."},
                {"role": "user", "content": complemento_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        texto += "\n\n" + complemento.choices[0].message.content.strip()

    return texto
