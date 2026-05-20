
"Pacotes"

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import string
from collections import Counter


"Código base"


texto = """
Produto excelente entrega rápida
Produto ruim Defeito atraso
bom preço entrega demorada,,
muito, satisfeito, produto bom.
"""

wordcloud = WordCloud(width=800, height=400).generate(texto)

plt.imshow(wordcloud)
plt.axis("off")
plt.show()



# ── Passo 1: Pré-processamento ──────────────────────────────────────────────

texto = """
produto excelente entrega rápida
produto ruim defeito atraso
bom preço entrega demorada
muito satisfeito produto bom
"""

# 1. Converter para minúsculas
texto = texto.lower()

# 2. Remover pontuação
texto = texto.translate(str.maketrans("", "", string.punctuation))

# 3. Remover palavras comuns (stopwords em português)
stopwords_pt = {
    "a", "o", "e", "de", "do", "da", "dos", "das", "em", "no", "na",
    "nos", "nas", "um", "uma", "uns", "umas", "com", "por", "para",
    "que", "se", "não", "mais", "como", "mas", "ao", "à", "ou", "foi",
    "ele", "ela", "eu", "tu", "nós", "eles", "elas", "muito", "bem",
    "já", "também", "só", "até", "sobre", "este", "esta", "isso", "aqui","produto","preço"
}

# 4. Separar palavras (tokenização)
tokens = texto.split()

# Filtrar stopwords
tokens_filtrados = [palavra for palavra in tokens if palavra not in stopwords_pt]

# Reunir tokens em texto limpo para a WordCloud
texto_limpo = " ".join(tokens_filtrados)

# ── Geração da WordCloud ────────────────────────────────────────────────────

wordcloud = WordCloud(width=800, height=400).generate(texto_limpo)

plt.imshow(wordcloud)
plt.axis("off")
plt.show()



# ── Passo 2: Frequência de Palavras ────────────────────────────────────────

# Contar frequência de cada palavra
frequencia = Counter(tokens_filtrados)

# Exibir as palavras mais frequentes
print("=== Palavras mais frequentes ===")
for palavra, contagem in frequencia.most_common(10):
    print(f"  '{palavra}': {contagem}x")

# Identificar padrões: palavras positivas x negativas
palavras_positivas = {"excelente", "bom", "satisfeito", "rápida", "ótimo", "perfeito"}
palavras_negativas = {"ruim", "defeito", "atraso", "demorada", "péssimo", "problema"}

print("\n=== Identificação de Padrões ===")
positivas_encontradas = {p: frequencia[p] for p in palavras_positivas if p in frequencia}
negativas_encontradas = {p: frequencia[p] for p in palavras_negativas if p in frequencia}

print(f"  Palavras positivas: {positivas_encontradas}")
print(f"  Palavras negativas: {negativas_encontradas}")

total_pos = sum(positivas_encontradas.values())
total_neg = sum(negativas_encontradas.values())
print(f"\n  Total positivo: {total_pos} | Total negativo: {total_neg}")

if total_pos > total_neg:
    print("  → Tendência POSITIVA no texto")
elif total_neg > total_pos:
    print("  → Tendência NEGATIVA no texto")
else:
    print("  → Texto NEUTRO / equilibrado")




# ── Passo 3: Análise de Sentimento ─────────────────────────────────────────

# Contagens
N_positivo = sum(positivas_encontradas.values())
N_negativo = sum(negativas_encontradas.values())
total_palavras = len(tokens_filtrados)

# Fórmula: Sentimento = (N_positivo - N_negativo) / Total de palavras
sentimento = (N_positivo - N_negativo) / total_palavras

print("\n=== Análise de Sentimento ===")
print(f"  Palavras positivas encontradas : {positivas_encontradas}")
print(f"  Palavras negativas encontradas : {negativas_encontradas}")
print(f"  N_positivo : {N_positivo}")
print(f"  N_negativo : {N_negativo}")
print(f"  Total de palavras              : {total_palavras}")
print(f"  Score de Sentimento            : {sentimento:.4f}")

if sentimento > 0:
    print("  → Sentimento POSITIVO")
elif sentimento < 0:
    print("  → Sentimento NEGATIVO")
else:
    print("  → Sentimento NEUTRO")





# ── Passo 4: Interpretação ─────────────────────────────────────────────────

# Categorias temáticas para identificar o principal problema
temas_produto  = {"ruim", "defeito", "péssimo", "excelente", "satisfeito", "bom"}
temas_entrega  = {"atraso", "demorada", "rápida"}

problemas_produto = {p: frequencia[p] for p in temas_produto & negativas_encontradas.keys()}
problemas_entrega = {p: frequencia[p] for p in temas_entrega & negativas_encontradas.keys()}

total_prob_produto = sum(problemas_produto.values())
total_prob_entrega = sum(problemas_entrega.values())

print("\n=== Interpretação ===")

# Pergunta 1: Sentimento geral
print(f"\n1. Sentimento geral é positivo ou negativo?")
if sentimento > 0:
    print(f"   → POSITIVO (score: {sentimento:.4f})")
elif sentimento < 0:
    print(f"   → NEGATIVO (score: {sentimento:.4f})")
else:
    print(f"   → NEUTRO (score: {sentimento:.4f})")

# Pergunta 2: Qual é o principal problema?
print(f"\n2. Qual é o principal problema?")
if not negativas_encontradas:
    print("   → Nenhum problema identificado no texto.")
else:
    principal_problema = max(negativas_encontradas, key=negativas_encontradas.get)
    print(f"   → '{principal_problema}' é o termo negativo mais frequente ({negativas_encontradas[principal_problema]}x)")

# Pergunta 3: Produto ou entrega?
print(f"\n3. Produto ou entrega?")
print(f"   Problemas com produto : {problemas_produto} (total: {total_prob_produto})")
print(f"   Problemas com entrega : {problemas_entrega} (total: {total_prob_entrega})")

if total_prob_produto > total_prob_entrega:
    print("   → Principal fonte de problemas: PRODUTO")
elif total_prob_entrega > total_prob_produto:
    print("   → Principal fonte de problemas: ENTREGA")
else:
    print("   → Problemas igualmente distribuídos entre produto e entrega")

# ── Geração da WordCloud ────────────────────────────────────────────────────

wordcloud = WordCloud(width=800, height=400).generate(texto_limpo)

plt.imshow(wordcloud)
plt.axis("off")
plt.show()













