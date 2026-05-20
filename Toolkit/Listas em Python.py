"""
03_listas.py
Listas em Python: criação, acesso, métodos, slicing, comprehension.
"""


# ============================================================
# CRIAR LISTAS
# ============================================================

def formas_de_criar():
    """Várias formas de criar listas."""
    vazia = []
    vazia_alt = list()

    simples = [1, 2, 3, 4, 5]
    mista = [1, 'texto', 3.14, True, None]    # Python aceita tipos mistos

    # A partir de range
    numeros = list(range(1, 11))               # [1, 2, ..., 10]
    pares = list(range(0, 21, 2))              # [0, 2, 4, ..., 20]

    # Repetição
    zeros = [0] * 5                            # [0, 0, 0, 0, 0]
    xyz = ['x'] * 3                            # ['x', 'x', 'x']

    # A partir de string
    letras = list('abc')                       # ['a', 'b', 'c']

    return simples, numeros, zeros


# ============================================================
# ACESSAR ELEMENTOS (INDEXACAO)
# ============================================================

def acessar():
    """Índices começam em 0. Negativos contam do fim."""
    lista = ['a', 'b', 'c', 'd', 'e']

    primeiro = lista[0]        # 'a'
    segundo = lista[1]         # 'b'
    ultimo = lista[-1]         # 'e'
    penultimo = lista[-2]      # 'd'

    # Modificar
    lista[0] = 'A'

    return primeiro, ultimo


# ============================================================
# SLICING (FATIAMENTO)
# ============================================================

def slicing():
    """
    lista[inicio:fim:passo]
    inicio inclusivo, fim exclusivo.
    Se omitir, inicio=0, fim=tamanho, passo=1.
    """
    lista = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    lista[2:5]              # [2, 3, 4]
    lista[:5]               # [0, 1, 2, 3, 4] (primeiros 5)
    lista[5:]               # [5, 6, 7, 8, 9] (do 5 até o fim)
    lista[:]                # cópia da lista inteira
    lista[::2]              # [0, 2, 4, 6, 8] (passo 2)
    lista[::-1]             # [9, 8, ..., 0] (inverter)
    lista[-3:]              # [7, 8, 9] (últimos 3)
    lista[:-3]              # [0, 1, ..., 6] (tudo menos últimos 3)

    # Atribuir em slice
    lista[0:3] = ['a', 'b', 'c']   # substitui os 3 primeiros


# ============================================================
# METODOS QUE MODIFICAM A LISTA
# ============================================================

def metodos_modificadores():
    """Métodos que alteram a lista original (retornam None)."""
    lista = [3, 1, 4, 1, 5]

    lista.append(9)              # adiciona no fim: [3, 1, 4, 1, 5, 9]
    lista.insert(0, 0)           # insere na posição: [0, 3, 1, 4, 1, 5, 9]
    lista.extend([2, 6])         # adiciona vários no fim
    lista.remove(1)              # remove PRIMEIRA ocorrência do valor

    x = lista.pop()              # remove e retorna o último
    y = lista.pop(0)             # remove e retorna da posição 0

    lista.sort()                 # ordena IN PLACE, retorna None
    lista.sort(reverse=True)     # decrescente
    lista.reverse()              # inverte IN PLACE
    lista.clear()                # esvazia a lista

    return lista


# ============================================================
# METODOS QUE NAO MODIFICAM (RETORNAM NOVO)
# ============================================================

def metodos_nao_modificadores():
    """Retornam valor ou nova lista sem alterar a original."""
    lista = [3, 1, 4, 1, 5, 9, 2, 6]

    tamanho = len(lista)          # 8
    conta = lista.count(1)        # 2 (quantas vezes o 1 aparece)
    posicao = lista.index(4)      # 2 (índice da primeira ocorrência)
    maximo = max(lista)           # 9
    minimo = min(lista)           # 1
    soma = sum(lista)             # 31

    # sorted retorna NOVA lista, não modifica
    ordenada = sorted(lista)
    decrescente = sorted(lista, reverse=True)

    # reversed retorna iterador, use list() para virar lista
    invertida = list(reversed(lista))


# ============================================================
# ORDENACAO CUSTOMIZADA
# ============================================================

