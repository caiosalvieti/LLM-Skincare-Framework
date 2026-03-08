import json
import re

# Carrega o banco de conhecimento de palavras-chave
def load_keywords(filepath: str = "data/keywords.json"):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)["keywords"]

def match(response_text: str, keyword: str) -> int:
    """
    Função indicadora binária que retorna 1 se a palavra-chave existir na resposta, e 0 caso contrário[cite: 33].
    Usamos expressões regulares para garantir que buscamos a palavra exata (case-insensitive).
    """
    pattern = rf"\b{re.escape(keyword.lower())}\b"
    if re.search(pattern, response_text.lower()):
        return 1
    return 0

def consistency_function(response_text: str, tau: int = 50) -> int:
    """
    Função de consistência C(R) que avalia o comprimento da resposta L(R).
    Retorna 5 se L(R) >= tau, e -5 se L(R) < tau.
    """
    L_R = len(response_text)
    if L_R >= tau:
        return 5
    else:
        return -5

def calculate_score(response_text: str, tau: int = 50) -> float:
    """
    Calcula a pontuação final usando a fórmula matemática interpretável[cite: 24].
    """
    keywords_db = load_keywords()
    
    # R representa a string de texto da resposta do modelo [cite: 29]
    R = response_text
    
    # Soma ponderada
    weighted_sum = 0.0
    for item in keywords_db:
        k_i = item["keyword"]
        w_i = item["weight"]
        # Acumula o peso * match
        weighted_sum += w_i * match(R, k_i)
        
    # Adiciona a função de consistência C(R)
    C_R = consistency_function(R, tau)
    
    final_score = weighted_sum + C_R
    return final_score