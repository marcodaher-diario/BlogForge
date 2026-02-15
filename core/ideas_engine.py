import random
import re


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
        "{keyword}: estratégia comprovada",
    ],

    "automodelismo": [
        "Guia definitivo sobre {keyword}",
        "Como melhorar {keyword} no seu RC",
        "Erros comuns em {keyword}",
        "Setup ideal para {keyword}",
        "{keyword}: dicas avançadas",
        "Tudo sobre {keyword} para iniciantes",
    ],

    "fotografia": [
        "Como dominar {keyword}",
        "Guia prático de {keyword}",
        "Erros que arruínam {keyword}",
        "{keyword}: técnica profissional explicada",
        "Segredos de {keyword}",
    ],

    "noticias": [
        "Entenda o impacto de {keyword}",
        "{keyword}: o que está acontecendo agora",
        "Análise completa sobre {keyword}",
        "Bastidores de {keyword}",
        "{keyword}: cenário atual e perspectivas",
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
# GERADOR PRINCIPAL
# ==========================================

def gerar_tema_estrategico(nicho):

    if nicho not in ESTRUTURAS:
        return "Conteúdo Estratégico Atualizado"

    estrutura = random.choice(ESTRUTURAS[nicho])
    keyword = random.choice(KEYWORDS[nicho])

    titulo = estrutura.replace("{keyword}", keyword)

    # Remove numeração automática
    titulo = re.sub(r"^\d+\.\s*", "", titulo)

    return titulo
