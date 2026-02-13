import os
import google.generativeai as genai

def gerar_conteudo(tema, config_blog):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY não encontrada.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash-latest")

    prompt = f"""
    Aja como especialista em {config_blog['nicho']}.
    Escreva um artigo de aproximadamente {config_blog['tamanho_artigo']} palavras.
    Use um tom {config_blog['tom']}.
    Tema principal: {tema}.
    Foque em SEO para: {config_blog['seo_foco']}.
    Estruture com introdução, subtítulos e conclusão.
    Linguagem natural, profissional e original.
    """

    response = model.generate_content(prompt)

    return response.text
