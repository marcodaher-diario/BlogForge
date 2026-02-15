import os
import json
import random
from datetime import datetime

from core.scheduler import blogs_do_dia
from core.content_engine import gerar_conteudo
from core.image_engine import buscar_imagens_16_9
from core.html_engine import gerar_html
from core.ideas_engine import gerar_tema_estrategico


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


def carregar_temas(nome_blog):
    caminho = f"blogs/{nome_blog}/temas.txt"

    if not os.path.exists(caminho):
        return []

    with open(caminho, "r", encoding="utf-8") as f:
        return [linha.strip() for linha in f if linha.strip()]


def salvar_preview(nome_blog, html):
    os.makedirs("preview", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"preview/{nome_blog}_{timestamp}.html"

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Preview salvo em: {nome_arquivo}")


# ==========================================
# ESCOLHA INTELIGENTE DE TEMA
# ==========================================

def escolher_tema(nome_blog, config):
    """
    Prioridade:
    1️⃣ temas.txt se existir
    2️⃣ banco estratégico automático por nicho
    """

    temas = carregar_temas(nome_blog)

    if temas:
        return random.choice(temas)

    nicho = config.get("nicho", "")
    return gerar_tema_estrategico(nicho)


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

            tema_escolhido = escolher_tema(nome, config)
            print(f"Tema escolhido: {tema_escolhido}")

            # ==============================
            # GERAR CONTEÚDO
            # ==============================
            print("Gerando conteúdo com IA...")
            conteudo = gerar_conteudo(tema_escolhido, config)

            # ==============================
            # GERAR IMAGENS
            # ==============================
            imagens = []

            if GERAR_IMAGENS and config.get("usar_imagens", True):
                print("Buscando imagens horizontais inteligentes...")
                try:
                    imagens = buscar_imagens_16_9(
                        tema_escolhido,
                        quantidade=config.get("quantidade_imagens", 2),
                        nicho=config.get("nicho")
                    )
                except Exception as e:
                    print(f"Erro ao buscar imagens: {e}")

            # ==============================
            # GERAR HTML
            # ==============================
            print("Gerando HTML estruturado...")
            try:
                html_final = gerar_html(
                    blog_nome=nome,
                    titulo=tema_escolhido,
                    conteudo=conteudo,
                    imagens=imagens,
                    config_blog=config
                )

                salvar_preview(nome, html_final)

            except Exception as e:
                print(f"Erro ao gerar HTML: {e}")

    print("\n===== SISTEMA FINALIZADO COM SUCESSO =====\n")


if __name__ == "__main__":
    main()
