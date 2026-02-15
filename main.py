import os
import json
from datetime import datetime

from core.scheduler import blogs_do_dia
from core.content_engine import gerar_conteudo
from core.image_engine import buscar_imagens_16_9
from core.html_engine import gerar_html
from core.ideas_engine import obter_tema


# ==========================================
# CONFIGURAÇÕES
# ==========================================

POSTS_POR_BLOG = 3
GERAR_IMAGENS = True


# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def carregar_config_blog(nome_blog):
    caminho = f"blogs/{nome_blog}/config.json"

    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Config não encontrada para {nome_blog}")

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_preview(nome_blog, html):
    os.makedirs("preview", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"preview/{nome_blog}_{timestamp}.html"

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Preview salvo em: {nome_arquivo}")


# ==========================================
# SISTEMA PRINCIPAL
# ==========================================

def main():
    print("\n===== SISTEMA HÍBRIDO PROFISSIONAL =====\n")

    blogs = blogs_do_dia()

    if not blogs:
        print("Nenhum blog programado.")
        return

    for blog in blogs:
        nome = blog["nome"]
        blog_id = blog["blog_id"]

        print(f"\nBlog: {nome}")
        print(f"Blog ID: {blog_id}")

        try:
            config = carregar_config_blog(nome)
        except FileNotFoundError as e:
            print(f"ERRO: {e}")
            continue

        for i in range(POSTS_POR_BLOG):
            print(f"\n--- Gerando post {i+1} de {POSTS_POR_BLOG} ---")

            # =====================================
            # BANCO INFINITO INTELIGENTE DE TEMAS
            # =====================================
            tema_escolhido = obter_tema(nome, config)
            print(f"Tema escolhido: {tema_escolhido}")

            # =====================================
            # GERAR CONTEÚDO
            # =====================================
            print("Gerando conteúdo com IA...")
            conteudo = gerar_conteudo(tema_escolhido, config)

            # =====================================
            # GERAR IMAGENS
            # =====================================
            imagens = []

            if GERAR_IMAGENS and config.get("usar_imagens", True):
                print("Buscando imagens 16:9...")
                try:
                    imagens = buscar_imagens_16_9(
                        tema_escolhido,
                        config.get("quantidade_imagens", 2)
                    )
                except Exception as e:
                    print(f"Erro ao buscar imagens: {e}")

            # =====================================
            # GERAR HTML ESTRUTURADO
            # =====================================
            print("Gerando HTML estruturado...")
            html_final = gerar_html(
                blog_nome=nome,
                titulo=tema_escolhido,
                conteudo=conteudo,
                imagens=imagens,
                config_blog=config
            )

            salvar_preview(nome, html_final)

    print("\n===== SISTEMA FINALIZADO COM SUCESSO =====\n")


if __name__ == "__main__":
    main()