def ordenacao_customizada():
    """Ordenar por critério personalizado usando key."""

    # Ordenar por comprimento da string
    palavras = ['banana', 'oi', 'elefante', 'cat']
    por_tamanho = sorted(palavras, key=len)

    # Ordenar por campo de dict
    pessoas = [
        {'nome': 'Ana', 'idade': 30},
        {'nome': 'Bruno', 'idade': 25},
        {'nome': 'Clara', 'idade': 35}
    ]
    por_idade = sorted(pessoas, key=lambda p: p['idade'])

    # Ordenar por múltiplos campos (tupla)
    por_idade_e_nome = sorted(pessoas, key=lambda p: (p['idade'], p['nome']))

    # Ordenar por atributo (se fossem objetos)
    # sorted(objetos, key=lambda o: o.atributo)

    return por_tamanho, por_idade


# ============================================================
# LIST COMPREHENSION
# ============================================================

def list_comprehension():
    """
    Forma compacta e pythônica de criar listas.
    [expressão for item in iterável if condição]
    """

    # Substituindo loop tradicional
    quadrados = [x ** 2 for x in range(10)]
    # Equivale a:
    # quadrados = []
    # for x in range(10):
    #     quadrados.append(x ** 2)

    # Com filtro (if no final)
    pares = [x for x in range(20) if x % 2 == 0]

    # Com if-else (antes do for)
    sinais = ['+' if x > 0 else '-' for x in [-2, 1, -3, 4]]

    # Transformar e filtrar
    nomes = ['ana', 'BRUNO', 'Clara']
    padronizados = [n.title() for n in nomes if len(n) > 3]

    # Aninhada (cuidado com legibilidade)
    matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    planificada = [x for linha in matriz for x in linha]   # [1,2,3,4,5,6,7,8,9]

    # Pares (produto cartesiano)
    pares_ordenados = [(i, j) for i in range(3) for j in range(3)]

    return quadrados, pares, planificada


# ============================================================
# OPERACOES COMUNS
# ============================================================

def operacoes_comuns():
    """Padrões que aparecem toda hora."""
    lista = [1, 2, 3, 4, 5]

    # Checar se contém
    tem_tres = 3 in lista                # True

    # Concatenar
    juntas = [1, 2, 3] + [4, 5, 6]       # [1, 2, 3, 4, 5, 6]

    # Desempacotar
    a, b, c = [1, 2, 3]                  # a=1, b=2, c=3
    primeiro, *resto = [1, 2, 3, 4, 5]   # primeiro=1, resto=[2, 3, 4, 5]
    *inicio, ultimo = [1, 2, 3, 4, 5]    # inicio=[1,2,3,4], ultimo=5

    # Achatar lista de listas
    listas = [[1, 2], [3, 4], [5, 6]]
    achatada = [x for sub in listas for x in sub]

    # Cópia (cuidado: cópia rasa)
    copia1 = lista.copy()
    copia2 = lista[:]                    # slice completo também copia
    copia3 = list(lista)

    # Cópia profunda (quando tem listas dentro)
    import copy
    lista_aninhada = [[1, 2], [3, 4]]
    copia_profunda = copy.deepcopy(lista_aninhada)

    # Remover duplicatas mantendo ordem
    original = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    sem_dup = list(dict.fromkeys(original))

    # Remover duplicatas (sem importar ordem)
    sem_dup_set = list(set(original))

    # Achar índices de todas as ocorrências
    lista2 = [1, 2, 3, 2, 1, 2]
    indices_do_2 = [i for i, v in enumerate(lista2) if v == 2]

    return juntas, sem_dup, indices_do_2


# ============================================================
# ARMADILHAS COMUNS
# ============================================================

def armadilhas():
    """Coisas que pegam iniciantes."""

    # Atribuição NÃO é cópia
    a = [1, 2, 3]
    b = a                         # b aponta para a MESMA lista
    b.append(4)
    # Agora a também é [1, 2, 3, 4]

    # Forma correta de copiar
    b = a.copy()
    # ou b = a[:]
    # ou b = list(a)

    # Multiplicação de lista com mutáveis
    matriz_errada = [[0] * 3] * 3    # BUG: todas as linhas são a MESMA lista
    matriz_certa = [[0] * 3 for _ in range(3)]

    # Modificar lista durante iteração é perigoso
    # NÃO FAÇA:
    # for x in lista:
    #     if x < 0:
    #         lista.remove(x)

    # FAÇA (itere sobre cópia ou use comprehension):
    lista = [1, -2, 3, -4]
    lista[:] = [x for x in lista if x > 0]


if __name__ == '__main__':
    quadrados, pares, planificada = list_comprehension()
    print('quadrados:', quadrados)
    print('pares:', pares)
    print('planificada:', planificada)

    juntas, sem_dup, indices = operacoes_comuns()
    print('sem duplicatas:', sem_dup)
    print('índices do 2:', indices)
