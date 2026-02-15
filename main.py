import os
import json
import random
import time
from datetime import datetime

from core.scheduler import blogs_do_dia
from core.content_engine import gerar_conteudo
from core.image_engine import buscar_imagens_16_9
from core.html_engine import gerar_html


# ==========================================
# CONFIGURAÇÕES GERAIS
# ==========================================

POSTS_POR_BLOG = 3
GERAR_IMAGENS = True
HISTORICO_FILE = "data/historico_temas.json"


# ==========================================
# UTILITÁRIOS
# ==========================================

def carregar_config_blog(nome_blog):
    caminho = f"blogs/{nome_blog}/config.json"

    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Config não encontrada para {nome_blog}")

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def carregar_historico():
    if not os.path.exists(HISTORICO_FILE):
        return {}

    with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_historico(historico):
    os.makedirs("data", exist_ok=True)
    with open(HISTORICO_FILE, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)


def escolher_tema(nome_blog, config, historico):
    """
    Escolhe tema evitando repetição recente.
    Usa banco infinito se existir.
    """

    banco_ideias = config.get("banco_ideias", [])

    if not banco_ideias:
        return "Tema Estratégico Automático"

    temas_usados = historico.get(nome_blog, [])

    temas_disponiveis = [
        tema for tema in banco_ideias
        if tema not in temas_usados
    ]

    # Se acabou tudo, reinicia ciclo
    if not temas_disponiveis:
        historico[nome_blog] = []
        temas_disponiveis = banco_ideias

    tema = random.choice(temas_disponiveis)

    historico.setdefault(nome_blog, []).append(tema)

    # Limitar histórico a últimos 50
    historico[nome_blog] = historico[nome_blog][-50:]

    return tema


def salvar_preview(nome_blog, html):
    os.makedirs("preview", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamp += f"_{int(time.time()*1000)}"

    nome_arquivo = f"preview/{nome_blog}_{timestamp}.html"

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
        print("Nenhum blog programado para hoje.")
        return

    historico = carregar_historico()

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

            # ======================================
            # TEMA INTELIGENTE COM HISTÓRICO
            # ======================================

            tema_escolhido = escolher_tema(nome, config, historico)
            print(f"Tema escolhido: {tema_escolhido}")

            # ======================================
            # GERAR CONTEÚDO
            # ======================================

            print("Gerando conteúdo com IA...")
            try:
                conteudo = gerar_conteudo(tema_escolhido, config)
            except Exception as e:
                print(f"Erro ao gerar conteúdo: {e}")
                continue

            # ======================================
            # GERAR IMAGENS
            # ======================================

            imagens = []

            if GERAR_IMAGENS and config.get("usar_imagens", True):

                print("Buscando imagens horizontais inteligentes...")

                try:
                    imagens = buscar_imagens_16_9(
                        tema_escolhido,
                        quantidade=1,
                        nicho=config.get("nicho")
                    )
                except Exception as e:
                    print(f"Erro ao buscar imagens: {e}")
                    imagens = []

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

    salvar_historico(historico)

    print("\n===== SISTEMA FINALIZADO COM SUCESSO =====\n")


if __name__ == "__main__":
    main()
