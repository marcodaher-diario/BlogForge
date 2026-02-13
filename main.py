import json
from core.scheduler import blogs_do_dia

def carregar_config_blog(nome_blog):
    caminho = f"blogs/{nome_blog}/config.json"
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

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
        print("-" * 40)

if __name__ == "__main__":
    main()
