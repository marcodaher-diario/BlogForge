import json
import re
from datetime import datetime
from core.assinatura import BLOCO_FIXO_FINAL


def converter_markdown_simples(texto):
    """
    Converte:
    **Título** -> <h2>
    * item -> lista
    Parágrafos normais -> <p>
    """

    linhas = texto.split("\n")
    html = ""
    em_lista = False

    for linha in linhas:
        linha = linha.strip()

        if not linha:
            continue

        # Subtítulos
        if linha.startswith("**") and linha.endswith("**"):
            if em_lista:
                html += "</ul>"
                em_lista = False
            titulo = linha.replace("**", "")
            html += f"<h2>{titulo}</h2>"
            continue

        # Lista
        if linha.startswith("* "):
            if not em_lista:
                html += "<ul>"
                em_lista = True
            item = linha[2:]
            html += f"<li>{item}</li>"
            continue
        else:
            if em_lista:
                html += "</ul>"
                em_lista = False

        # Parágrafo
        html += f"<p>{linha}</p>"

    if em_lista:
        html += "</ul>"

    return html


def gerar_html(blog_nome, titulo, conteudo, imagens, config_blog):

    data_publicacao = datetime.now().strftime("%Y-%m-%d")
    autor = "Marco Daher"

    url_base = config_blog.get("url_base", "")
    slug = re.sub(r"[^a-z0-9-]", "", titulo.lower().replace(" ", "-"))
    canonical = f"{url_base}/{slug}" if url_base else url_base

    imagem_principal = imagens[0] if imagens else None

    # JSON-LD
    json_ld = {
        "@context": "https://schema.org",
        "@type": config_blog.get("schema_type", "BlogPosting"),
        "headline": titulo,
        "description": titulo,
        "author": {
            "@type": "Person",
            "name": autor
        },
        "publisher": {
            "@type": "Organization",
            "name": blog_nome
        },
        "datePublished": data_publicacao,
        "dateModified": data_publicacao,
        "mainEntityOfPage": canonical
    }

    if imagem_principal:
        json_ld["image"] = imagem_principal

    json_ld_str = json.dumps(json_ld, ensure_ascii=False, indent=2)

    # Converter conteúdo
    conteudo_html = converter_markdown_simples(conteudo)

    # Imagem principal
    imagem_html = ""
    if imagem_principal:
        imagem_html = f"""
        <div class="post-image">
            <img src="{imagem_principal}" alt="{titulo}">
        </div>
        """

    html = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>{titulo}</title>
<meta name="description" content="{titulo}">
<meta name="author" content="{autor}">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="canonical" href="{canonical}">

<meta property="og:type" content="article">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{titulo}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{blog_nome}">
"""

    if imagem_principal:
        html += f'<meta property="og:image" content="{imagem_principal}">\n'

    html += f"""
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{titulo}">
<meta name="twitter:description" content="{titulo}">
"""

    if imagem_principal:
        html += f'<meta name="twitter:image" content="{imagem_principal}">\n'

    html += f"""
<script type="application/ld+json">
{json_ld_str}
</script>

<style>
body {{
    font-family: Arial, sans-serif;
    line-height: 1.8;
    max-width: 800px;
    margin: auto;
    padding: 20px;
    color: #003366;
}}

h1 {{
    text-align: center;
    margin-bottom: 25px;
}}

h2 {{
    margin-top: 30px;
    margin-bottom: 10px;
    color: #0b5394;
}}

p {{
    margin-bottom: 18px;
    text-align: justify;
}}

ul {{
    margin-bottom: 20px;
}}

li {{
    margin-bottom: 10px;
}}

.post-image img {{
    width: 100%;
    border-radius: 10px;
    margin-bottom: 25px;
}}
</style>

</head>
<body>

<h1>{titulo.upper()}</h1>

{imagem_html}

{conteudo_html}

{BLOCO_FIXO_FINAL}

</body>
</html>
"""

    return html
