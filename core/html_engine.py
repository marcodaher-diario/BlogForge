from core.assinatura import BLOCO_FIXO_FINAL


def gerar_html(titulo, conteudo, imagens):
    # Container principal do Blogger
    html = '<div style="line-height: 1.6;">\n'

    # Título
    html += f'''
    <h1 style="color: #003366; font-family: Arial, sans-serif; font-size: x-large; font-weight: bold; margin-bottom: 20px; text-align: center;">
        {titulo.upper()}
    </h1>
    '''

    # Inserir imagens (uma abaixo do título e outras distribuídas)
    for img in imagens:
        html += f'''
        <div style="color: #003366; font-family: Arial, sans-serif; margin-bottom: 20px; text-align: center;">
            <img src="{img}" style="aspect-ratio: 16 / 9; border-radius: 10px; box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 8px; object-fit: cover; width: 100%;" />
        </div>
        '''

    # Converter markdown simples para HTML básico
    conteudo_html = conteudo.replace("**", "")
    conteudo_html = conteudo_html.replace("\n\n", "</div><div style='color: #003366; font-family: Arial, sans-serif; font-size: medium; margin: 10px 0px; text-align: justify;'>")

    html += f'''
    <div style="color: #003366; font-family: Arial, sans-serif; font-size: medium; margin: 10px 0px; text-align: justify;">
        {conteudo_html}
    </div>
    '''

    html += "</div>\n"

    # Anexar assinatura oficial
    html += BLOCO_FIXO_FINAL

    return html
