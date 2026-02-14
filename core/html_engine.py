from datetime import datetime
from core.assinatura import BLOCO_FIXO_FINAL


def gerar_html(titulo, conteudo, imagens, blog_nome, blog_url):

    data_publicacao = datetime.now().strftime("%Y-%m-%d")
    descricao = titulo

    # ==========================================
    # DEFINIÇÃO DO TIPO DE ARTIGO
    # ==========================================
    if "noticia" in blog_nome.lower() or "diario" in blog_nome.lower():
        tipo_schema = "NewsArticle"
    else:
        tipo_schema = "BlogPosting"

    # ==========================================
    # IMAGEM PRINCIPAL
    # ==========================================
    imagem_principal = imagens[0] if imagens else ""

    # ==========================================
    # TRATAR CONTEÚDO ANTES DA F-STRING
    # ==========================================
    conteudo_formatado = conteudo.replace("\n", "<br><br>")

    # ==========================================
    # JSON-LD
    # ==========================================
    json_ld = f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "{tipo_schema}",
  "headline": "{titulo}",
  "description": "{descricao}",
  "author": {{
    "@type": "Person",
    "name": "Marco Daher"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "{blog_nome}",
    "logo": {{
      "@type": "ImageObject",
      "url": "{blog_url}/favicon.ico"
    }}
  }},
  "datePublished": "{data_publicacao}",
  "dateModified": "{data_publicacao}",
  "mainEntityOfPage": "{blog_url}",
  "image": "{imagem_principal}"
}}
</script>
"""

    # ==========================================
    # OPEN GRAPH
    # ==========================================
    open_graph = f"""
<meta property="og:type" content="article">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descricao}">
<meta property="og:image" content="{imagem_principal}">
<meta property="og:url" content="{blog_url}">
<meta property="og:site_name" content="{blog_nome}">
"""

    # ==========================================
    # TWITTER CARD
    # ==========================================
    twitter_card = f"""
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{titulo}">
<meta name="twitter:description" content="{descricao}">
<meta name="twitter:image" content="{imagem_principal}">
"""

    # ==========================================
    # IMAGENS NO CORPO
    # ==========================================
    imagens_html = ""
    for img in imagens:
        imagens_html += f"""
        <div style="margin: 30px 0px; text-align: center;">
            <img src="{img}" style="aspect-ratio: 16/9; border-radius: 10px; box-shadow: rgba(0,0,0,0.1) 0px 4px 8px; object-fit: cover; width: 100%;" />
        </div>
        """

    # ==========================================
    # HTML FINAL
    # ==========================================
    html_final = f"""
{json_ld}
{open_graph}
{twitter_card}

<div style="line-height: 1.6;">

    <h1 style="color: #003366; font-family: Arial, sans-serif; font-size: x-large; font-weight: bold; margin-bottom: 20px; text-align: center;">
        {titulo.upper()}
    </h1>

    {imagens_html}

    <div style="color: #003366; font-family: Arial, sans-serif; font-size: medium; margin: 10px 0px; text-align: justify;">
        {conteudo_formatado}
    </div>

</div>

{BLOCO_FIXO_FINAL}
"""

    return html_final
