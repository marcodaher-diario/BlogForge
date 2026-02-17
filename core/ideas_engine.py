import random
import re
import os
import json

DATA_DIR = "data"
HISTORICO_FILE = os.path.join(DATA_DIR, "historico_temas.json")


# ==========================================
# ESTRUTURAS ESTRATÉGICAS POR NICHO
# ==========================================

ESTRUTURAS = {
    "saude": [
        "Como {keyword} de forma natural",
        "{keyword}: guia completo atualizado",
        "{keyword} funciona mesmo? Entenda a verdade",
        "Erros comuns sobre {keyword}",
        "{keyword} após os 40 anos: o que muda?",
        "O que ninguém te conta sobre {keyword}",
        "{keyword}: estratégia comprovada"
    ],

    "automodelismo": [
        "Guia definitivo sobre {keyword}",
        "Como melhorar {keyword} no seu RC",
        "Erros comuns em {keyword}",
        "Setup ideal para {keyword}",
        "{keyword}: dicas avançadas",
        "Tudo sobre {keyword} para iniciantes"
    ],

    "fotografia": [
        "Como dominar {keyword}",
        "Guia prático de {keyword}",
        "Erros que arruínam {keyword}",
        "{keyword}: técnica profissional explicada",
        "Segredos de {keyword}"
    ],

    "noticias": [
        "Entenda o impacto de {keyword}",
        "{keyword}: o que está acontecendo agora",
        "Análise completa sobre {keyword}",
        "Bastidores de {keyword}",
        "{keyword}: cenário atual e perspectivas"
    ]
}


# ==========================================
# PALAVRAS-CHAVE POR NICHO
# ==========================================

KEYWORDS = {
    "saude": [
        "emagrecimento saudável",
        "perda de gordura",
        "metabolismo acelerado",
        "dieta equilibrada",
        "hábitos saudáveis",
        "queima de gordura",
        "reeducação alimentar"
    ],

    "automodelismo": [
        "suspensão RC",
        "motor brushless",
        "bateria LiPo",
        "setup para pista",
        "drift RC",
        "manutenção preventiva",
        "bolha de policarbonato"
    ],

    "fotografia": [
        "fotografia noturna",
        "composição fotográfica",
        "luz natural",
        "edição no Photoshop",
        "fotografia profissional",
        "portfólio digital"
    ],

    "noticias": [
        "economia brasileira",
        "crise política",
        "reforma tributária",
        "mercado financeiro",
        "relações internacionais",
        "cenário eleitoral"
    ]
}


# ==========================================
# HISTÓRICO
# ==========================================

def carregar_historico():
    if not os.path.exists(HISTORICO_FILE):
        return {}

    with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_historico(historico):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(HISTORICO_FILE, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)


# ==========================================
# GERADOR DEFINITIVO
# ==========================================

def gerar_tema_estrategico(nicho):

    if nicho not in ESTRUTURAS:
        return "Conteúdo Estratégico Atualizado"

    historico = carregar_historico()

    if nicho not in historico:
        historico[nicho] = []

    tentativas = 0

    while tentativas < 50:

        estrutura = random.choice(ESTRUTURAS[nicho])
        keyword = random.choice(KEYWORDS[nicho])

        titulo = estrutura.replace("{keyword}", keyword)
        titulo = re.sub(r"^\d+\.\s*", "", titulo)

        if titulo not in historico[nicho]:
            historico[nicho].append(titulo)
            salvar_historico(historico)
            return titulo

        tentativas += 1

    # Se esgotar combinações, força expansão
    titulo_extra = f"{random.choice(KEYWORDS[nicho]).title()}: análise aprofundada e atualizada"
    historico[nicho].append(titulo_extra)
    salvar_historico(historico)
    return titulo_extra
