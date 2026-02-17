import os
import json
import random
import time
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
HISTORICO_LIMITE = 50


# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def carregar_config_blog(nome_blog):
    caminho = f"blogs/{nome_blog}/config.json"

    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Config não encontrada para {nome_blog}")

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def carregar_historico(nome_blog):
    caminho = f"blogs/{nome_blog}/historico_temas.json"

    if not os.path.exists(caminho):
        return []

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_historico(nome_blog, historico):
    caminho = f"blogs/{nome_blog}/historico_temas.json"
    os.makedirs(f"blogs/{nome_blog}", exist_ok=True)

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(historico[-HISTORICO_LIMITE:], f, indent=2, ensure_ascii=False)


def gerar_tema_unico(nicho, historico):
    tentativas = 0

    while tentativas < 20:
        tema = gerar_tema_estrategico(nicho)

        if tema not in historico:
            return tema

        tentativas += 1

    # fallback se tudo repetir
    return gerar_tema_estrategico(nicho)


def salvar_preview(nome_blog, html):
    os.makedirs("preview", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    millis = int(time.time() * 1000)

    nome_arquivo = f"preview/{nome_blog}_{timestamp}_{millis}.html"

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Preview salvo em: {nome_arquivo}")


# ==========================================
# SISTEMA PRINCIPAL
# ==========================================

def main():
    print("\n===== SISTEMA PROFISSIONAL DEFINITIVO =====\n")

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

        nicho = config.get("nicho", "")
        historico = carregar_historico(nome)

        for i in range(POSTS_POR_BLOG):
            print(f"\n--- Gerando post {i+1} de {POSTS_POR_BLOG} ---")

            # ======================================
            # GERAR TEMA ESTRATÉGICO ÚNICO
            # ======================================

            tema_escolhido = gerar_tema_unico(nicho, historico)
            print(f"Tema escolhido: {tema_escolhido}")

            historico.append(tema_escolhido)

            # ======================================
            # GERAR CONTEÚDO
            # ======================================

            print("Gerando conteúdo com IA...")
            conteudo = gerar_conteudo(tema_escolhido, config)

            # ======================================
            # GERAR IMAGENS INTELIGENTES
            # ======================================

            imagens = []

            if GERAR_IMAGENS and config.get("usar_imagens", True):
                print("Buscando imagens horizontais inteligentes...")
                try:
                    imagens = buscar_imagens_16_9(
                        tema_escolhido,
                        quantidade=1,
                        nicho=nicho
                    )
                except Exception as e:
                    print(f"Erro ao buscar imagens: {e}")

            # ======================================
            # GERAR HTML
            # ======================================

            print("Gerando HTML estruturado...")
            try:
                html_final = gerar_html(
                    blog_nome=nome,
                    titulo=tema_escolhido,
                    conteudo=conteudo,
                    imagens=imagens,
                    config_blog=config
                )
            except Exception as e:
                print(f"Erro ao gerar HTML: {e}")
                continue

            salvar_preview(nome, html_final)

        # salva histórico após todos os posts do blog
        salvar_historico(nome, historico)

    print("\n===== SISTEMA FINALIZADO COM SUCESSO =====\n")


if __name__ == "__main__":
    main()
