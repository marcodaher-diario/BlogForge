import re


def formatar_conteudo(conteudo):
    """
    Converte Markdown básico em HTML estruturado profissional
    """

    # Converter títulos **Texto** para <h2>
    conteudo = re.sub(r"\*\*(.*?)\*\*", r"<h2>\1</h2>", conteudo)

    # Dividir por linhas duplas para criar parágrafos
    paragrafos = conteudo.split("\n\n")

    html_formatado = ""

    for p in paragrafos:
        p = p.strip()
        if not p:
            continue

        # Se já for título, não envolver em <p>
        if p.startswith("<h2>"):
            html_formatado += p + "\n"
        else:
            html_formatado += f"<p>{p}</p>\n"

    return html_formatado


def gerar_html(titulo, conteudo, imagens):

    conteudo_formatado = formatar_conteudo(conteudo)

    html = f"""
<html>
<head>
    <meta charset="UTF-8">
    <title>{titulo}</title>
    <meta name="description" content="{titulo}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #073763;
            margin-bottom: 20px;
        }}
        h2 {{
            margin-top: 30px;
            color: #0b5394;
        }}
        img {{
            width: 100%;
            margin: 25px 0;
            border-radius: 8px;
        }}
        p {{
            margin-bottom: 18px;
            text-align: justify;
        }}
    </style>
</head>
<body>

    <h1>{titulo}</h1>
"""

    for i, img in enumerate(imagens):
        if i == 0:
            html += f'<img src="{img}" alt="{titulo}">\n'
        else:
            html += f'<img src="{img}" alt="Imagem complementar">\n'

    html += f"""
    <div>
        {conteudo_formatado}
    </div>

</body>
</html>
"""

    return html
