"""
06_colecoes.py
Estruturas do módulo collections: Counter, defaultdict, deque, namedtuple.
Também: set, frozenset, tuple.
"""

from collections import Counter, defaultdict, deque, namedtuple, OrderedDict


# ============================================================
# COUNTER: CONTAR OCORRENCIAS
# ============================================================

def counter_exemplos():
    """
    Counter conta quantas vezes cada elemento aparece.
    Muito útil para análise de frequência.
    """

    # Contar elementos de uma lista
    palavras = ['a', 'b', 'a', 'c', 'b', 'a', 'a']
    c = Counter(palavras)
    # Counter({'a': 4, 'b': 2, 'c': 1})

    c['a']                       # 4
    c['z']                       # 0 (não gera erro, retorna 0)

    # Mais comuns
    c.most_common(2)             # [('a', 4), ('b', 2)]

    # Total de elementos
    sum(c.values())              # 7

    # Atualizar contagem
    c.update(['a', 'd'])         # 'a' vira 5, 'd' vira 1

    # A partir de string
    Counter('abracadabra')       # Counter({'a': 5, 'b': 2, 'r': 2, ...})

    # Operações aritméticas
    c1 = Counter({'a': 3, 'b': 1})
    c2 = Counter({'a': 1, 'b': 2, 'c': 1})

    c1 + c2                      # Counter({'a': 4, 'b': 3, 'c': 1})
    c1 - c2                      # Counter({'a': 2}) (subtrai e ignora negativos)
    c1 & c2                      # Counter({'a': 1, 'b': 1}) (mínimo)
    c1 | c2                      # Counter({'a': 3, 'b': 2, 'c': 1}) (máximo)

    return c


# ============================================================
# DEFAULTDICT: DICT COM VALOR PADRAO
# ============================================================

def defaultdict_exemplos():
    """
    defaultdict cria automaticamente o valor padrão quando
    você acessa uma chave que não existe.
    """

    # Com int: contar (alternativa ao Counter)
    contagem = defaultdict(int)
    for palavra in ['a', 'b', 'a', 'c']:
        contagem[palavra] += 1       # não precisa checar se chave existe
    # defaultdict(int, {'a': 2, 'b': 1, 'c': 1})

    # Com list: agrupar
    grupos = defaultdict(list)
    pares = [('fruta', 'maçã'), ('fruta', 'uva'), ('bebida', 'café')]
    for categoria, item in pares:
        grupos[categoria].append(item)
    # {'fruta': ['maçã', 'uva'], 'bebida': ['café']}

    # Com set: únicos por grupo
    tags_por_usuario = defaultdict(set)
    eventos = [('ana', 'vip'), ('bruno', 'basico'), ('ana', 'vip'), ('ana', 'novo')]
    for user, tag in eventos:
        tags_por_usuario[user].add(tag)
    # {'ana': {'vip', 'novo'}, 'bruno': {'basico'}}

    # Com lambda: valor padrão customizado
    custom = defaultdict(lambda: 'N/A')
    custom['a'] = 1
    custom['b']                      # 'N/A' (cria automaticamente)

    return contagem, grupos


# ============================================================
# DEQUE: FILA DUPLA EFICIENTE
# ============================================================

def deque_exemplos():
    """
    deque é lista otimizada para adicionar/remover nas pontas.
    Muito mais rápido que list para operações no início.
    """

    # Criar
    d = deque([1, 2, 3])

    # Adicionar
    d.append(4)                  # [1, 2, 3, 4]
    d.appendleft(0)              # [0, 1, 2, 3, 4]

    # Remover
    d.pop()                      # 4, deque fica [0, 1, 2, 3]
    d.popleft()                  # 0, deque fica [1, 2, 3]

    # Rotacionar
    d = deque([1, 2, 3, 4, 5])
    d.rotate(2)                  # deque([4, 5, 1, 2, 3])
    d.rotate(-2)                 # desfaz

    # Com tamanho máximo (descarta os mais antigos)
    recentes = deque(maxlen=3)
    for i in range(5):
        recentes.append(i)
    # deque([2, 3, 4]) - só guarda os 3 últimos

    return d


# ============================================================
# NAMEDTUPLE: TUPLA COM NOMES
# ============================================================

def namedtuple_exemplos():
    """
    namedtuple cria tupla com campos nomeados.
    Mais leve que classe, útil para representar registros.
    """

    # Criar tipo
    Pessoa = namedtuple('Pessoa', ['nome', 'idade', 'cidade'])

    # Criar instância
    ana = Pessoa('Ana', 30, 'Rio')

    # Acessar por nome ou índice
    ana.nome                     # 'Ana'
    ana[0]                       # 'Ana'

    # Imutável como tupla normal
    # ana.nome = 'Bruno'         # ERRO

    # Mas você pode criar cópia modificada
    bruno = ana._replace(nome='Bruno')

    # Converter para dict
    ana._asdict()                # {'nome': 'Ana', 'idade': 30, 'cidade': 'Rio'}

    return ana, bruno


