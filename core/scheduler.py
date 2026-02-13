import json
from datetime import datetime

def carregar_config():
    with open("blogs_config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def blogs_do_dia():
    config = carregar_config()

    hoje = datetime.now()
    dia_semana = hoje.isoweekday()  # 1=Segunda ... 7=Domingo

    blogs_para_publicar = []

    for nome_blog, dados in config.items():
        if dia_semana in dados["dias"]:
            blogs_para_publicar.append({
                "nome": nome_blog,
                "blog_id": dados["blog_id"]
            })

    return blogs_para_publicar

