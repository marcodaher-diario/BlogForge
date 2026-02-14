import os
import json
from datetime import datetime

from core.content_engine import gerar_conteudo
from core.image_engine import buscar_imagens
from core.html_engine import gerar_html
from core.editorial_engine import escolher_tema


# ==============================
# CONFIGURAÇÕES GERAIS
# ==============================

TESTE_CARGA = True
POSTS_POR_BLOG = 3


BLOGS = {
    "emagrecer": {
        "id": "5251820458826857223",
        "url": "https://emagrecendo100crise.blogspot.com/"
    },
    "dfbolhas": {
        "id": "4324376157396303471",
        "url": "https://dfbolhas.blogspot.com/"
    },
    "mdartefoto": {
        "id": "5852420775961497718",
        "url": "https://mdartefoto.blogspot.com/"
    },
    "diariodenoticias": {
        "id": "8284393764979637984",
        "url": "https://diariodenoticiasnovo.blogspot.com/"
    },
    "cursosnegocios": {
        "id": "0000000000000000000",
        "url": "https://cursosnegocioseoportunidades.blogspot.com/"
    }
}


# ==============================
# FUNÇÕES AUXILIARES
# ==============================

def carregar_config_blog(nome_blog):
    caminho = f"blogs/{nome_blog}/config.json"
    
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_preview(nome_blog, html):
    if not os.path.exists("preview"):
        os.makedirs("preview")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"preview/{nome_blog}_{timestamp}.html"

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Preview salvo em: {nome_arquivo}")


# ==============================
# EXECUÇÃO PRINCIPAL
# ==============================

def main():

    print("\n===== TESTE COMPLETO DE CARGA =====\n")

    for nome_blog, dados_blog in BLOGS.items():

        print(f"\nBlog: {nome_blog}")
        print(f"Blog ID: {dados_blog['id']}")

        try:
            config = carregar_config_blog(nome_blog)
        except Exception as e:
            print(f"❌ Erro ao carregar config: {e}")
            continue

        for i in range(POSTS_POR_BLOG):

            print(f"\n--- Gerando post {i+1} de {POSTS_POR_BLOG} ---")

            try:
                caminho_blog = f"blogs/{nome_blog}"
                tema_escolhido = escolher_tema(caminho_blog)

                print(f"Tema escolhido: {tema_escolhido}")

                print("Gerando conteúdo com IA...")
                conteudo = gerar_conteudo(tema_escolhido, config)

                imagens = []

                if config.get("usar_imagens", False):
                    print("Buscando imagens 16:9...")
                    imagens = buscar_imagens(
                        tema_escolhido,
                        config.get("quantidade_imagens", 1)
                    )

                print("Gerando HTML estruturado...")
                html_final = gerar_html(
                    titulo=tema_escolhido,
                    conteudo=conteudo,
                    imagens=imagens,
                    blog_nome=nome_blog,
                    blog_url=dados_blog["url"],
                    seo_foco=config.get("seo_foco", "")
                )

                salvar_preview(nome_blog, html_final)

            except Exception as e:
                print(f"❌ Erro ao gerar post: {e}")
                continue

    print("\n===== TESTE FINALIZADO COM SUCESSO =====\n")


if __name__ == "__main__":
    main()
