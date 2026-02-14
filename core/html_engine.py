from datetime import datetime
from core.assinatura import BLOCO_FIXO_FINAL


def gerar_html(tema, conteudo, imagens, blog_nome, blog_url):
    """
    Gera HTML completo otimizado para SEO profissional
    """

    # =========================
    # DATA DINÂMICA
    # =========================
    data_publicacao = datetime.utcnow().isoformat()

    # =========================
    # IMAGEM PRINCIPAL
    # =========================
    imagem_principal = imagens[0] if imagens else ""

    # =========================
    # JSON-LD ESTRUTURADO
    # =========================
    json_ld = f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{tema}",
  "description": "{tema}",
  "image": "{imagem_principal}",
  "author": {{
    "@type": "Person",
    "name": "Marco Daher"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "{blog_nome}",
    "logo": {{
      "@type": "ImageObject",
      "url": "{imagem_principal}"
    }}
  }},
  "datePublished": "{data_publicacao}",
  "mainEntityOfPage": {{
    "@type": "WebPage",
    "@id": "{blog_url}"
  }}
}}
</script>
"""

    # =========================
    # IMAGENS NO CORPO
    # =========================
    imagens_html = ""
    for img in imagens:
        imagens_html += f"""
<div style="margin:20px 0;text-align:center;">
    <img src="{img}" style="aspect-ratio:16/9;width:100%;border-radius:10px;object-fit:cover;" />
</div>
"""

    # =========================
    # CONTEÚDO FORMATADO
    # =========================
    paragrafos = conteudo.split("\n")
    conteudo_formatado = ""

    for p in paragrafos:
        if p.strip():
            conteudo_formatado += f"""
<div style="color:#003366;font-family:Arial,sans-serif;font-size:medium;margin:10px 0;text-align:justify;">
{p}
</div>
"""

    # =========================
    # HTML FINAL
    # =========================
    html = f"""
<div style="line-height:1.6;">

<h1 style="color:#003366;font-family:Arial,sans-serif;font-size:x-large;font-weight:bold;margin-bottom:20px;text-align:center;">
{tema.upper()}
</h1>

{json_ld}

{imagens_html}

{conteudo_formatado}

</div>

{BLOCO_FIXO_FINAL}
"""

    return html
