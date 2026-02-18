import json
import re
from datetime import datetime
from core.assinatura import BLOCO_FIXO_FINAL


def gerar_html(blog_nome, titulo, conteudo, imagens, config_blog):
    """
    Gera HTML profissional definitivo seguindo padrão estrutural fixo:
    - Título x-large Arial #003366
    - 2 imagens grandes centralizadas
    - Subtítulos large Arial #003366
    - Texto medium Arial #003366
    - Imagem 2 após segundo bloco de conteúdo
    - Considerações Finais como subtítulo
    """

    data_publicacao = datetime.now().strftime("%Y-%m-%d")
    autor = "Marco Daher"

    url_base = config_blog.get("url_base", "")
    slug = re.sub(r"[^a-z0-9-]", "", titulo.lower().replace(" ", "-"))
    canonical = f"{url_base}/{slug}" if url_base else url_base

    imagem_topo = imagens[0] if len(imagens) > 0 else None
    imagem_intermediaria = imagens[1] if len(imagens) > 1 else None

    # ==============================
    # JSON-LD
    # ==============================

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

    if imagem_topo:
        json_ld["image"] = imagem_topo

    json_ld_str = json.dumps(json_ld, ensure_ascii=False, indent=2)

    # ==============================
    # PROCESSAMENTO DO CONTEÚDO
    # ==============================

    linhas = conteudo.split("\n")
    html_conteudo = ""
    contador_blocos = 0

    for linha in linhas:
        linha = linha.strip()

        if not linha:
            continue

        # INTRODUÇÃO
        if linha.upper().startswith("INTRODUÇÃO:"):
            continue

        # SUBTÍTULO
        if linha.upper().startswith("SUBTITULO:"):
            subtitulo = linha.replace("SUBTITULO:", "").strip()

            html_conteudo += f"""
<h2 style="font-family: Arial; font-size: large; color: #003366; margin-top: 30px;">
{subtitulo}
</h2>
"""
            continue

        # CONSIDERAÇÕES FINAIS
        if linha.upper().startswith("CONSIDERAÇÕES FINAIS"):
            html_conteudo += """
<h2 style="font-family: Arial; font-size: large; color: #003366; margin-top: 30px;">
Considerações Finais
</h2>
"""
            continue

        # PARÁGRAFO NORMAL
        contador_blocos += 1

        html_conteudo += f"""
<p style="font-family: Arial; font-size: medium; color: #003366; text-align: justify; margin-bottom: 18px;">
{linha}
</p>
"""

        # Inserir imagem intermediária após segundo bloco de conteúdo
        if contador_blocos == 2 and imagem_intermediaria:
            html_conteudo += f"""
<div style="text-align: center; margin: 30px 0;">
    <img src="{imagem_intermediaria}" 
         style="width: 100%; max-width: 800px; border-radius: 10px;">
</div>
"""

    # ==============================
    # HTML FINAL
    # ==============================

    html = f"""<!DOCTYPE html>
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
{"<meta property='og:image' content='" + imagem_topo + "'>" if imagem_topo else ""}

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{titulo}">
<meta name="twitter:description" content="{titulo}">
{"<meta name='twitter:image' content='" + imagem_topo + "'>" if imagem_topo else ""}

<script type="application/ld+json">
{json_ld_str}
</script>

</head>

<body style="max-width: 800px; margin: auto; padding: 20px;">

<h1 style="font-family: Arial; font-size: x-large; color: #003366; text-align: center; margin-bottom: 25px;">
{titulo}
</h1>

{"<div style='text-align: center; margin: 30px 0;'><img src='" + imagem_topo + "' style='width: 100%; max-width: 800px; border-radius: 10px;'></div>" if imagem_topo else ""}

{html_conteudo}

{BLOCO_FIXO_FINAL}

</body>
</html>
"""

    return html
