# ============================================================

# CONVERSOR DE MOEDAS

# API usada: https://www.frankfurter.app (gratuita, sem cadastro)

# ============================================================

# Importa as bibliotecas necessárias

import requests  # faz chamadas à internet (HTTP)
import json      # lida com dados no formato JSON

# –– CONFIGURAÇÕES ––

# Moeda de origem e destino (formato ISO 4217)

moeda_origem = “USD”   # ex: USD, BRL, EUR, GBP, JPY
moeda_destino = “BRL”

# Valor que você quer converter

valor = 100

# –– CHAMADA À API ––

# Monta a URL com os parâmetros de conversão

url = f”https://api.frankfurter.app/latest?amount={valor}&from={moeda_origem}&to={moeda_destino}”

# Faz a requisição GET e guarda a resposta

resposta = requests.get(url)

# Converte o retorno da API (texto JSON) para dicionário Python

dados = resposta.json()

# –– EXTRAÇÃO DO RESULTADO ––

# A API retorna um dicionário com a chave “rates”

# Dentro dela, o valor convertido está indexado pela moeda destino

valor_convertido = dados[“rates”][moeda_destino]

# Pega a taxa de câmbio implícita (valor convertido dividido pelo original)

taxa = valor_convertido / valor

# –– EXIBIÇÃO ––

# Imprime o resultado de forma legível

print(f”\n  {valor:.2f} {moeda_origem} = {valor_convertido:.2f} {moeda_destino}”)
print(f”  Taxa de câmbio: 1 {moeda_origem} = {taxa:.4f} {moeda_destino}\n”)