from datetime import datetime


def gerar_schema(config, titulo, descricao, imagens, slug):
    schema_type = config.get("schema_type", "Article")
    autor = config.get("autor", "Marco Daher")
    site_url = config.get("site_url", "")
    nome_site = config.get("nome_site", "")
    logo_url = config.get("logo_url", "")

    data_atual = datetime.utcnow().strftime("%Y-%m-%d")

    imagem_principal = imagens[0] if imagens else ""

    url_canonica = f"{site_url}{slug}.html"

    schema = f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "{schema_type}",
  "headline": "{titulo}",
  "description": "{descricao}",
  "image": "{imagem_principal}",
  "author": {{
    "@type": "Person",
    "name": "{autor}"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "{nome_site}",
    "logo": {{
      "@type": "ImageObject",
      "url": "{logo_url}"
    }}
  }},
  "datePublished": "{data_atual}",
  "dateModified": "{data_atual}",
  "mainEntityOfPage": {{
    "@type": "WebPage",
    "@id": "{url_canonica}"
  }}
}}
</script>
"""
    return schema
