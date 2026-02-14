import json
import random
import os
from datetime import datetime

from core.scheduler import blogs_do_dia
from core.content_engine import gerar_conteudo
from core.image_engine import buscar_imagens_16_9
from core.html_engine import gerar_html


# ==========================================
# CARREGAR CONFIG DO BLOG
# ==========================================
def carregar_config_blog(nome_blog):
    caminho = f"blogs/{nome_blog}/config.json"
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


# ==========================================
# CARREGAR TEMAS
# ==========================================
def carregar_temas(nome_blog):
    caminho = f"blogs/{nome_blog}/temas.txt"
    with open(caminho, "r", encoding="utf-8") as f:
        temas = [linha.strip() for linha in f if linha.strip()]
    return temas


# ==========================================
# GERAR PREVIEW HTML
# ==========================================
def salvar_preview(nome_blog, html_final):
    os.makedirs("preview", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_preview = f"preview/{nome_blog}_{timestamp}.html"

    with open(arquivo_preview, "w", encoding="utf-8") as f:
        f.write(html_final)

    print(f"Preview salvo em: {arquivo_preview}")


# ==========================================
# TESTE COMPLETO DE CARGA
# ==========================================
def main():

    print("\n===== TESTE COMPLETO DE CARGA =====\n")

    blogs = blogs_do_dia()

    if not blogs:
        print("Nenhum blog programado para hoje.")
        return

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

        # QUANTIDADE DE POSTS POR EXECUÇÃO (teste de carga)
        quantidade_posts = 3

        for i in range(quantidade_posts):

            print(f"\n--- Gerando post {i+1} de {quantidade_posts} ---")

            tema_escolhido = random.choice(temas)
            print(f"Tema escolhido: {tema_escolhido}")

            # ======================================
            # GERAR CONTEÚDO
            # ======================================
            print("Gerando conteúdo com IA...")
            conteudo = gerar_conteudo(tema_escolhido, config)

            # ======================================
            # BUSCAR IMAGENS
            # ======================================
            imagens = []

            if config.get("usar_imagens", False):
                print("Buscando imagens 16:9...")
                imagens = buscar_imagens_16_9(
                    tema_escolhido,
                    config.get("quantidade_imagens", 1)
                )

            # ======================================
            # GERAR HTML ESTRUTURADO
            # ======================================
            print("Gerando HTML estruturado...")

            html_final = gerar_html(
                titulo=tema_escolhido,
                conteudo=conteudo,
                imagens=imagens,
                blog_nome=nome,
                blog_url=config.get("url", "")
            )

            # ======================================
            # SALVAR PREVIEW
            # ======================================
            salvar_preview(nome, html_final)

    print("\n===== TESTE FINALIZADO COM SUCESSO =====\n")


# ==========================================
# EXECUÇÃO
# ==========================================
if __name__ == "__main__":
    main()
