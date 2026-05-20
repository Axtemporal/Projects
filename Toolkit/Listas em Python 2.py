"""
08_iteradores.py
enumerate, zip, map, filter, generators e ferramentas do itertools.
Essenciais para processar sequências de forma eficiente.
"""

import itertools


# ============================================================
# ENUMERATE: INDICE + VALOR
# ============================================================

def enumerate_exemplos():
    """
    enumerate adiciona contador ao iterar.
    Evita o padrão feio 'for i in range(len(lista))'.
    """
    cores = ['vermelho', 'verde', 'azul']

    # Com índice começando em 0
    for i, cor in enumerate(cores):
        print(f'{i}: {cor}')

    # Começar de outro número
    for i, cor in enumerate(cores, start=1):
        print(f'{i}. {cor}')

    # Criar dict numerado
    numerado = dict(enumerate(cores))      # {0: 'vermelho', 1: 'verde', 2: 'azul'}

    # Inverter: valor para índice
    indice = {cor: i for i, cor in enumerate(cores)}


# ============================================================
# ZIP: COMBINAR ITERAVEIS
# ============================================================

def zip_exemplos():
    """
    zip combina elementos de várias sequências em tuplas.
    Para na sequência mais curta.
    """
    nomes = ['Ana', 'Bruno', 'Clara']
    idades = [30, 25, 35]
    cidades = ['Rio', 'SP', 'BH']

    # Combinar duas listas
    for nome, idade in zip(nomes, idades):
        print(f'{nome}: {idade}')

    # Combinar três ou mais
    for nome, idade, cidade in zip(nomes, idades, cidades):
        print(f'{nome}, {idade}, {cidade}')

    # Para em 'Bruno' porque a segunda lista é menor
    for nome, idade in zip(['Ana', 'Bruno', 'Clara'], [30, 25]):
        print(nome, idade)

    # Criar dict a partir de duas listas
    d = dict(zip(nomes, idades))           # {'Ana': 30, 'Bruno': 25, 'Clara': 35}

    # "Unzip" (separar de volta)
    pares = [('a', 1), ('b', 2), ('c', 3)]
    letras, numeros = zip(*pares)          # ('a','b','c'), (1,2,3)

    # Transpor matriz
    matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    transposta = list(zip(*matriz))        # [(1,4,7), (2,5,8), (3,6,9)]


def zip_longest_exemplo():
    """
    zip_longest vai até o iterável mais LONGO.
    Preenche os faltantes com um valor padrão.
    """
    a = [1, 2, 3, 4, 5]
    b = ['a', 'b', 'c']
    list(itertools.zip_longest(a, b, fillvalue='-'))
    # [(1,'a'), (2,'b'), (3,'c'), (4,'-'), (5,'-')]


# ============================================================
# MAP: APLICAR FUNCAO A CADA ELEMENTO
# ============================================================

def map_exemplos():
    """
    map aplica função a cada item e retorna iterador.
    Geralmente list comprehension é mais legível.
    """
    numeros = [1, 2, 3, 4, 5]

    # Aplicar função
    dobrados = list(map(lambda x: x * 2, numeros))     # [2, 4, 6, 8, 10]

    # Equivalente com list comprehension (mais comum)
    dobrados_lc = [x * 2 for x in numeros]

    # Múltiplas sequências (a função recebe múltiplos args)
    a = [1, 2, 3]
    b = [10, 20, 30]
    somas = list(map(lambda x, y: x + y, a, b))        # [11, 22, 33]

    # Converter tipos em lote
    strings = ['1', '2', '3', '4']
    inteiros = list(map(int, strings))                 # [1, 2, 3, 4]


# ============================================================
# FILTER: FILTRAR POR CONDICAO
# ============================================================

def filter_exemplos():
    """
    filter mantém apenas elementos onde a função retorna True.
    List comprehension com if costuma ser mais legível.
    """
    numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Filtrar pares
    pares = list(filter(lambda x: x % 2 == 0, numeros))    # [2, 4, 6, 8, 10]

    # Equivalente com list comprehension
    pares_lc = [x for x in numeros if x % 2 == 0]

    # Remover valores falsy (None, 0, '', []) com filter(None, ...)
    mistura = [1, None, 2, '', 3, 0, 4, [], 5]
    so_truthy = list(filter(None, mistura))            # [1, 2, 3, 4, 5]


# ============================================================
# GENERATORS: ITERADORES PREGUICOSOS
# ============================================================

def generator_funcao():
    """
    Função com yield vira um gerador.
    Produz valores sob demanda, sem guardar tudo na memória.
    Útil para sequências grandes ou infinitas.
    """

    def contador_ate(n):
        """Gerador que produz 0, 1, 2, ..., n-1."""
        i = 0
        while i < n:
            yield i
            i += 1

    # Usar
    for x in contador_ate(5):
        print(x)

    # Converter para lista (gasta tudo de uma vez)
    lista = list(contador_ate(10))


def generator_infinito():
    """Gerador pode ser infinito, contanto que você pare de consumir."""

    def pares_infinitos():
        n = 0
        while True:
            yield n
            n += 2

    # Pegar só os primeiros 5
    gen = pares_infinitos()
    primeiros_5 = [next(gen) for _ in range(5)]        # [0, 2, 4, 6, 8]


