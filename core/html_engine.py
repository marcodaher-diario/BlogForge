def gerar_html(titulo, conteudo, imagens):
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{titulo}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: auto;
                padding: 20px;
            }}
            h1 {{
                color: #073763;
            }}
            img {{
                width: 100%;
                margin: 20px 0;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <h1>{titulo}</h1>
    """

    for i, img in enumerate(imagens):
        if i == 0:
            html += f'<img src="{img}" alt="Imagem principal">\n'
        else:
            html += f'<img src="{img}" alt="Imagem complementar">\n'

    html += f"""
        <div>
            {conteudo.replace('\n', '<br><br>')}
        </div>
    </body>
    </html>
    """

    return html
