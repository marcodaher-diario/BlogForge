import re
from datetime import datetime
from core.schema_engine import gerar_schema
from core.assinatura import BLOCO_FIXO_FINAL


def gerar_slug(titulo):
    slug = titulo.lower()
    slug = slug.replace(" ", "-")
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    return slug


def formatar_conteudo(conteudo):
    linhas = conteudo.split("\n")
    html_formatado = ""

    for linha in linhas:
        linha = linha.strip()

        if not linha:
            continue

        # Detectar subtítulos
        if linha.startswith("**") and linha.endswith("**"):
            titulo = linha.replace("**", "")
            html_formatado += f"""
<p style="color:#003366;font-family:Arial,sans-serif;
font-size:large;font-weight:bold;margin:25px 0 5px;text-align:left;">
{titulo}
</p>
"""
        else:
            html_formatado += f"""
<div style="color:#003366;font-family:Arial,sans-serif;
font-size:medium;margin:10px 0;text-align:justify;">
{linha}
</div>
"""

    return html_formatado


def gerar_html(titulo, conteudo, imagens, config):
    slug = gerar_slug(titulo)
    descricao = titulo
    data_atual = datetime.utcnow().strftime("%Y-%m-%d")

    # =========================
    # IMAGENS
    # =========================
    imagens_html = ""
    for img in imagens:
        imagens_html += f"""
<div style="margin:20px 0;text-align:center;">
<img src="{img}" 
style="aspect-ratio:16/9;border-radius:10px;
box-shadow:0 4px 8px rgba(0,0,0,0.1);
object-fit:cover;width:100%;" />
</div>
"""

    # =========================
    # SCHEMA JSON-LD
    # =========================
    schema = gerar_schema(config, titulo, descricao, imagens, slug)

    # =========================
    # OPEN GRAPH + TWITTER
    # =========================
    imagem_principal = imagens[0] if imagens else ""

    meta_social = f"""
<meta property="og:type" content="article">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descricao}">
<meta property="og:image" content="{imagem_principal}">
<meta property="og:url" content="{config['site_url']}{slug}.html">
<meta property="og:site_name" content="{config['nome_site']}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{titulo}">
<meta name="twitter:description" content="{descricao}">
<meta name="twitter:image" content="{imagem_principal}">
"""

    # =========================
    # CONTEÚDO FORMATADO
    # =========================
    corpo_formatado = formatar_conteudo(conteudo)

    # =========================
    # HTML FINAL
    # =========================
    html = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>{titulo}</title>
<meta name="description" content="{descricao}">
<meta name="author" content="{config.get('autor', 'Marco Daher')}">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link rel="canonical" href="{config['site_url']}{slug}.html">

{meta_social}

{schema}

</head>

<body>

<div style="line-height:1.6;max-width:800px;margin:auto;padding:10px;">

<h1 style="color:#003366;font-family:Arial,sans-serif;
font-size:x-large;font-weight:bold;
margin-bottom:20px;text-align:center;">
{titulo.upper()}
</h1>

{imagens_html}

{corpo_formatado}

</div>

{BLOCO_FIXO_FINAL}

</body>
</html>
"""

    return html
