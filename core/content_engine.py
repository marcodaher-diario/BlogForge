import os
from groq import Groq


def gerar_conteudo(tema, config_blog):
    """
    Gera conteúdo profissional com controle mínimo de tamanho
    """

    # ==========================================
    # CONFIGURAÇÕES
    # ==========================================
    tom = config_blog.get("tom", "educativo")
    seo_foco = config_blog.get("seo_foco", tema)

    # Tamanho mínimo e alvo
    palavras_minimas = 600
    palavras_alvo = 800

    # ==========================================
    # CLIENTE GROQ
    # ==========================================
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise Exception("GROQ_API_KEY não encontrada nas variáveis de ambiente.")

    client = Groq(api_key=api_key)

    # ==========================================
    # PROMPT PROFISSIONAL DEFINITIVO
    # ==========================================
    prompt = f"""
Escreva um artigo completo e aprofundado para blog sobre:

TEMA: "{tema}"

REGRAS OBRIGATÓRIAS:

- O artigo deve ter NO MÍNIMO {palavras_minimas} palavras.
- Idealmente entre 700 e 850 palavras.
- Nunca gerar texto curto ou superficial.
- Desenvolver ideias com explicações completas.
- Explorar exemplos práticos quando possível.
- Linguagem natural e profissional.
- Não usar emojis.
- Não usar hashtags.
- Não escrever HTML.
- Não numerar tópicos automaticamente.
- Não incluir meta-comentários.

ESTRUTURA OBRIGATÓRIA:

1) Introdução envolvente com 2 a 3 parágrafos.
2) Pelo menos 3 subtítulos claros.
3) Desenvolvimento detalhado em cada seção.
4) Se necessário, usar listas com marcador "*".
5) Conclusão estratégica consistente e bem desenvolvida.

FOCO EM SEO:
- Palavra-chave principal: {seo_foco}
- Inserir naturalmente ao longo do texto.

TOM:
{tom}

O artigo deve parecer escrito por um especialista experiente no assunto.
"""

    # ==========================================
    # CHAMADA DA IA
    # ==========================================
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Você é um redator profissional especialista em SEO, conteúdo estratégico e blogs de alta qualidade."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2500
    )

    texto = response.choices[0].message.content.strip()

    return texto