# ============================================================
# SET: CONJUNTO DE ELEMENTOS UNICOS
# ============================================================

def set_exemplos():
    """
    Set é coleção sem duplicatas e sem ordem.
    Operações de conjunto (união, interseção) são rápidas.
    """

    # Criar
    s = {1, 2, 3, 4}
    s_vazio = set()              # {} cria dict, NÃO set!
    s_de_lista = set([1, 2, 2, 3, 3])  # {1, 2, 3} (remove duplicatas)

    # Adicionar e remover
    s.add(5)
    s.discard(10)                # não reclama se não existir
    s.remove(1)                  # KeyError se não existir
    s.pop()                      # remove e retorna elemento arbitrário

    # Checar pertencimento (super rápido, O(1))
    3 in s                       # True

    # Operações de conjunto
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}

    a | b                        # união: {1, 2, 3, 4, 5, 6}
    a & b                        # interseção: {3, 4}
    a - b                        # diferença: {1, 2}
    a ^ b                        # diferença simétrica: {1, 2, 5, 6}

    # Métodos equivalentes
    a.union(b)
    a.intersection(b)
    a.difference(b)
    a.symmetric_difference(b)

    # Comparações
    {1, 2}.issubset({1, 2, 3})   # True
    {1, 2, 3}.issuperset({1, 2}) # True
    {1, 2}.isdisjoint({3, 4})    # True (nada em comum)

    # Set comprehension
    quadrados = {x ** 2 for x in range(-3, 4)}   # {0, 1, 4, 9}

    return a & b


# ============================================================
# FROZENSET: SET IMUTAVEL
# ============================================================

def frozenset_exemplos():
    """
    frozenset é set que não pode ser modificado.
    Vantagem: pode ser usado como chave de dict ou elemento de set.
    """
    fs = frozenset([1, 2, 3])
    # fs.add(4)                  # ERRO: frozenset é imutável

    # Pode ser chave de dict
    d = {frozenset([1, 2]): 'a', frozenset([3, 4]): 'b'}


# ============================================================
# TUPLE: LISTA IMUTAVEL
# ============================================================

def tuple_exemplos():
    """
    Tupla é como lista, mas imutável.
    Mais rápida e pode ser chave de dict.
    """

    # Criar
    t = (1, 2, 3)
    t_vazia = ()
    t_um = (1,)                  # vírgula obrigatória para tupla de 1 elemento
    t_sem_parenteses = 1, 2, 3   # parênteses são opcionais

    # Acesso igual à lista
    t[0]                         # 1
    t[-1]                        # 3
    t[1:]                        # (2, 3)

    # Imutável
    # t[0] = 10                  # ERRO

    # Desempacotamento (muito usado)
    a, b, c = (10, 20, 30)

    # Trocar valores sem variável temp
    x, y = 1, 2
    x, y = y, x                  # agora x=2, y=1

    # Retorno múltiplo de função é tupla
    def divmod_manual(a, b):
        return a // b, a % b

    quoc, resto = divmod_manual(10, 3)

    # Tupla pode ser chave de dict
    coordenadas = {(0, 0): 'origem', (1, 1): 'ponto'}


# ============================================================
# COMPARATIVO: QUANDO USAR CADA UM
# ============================================================

def quando_usar():
    """
    LIST [1,2,3]       Ordenada, mutável, permite duplicatas
    TUPLE (1,2,3)      Ordenada, IMUTÁVEL, permite duplicatas
    SET {1,2,3}        Não ordenada, mutável, SEM duplicatas
    FROZENSET          Como set mas imutável (pode ser chave de dict)
    DICT {'a': 1}      Chave-valor, mutável, chaves únicas
    COUNTER            Dict especializado para contagem
    DEFAULTDICT        Dict com valor padrão automático
    DEQUE              Lista otimizada para pontas (fila/pilha)
    NAMEDTUPLE         Tupla com campos nomeados (imutável, leve)
    """
    pass


if __name__ == '__main__':
    # Demonstração rápida
    palavras = 'a b c a b a'.split()
    print('Counter:', Counter(palavras))
    print('Counter mais comuns:', Counter(palavras).most_common(2))

    grupos = defaultdict(list)
    for cat, item in [('fruta', 'maçã'), ('fruta', 'uva'), ('bebida', 'café')]:
        grupos[cat].append(item)
    print('Grupos:', dict(grupos))

    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}
    print('União:', a | b)
    print('Interseção:', a & b)
