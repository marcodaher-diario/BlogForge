import re


def formatar_conteudo(conteudo):

    linhas = conteudo.split("\n")
    html_final = ""
    em_lista = False

    for linha in linhas:
        linha = linha.strip()

        if not linha:
            continue

        # Item de lista
        if linha.startswith("* "):
            if not em_lista:
                html_final += "<ul>\n"
                em_lista = True

            item = linha.replace("* ", "")

            match = re.match(r"\*\*(.*?)\*\*(.*)", item)
            if match:
                titulo = match.group(1)
                resto = match.group(2)
                html_final += f"<li><strong>{titulo}</strong>{resto}</li>\n"
            else:
                html_final += f"<li>{item}</li>\n"

        else:
            if em_lista:
                html_final += "</ul>\n"
                em_lista = False

            # Título principal
            if linha.startswith("**") and linha.endswith("**"):
                titulo = linha.replace("**", "")
                html_final += f"<h2>{titulo}</h2>\n"
            else:
                html_final += f"<p>{linha}</p>\n"

    if em_lista:
        html_final += "</ul>\n"

    return html_final


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
        ul {{
            margin-left: 20px;
            margin-bottom: 20px;
        }}
        li {{
            margin-bottom: 10px;
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
