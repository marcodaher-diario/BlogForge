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

            # Se tiver **Titulo** dentro da linha
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

            # Títulos principais
            if linha.startswith("**") and linha.endswith("**"):
                titulo = linha.replace("**", "")
                html_final += f"<h2>{titulo}</h2>\n"
            else:
                html_final += f"<p>{linha}</p>\n"

    if em_lista:
        html_final += "</ul>\n"

    return html_final
