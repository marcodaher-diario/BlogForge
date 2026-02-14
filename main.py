import json
import random
import time
from core.scheduler import blogs_do_dia
from core.content_engine import gerar_conteudo
from core.image_engine import buscar_imagens_16_9
from core.html_engine import gerar_html

# ==============================
# CONFIG TESTE DE CARGA
# ==============================
POSTS_POR_BLOG = 3  # quantos posts gerar por blog no teste

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

    print("\n===== TESTE COMPLETO DE CARGA =====\n")

    for blog in blogs:
        nome = blog["nome"]
        blog_id = blog["blog_id"]

        print(f"\nBlog: {nome}")
        print(f"Blog ID: {blog_id}")

        config = carregar_config_blog(nome)
        temas = carregar_temas(nome)

        if not temas:
            print("Nenhum tema encontrado!")
            continue

        for i in range(POSTS_POR_BLOG):

            print(f"\n--- Gerando post {i+1} de {POSTS_POR_BLOG} ---")

            tema_escolhido = random.choice(temas)
            print(f"Tema escolhido: {tema_escolhido}")

            print("Gerando conteúdo com IA...")
            conteudo = gerar_conteudo(tema_escolhido, config)

            print("Buscando imagens 16:9...")
            imagens = []
            if config.get("usar_imagens", False):
                imagens = buscar_imagens_16_9(
                    tema_escolhido,
                    config.get("quantidade_imagens", 1)
                )

            print("Gerando HTML estruturado...")
            html_final = gerar_html(
                titulo=tema_escolhido,
                conteudo=conteudo,
                imagens=imagens,
                config=config,
                blog_nome=nome
            )

            # Nome único para evitar sobrescrever arquivos
            timestamp = int(time.time())
            arquivo_preview = f"preview/{nome}_{timestamp}_{i}.html"

            with open(arquivo_preview, "w", encoding="utf-8") as f:
                f.write(html_final)

            print(f"Preview salvo em: {arquivo_preview}")

    print("\n===== TESTE FINALIZADO =====\n")


if __name__ == "__main__":
    main()
