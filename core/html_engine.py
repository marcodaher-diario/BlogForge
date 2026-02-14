import re


def formatar_conteudo(conteudo):
    """
    Converte Markdown básico para HTML profissional
    """

    # Converter títulos em negrito para <h2>
    conteudo = re.sub(r"\*\*(.*?)\*\*", r"<h2>\1</h2>", conteudo)

    # Converter quebras de linha
    conteudo = conteudo.replace("\n", "<br><br>")

    return conteudo


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
            margin-bottom: 15px;
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