def generator_expression():
    """
    Gerador em forma compacta, parece list comprehension com () em vez de [].
    Economiza memória quando você vai iterar uma vez só.
    """
    # List comprehension: cria lista inteira na memória
    quadrados_lista = [x ** 2 for x in range(1000000)]

    # Generator expression: calcula um de cada vez
    quadrados_gen = (x ** 2 for x in range(1000000))

    # Ideal para funções que iteram (sum, max, any, all)
    soma = sum(x ** 2 for x in range(100))             # sem parênteses extras aqui
    tem_negativo = any(x < 0 for x in [1, 2, -3, 4])   # para assim que acha um

    # Pegar só os N primeiros de um gerador
    primeiros_10 = list(itertools.islice((x ** 2 for x in range(1000)), 10))


# ============================================================
# FUNCOES DE AGREGACAO
# ============================================================

def agregacao_builtin():
    """Funções built-in que agregam iteráveis."""
    numeros = [3, 1, 4, 1, 5, 9, 2, 6]

    sum(numeros)                    # 31
    min(numeros)                    # 1
    max(numeros)                    # 9
    len(numeros)                    # 8

    # any: True se pelo menos um elemento for verdadeiro
    any([False, False, True])       # True
    any(x > 10 for x in numeros)    # False

    # all: True se TODOS forem verdadeiros
    all([True, True, True])         # True
    all(x > 0 for x in numeros)     # True

    # Com key (para dicts ou tuplas)
    pessoas = [{'nome': 'Ana', 'idade': 30}, {'nome': 'Bruno', 'idade': 25}]
    mais_velho = max(pessoas, key=lambda p: p['idade'])


# ============================================================
# ITERTOOLS: UTILIDADES DE ITERACAO
# ============================================================

def itertools_exemplos():
    """Funções úteis do módulo itertools."""

    # chain: concatenar iteráveis
    list(itertools.chain([1, 2], [3, 4], [5, 6]))      # [1, 2, 3, 4, 5, 6]

    # count: contador infinito
    list(itertools.islice(itertools.count(10, 2), 5))  # [10, 12, 14, 16, 18]

    # cycle: repetir iterável infinitamente
    list(itertools.islice(itertools.cycle('AB'), 6))   # ['A','B','A','B','A','B']

    # repeat: repetir valor N vezes
    list(itertools.repeat('x', 4))                      # ['x', 'x', 'x', 'x']

    # combinations: todas as combinações de tamanho K
    list(itertools.combinations([1, 2, 3, 4], 2))
    # [(1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]

    # permutations: todas as ordenações
    list(itertools.permutations([1, 2, 3], 2))
    # [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2)]

    # product: produto cartesiano
    list(itertools.product([1, 2], ['a', 'b']))
    # [(1,'a'), (1,'b'), (2,'a'), (2,'b')]

    # groupby: agrupar elementos consecutivos iguais
    # ATENCAO: só agrupa se consecutivos. Ordene antes para agrupar tudo.
    dados = [('A', 1), ('A', 2), ('B', 3), ('A', 4), ('B', 5)]
    dados_ordenados = sorted(dados, key=lambda x: x[0])
    for chave, grupo in itertools.groupby(dados_ordenados, key=lambda x: x[0]):
        print(chave, list(grupo))

    # accumulate: soma acumulada
    list(itertools.accumulate([1, 2, 3, 4]))            # [1, 3, 6, 10]
    # Com função customizada
    list(itertools.accumulate([1, 2, 3, 4], lambda a, b: a * b))   # produto acumulado

    # takewhile: pega enquanto condição for verdadeira
    list(itertools.takewhile(lambda x: x < 5, [1, 3, 5, 7, 1]))    # [1, 3]

    # dropwhile: pula enquanto condição for verdadeira
    list(itertools.dropwhile(lambda x: x < 5, [1, 3, 5, 7, 1]))    # [5, 7, 1]


# ============================================================
# NEXT E ITER
# ============================================================

def iter_next_exemplos():
    """
    iter() cria iterador a partir de qualquer iterável.
    next() pega o próximo valor.
    """
    lista = [10, 20, 30]
    it = iter(lista)

    next(it)                        # 10
    next(it)                        # 20
    next(it)                        # 30
    # next(it)                      # StopIteration

    # next com valor padrão (não quebra se acabar)
    next(it, 'fim')                 # 'fim'

    # Achar primeiro item que satisfaz condição
    numeros = [1, 3, 5, 8, 10, 12]
    primeiro_par = next((x for x in numeros if x % 2 == 0), None)    # 8


if __name__ == '__main__':
    # Demos
    nomes = ['Ana', 'Bruno', 'Clara']
    idades = [30, 25, 35]

    print('Enumerate:')
    for i, nome in enumerate(nomes, 1):
        print(f'  {i}. {nome}')

    print('\nZip:')
    for n, i in zip(nomes, idades):
        print(f'  {n}: {i}')

    print('\nCombinations:')
    print(list(itertools.combinations([1, 2, 3, 4], 2)))

    print('\nAccumulate (soma):')
    print(list(itertools.accumulate([1, 2, 3, 4, 5])))
