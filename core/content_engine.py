import os
from groq import Groq


def gerar_conteudo(tema, config_blog):
    """
    Geração profissional definitiva de conteúdo.
    Blindagem especial para AUTOMODELISMO RC.
    """

    tom = config_blog.get("tom", "educativo")
    tamanho = config_blog.get("tamanho_artigo", 900)
    seo_foco = config_blog.get("seo_foco", tema)
    nicho = config_blog.get("nicho", "")

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise Exception("GROQ_API_KEY não encontrada.")

    client = Groq(api_key=api_key)

    # ==========================================
    # BLINDAGEM ESPECIAL AUTOMODELISMO RC
    # ==========================================

    blindagem_automodelismo = ""

    if nicho == "automodelismo":
        blindagem_automodelismo = """
        IMPORTANTE:
        Você está escrevendo exclusivamente sobre AUTOMODELISMO RÁDIO CONTROLADO (RC).

        Automodelismo RC envolve modelos em escala 1/5, 1/8, 1/10, 1/12 e Mini Z.

        Categorias:
        - On Road: Velocidade, Escala Realista e Drift
        - Off Road: Buggy, Truggy, Monster Truck, Crawler, Short Course

        Nunca escreva sobre:
        - Carros tamanho real
        - Veículos de rua
        - Fabricação de faróis, vidros ou janelas
        - Peças automotivas reais
        - Drift de carros reais
        - Monster trucks reais
        - Qualquer tipo de veículo fora do universo RC
        """

    # ==========================================
    # PROMPT PROFISSIONAL DEFINITIVO
    # ==========================================

    prompt = f"""
    Escreva um artigo completo para blog sobre:

    {tema}

    {blindagem_automodelismo}

    Requisitos obrigatórios:

    - Mínimo de 600 palavras (nunca menos que isso)
    - Ideal entre 700 e 900 palavras
    - Tom: {tom}
    - Foco em SEO: {seo_foco}
    - Linguagem natural e profissional
    - Não usar emojis
    - Não usar hashtags
    - Não usar símbolos como # ou *
    - Não usar marcações Markdown
    - Não numerar subtítulos
    - Não escrever HTML

    Estrutura obrigatória do texto:

    Introdução com 2 ou 3 parágrafos.

    Subtítulo claro (somente texto, sem símbolos).

    Desenvolvimento com 2 ou 3 parágrafos.

    Segundo subtítulo claro.

    Desenvolvimento com 2 ou 3 parágrafos.

    Terceiro subtítulo (se necessário).

    Desenvolvimento.

    Considerações Finais

    Parágrafo final estratégico e conclusivo.

    O texto deve vir totalmente limpo, apenas texto corrido.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Você é um redator profissional especialista em SEO."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=2500
    )

    texto = response.choices[0].message.content.strip()

    return texto
