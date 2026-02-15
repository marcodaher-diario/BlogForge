import json
import re
from datetime import datetime
from core.assinatura import BLOCO_FIXO_FINAL


def processar_conteudo(conteudo):
    """
    Converte markdown simples em HTML estruturado:
    - **Título** → <h2>
    - * item → lista <ul><li>
    - Parágrafos normais → <p>
    """

    linhas = conteudo.split("\n")
    html = ""
    em_lista = False

    for linha in linhas:
        linha = linha.strip()

        if not linha:
            continue

        # ==========================
        # SUBTÍTULO
        # ==========================
        if re.match(r"\*\*(.*?)\*\*", linha):
            if em_lista:
                html += "</ul>"
                em_lista = False

            titulo = re.sub(r"\*\*(.*?)\*\*", r"\1", linha)
            html += f"""
<h2 style="color:#0b5394;margin-top:30px;margin-bottom:10px;font-family:Arial;">
{titulo}
</h2>
"""
            continue

        # ==========================
        # LISTA
        # ==========================
        if linha.startswith("* "):
            if not em_lista:
                html += "<ul style='margin:15px 0 20px 20px;font-family:Arial;color:#003366;'>"
                em_lista = True

            item = linha[2:]
            html += f"<li style='margin-bottom:8px;'>{item}</li>"
            continue

        else:
            if em_lista:
                html += "</ul>"
                em_lista = False

        # ==========================
        # PARÁGRAFO
        # ==========================
        html += f"""
<p style="color:#003366;font-family:Arial;line-height:1.7;margin:15px 0;text-align:justify;">
{linha}
</p>
"""

    if em_lista:
        html += "</ul>"

    return html


def gerar_html(blog_nome, titulo, conteudo, imagens, config_blog):

    data_publicacao = datetime.now().strftime("%Y-%m-%d")
    autor = "Marco Daher"
    descricao = titulo

    url_base = config_blog.get("url_base", "")
    canonical = url_base if url_base else ""

    imagem_principal = imagens[0] if imagens else ""

    # ==========================
    # JSON-LD
    # ==========================

    json_ld = {
        "@context": "https://schema.org",
        "@type": config_blog.get("schema_type", "BlogPosting"),
        "headline": titulo,
        "description": descricao,
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
        "mainEntityOfPage": url_base,
        "image": imagem_principal
    }

    json_ld_str = json.dumps(json_ld, ensure_ascii=False, indent=2)

    # ==========================
    # PROCESSAR CONTEÚDO
    # ==========================

    corpo_formatado = processar_conteudo(conteudo)

    # ==========================
    # IMAGENS
    # ==========================

    imagens_html = ""

    for img in imagens:
        imagens_html += f"""
<div style="margin:25px 0;text-align:center;">
    <img src="{img}" 
         style="max-width:100%;height:auto;border-radius:10px;
                box-shadow:0 4px 8px rgba(0,0,0,0.1);" />
</div>
"""

    # ==========================
    # HTML FINAL
    # ==========================

    html = f"""
<script type="application/ld+json">
{json_ld_str}
</script>

<meta property="og:type" content="article">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descricao}">
<meta property="og:image" content="{imagem_principal}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{blog_nome}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{titulo}">
<meta name="twitter:description" content="{descricao}">
<meta name="twitter:image" content="{imagem_principal}">

<div style="max-width:800px;margin:auto;line-height:1.6;">

<h1 style="color:#003366;font-family:Arial;
           font-size:28px;font-weight:bold;
           margin:20px 0;text-align:center;">
{titulo.upper()}
</h1>

{imagens_html}

{corpo_formatado}

</div>

{BLOCO_FIXO_FINAL}
"""

    return html
