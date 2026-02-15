import json
from datetime import datetime
from core.assinatura import BLOCO_FIXO_FINAL


def gerar_html(blog_nome, titulo, conteudo, imagens, config_blog):
    """
    Gera HTML estruturado completo com:
    - SEO profissional
    - JSON-LD dinâmico
    - OpenGraph
    - Twitter Cards
    - Canonical
    - Autor
    - Data dinâmica
    """

    data_publicacao = datetime.now().strftime("%Y-%m-%d")
    descricao = titulo
    autor = "Marco Daher"
    url_base = config_blog.get("url_base", "")
    canonical = f"{url_base}/{titulo.replace(' ', '-').lower()}" if url_base else ""

    imagem_principal = imagens[0] if imagens else ""

    # ==========================================
    # JSON-LD Article
    # ==========================================

    json_ld = {
        "@context": "https://schema.org",
        "@type": config_blog.get("schema_type", "BlogPosting"),
        "headline": titulo,
        "author": {
            "@type": "Person",
            "name": autor
        },
        "datePublished": data_publicacao,
        "image": imagem_principal,
        "publisher": {
            "@type": "Organization",
            "name": blog_nome
        }
    }

    json_ld_str = json.dumps(json_ld, ensure_ascii=False, indent=2)

    # ==========================================
    # Montagem do corpo do conteúdo
    # ==========================================

    conteudo_formatado = ""
    paragrafos = conteudo.split("\n")

    for p in paragrafos:
        if p.strip():
            conteudo_formatado += f"""
            <div style='color: #003366; font-family: Arial, sans-serif; font-size: medium; margin: 10px 0px; text-align: justify;'>
                {p.strip()}
            </div>
            """

    # ==========================================
    # Imagens formatadas
    # ==========================================

    imagens_html = ""

    for img in imagens:
        imagens_html += f"""
        <div style="margin: 30px 0px; text-align: center;">
            <img src="{img}" style="aspect-ratio: 16 / 9; border-radius: 10px; box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 8px; object-fit: cover; width: 100%;" />
        </div>
        """

    # ==========================================
    # HTML Final
    # ==========================================

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{titulo}</title>
<meta name="description" content="{descricao}">
<meta name="author" content="{autor}">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="canonical" href="{canonical}">

<!-- OpenGraph -->
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descricao}">
<meta property="og:type" content="article">
<meta property="og:image" content="{imagem_principal}">
<meta property="og:url" content="{canonical}">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{titulo}">
<meta name="twitter:description" content="{descricao}">
<meta name="twitter:image" content="{imagem_principal}">

<script type="application/ld+json">
{json_ld_str}
</script>

</head>

<body>

<div style="line-height: 1.6;">

<h1 style="color: #003366; font-family: Arial, sans-serif; font-size: x-large; font-weight: bold; margin-bottom: 20px; text-align: center;">
{titulo.upper()}
</h1>

{imagens_html}

{conteudo_formatado}

</div>

{BLOCO_FIXO_FINAL}

</body>
</html>
"""

    return html
