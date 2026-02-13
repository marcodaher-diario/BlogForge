import json
import random
from core.scheduler import blogs_do_dia

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
        print("-" * 40)

if __name__ == "__main__":
    main()
