import json
import random
from core.scheduler import blogs_do_dia
from core.content_engine import gerar_conteudo
from core.image_engine import buscar_imagens_16_9
from core.html_engine import gerar_html

def carregar_config_blog(nome_blog):
    caminho = f"blogs/{nome_blog}/config.json"
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_temas(nome_blog):
    caminho = f"blogs/{nome_blog}/temas.txt"
    with open(caminho, "r", encoding="utf-8") as f:
        temas = [linha.strip() for linha in f if linha.strip()]
    return temas

def main():
    blogs = blogs_do_dia()

    if not blogs:
        print("Nenhum blog programado para hoje.")
        return

    print("Blogs programados para hoje:\n")

    for blog in blogs:
        nome = blog["nome"]
        blog_id = blog["blog_id"]

        print(f"Blog: {nome}")
        print(f"Blog ID: {blog_id}")

        config = carregar_config_blog(nome)
        print("Config carregado:")
        print(config)

        temas = carregar_temas(nome)

        if not temas:
            print("Nenhum tema encontrado!")
            print("-" * 40)
            continue

        tema_escolhido = random.choice(temas)
        print(f"Tema escolhido: {tema_escolhido}")

        print("Gerando conteúdo com IA...")
        conteudo = gerar_conteudo(tema_escolhido, config)

        print("Buscando imagens 16:9...")
        imagens = buscar_imagens_16_9(tema_escolhido, config["quantidade_imagens"])

        print("Imagens selecionadas:")
        for img in imagens:
            print(img)

        print("\nPrévia do conteúdo gerado:")
        print(conteudo[:500])
        print("-" * 40)

print("Gerando HTML estruturado...")

html_final = gerar_html(tema_escolhido, conteudo, imagens)

arquivo_preview = f"preview/{nome}_preview.html"

with open(arquivo_preview, "w", encoding="utf-8") as f:
    f.write(html_final)

print(f"Arquivo HTML salvo em: {arquivo_preview}")


if __name__ == "__main__":
    main()
