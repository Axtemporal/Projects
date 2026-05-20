"""
04_dicionarios.py
Dicionários: criação, acesso, métodos, comprehension, merge.
"""


# ============================================================
# CRIAR DICIONARIOS
# ============================================================

def formas_de_criar():
    """Várias formas de criar dicts."""
    vazio = {}
    vazio_alt = dict()

    # Literal
    pessoa = {'nome': 'Ana', 'idade': 30, 'cidade': 'Rio'}

    # Com argumentos nomeados (chaves devem ser strings)
    pessoa2 = dict(nome='Ana', idade=30, cidade='Rio')

    # A partir de lista de tuplas
    pares = [('a', 1), ('b', 2), ('c', 3)]
    d = dict(pares)

    # A partir de duas listas com zip
    chaves = ['a', 'b', 'c']
    valores = [1, 2, 3]
    d2 = dict(zip(chaves, valores))

    # Chaves com mesmo valor inicial
    template = dict.fromkeys(['a', 'b', 'c'], 0)
    # Vira {'a': 0, 'b': 0, 'c': 0}

    return pessoa, d, template


# ============================================================
# ACESSAR E MODIFICAR
# ============================================================

def acessar_modificar():
    """Acesso e alteração de chaves."""
    d = {'nome': 'Ana', 'idade': 30}

    # Acesso direto (KeyError se não existir)
    d['nome']                    # 'Ana'

    # Acesso seguro com get (None se não existir)
    d.get('telefone')            # None
    d.get('telefone', 'N/A')     # 'N/A' (valor padrão)

    # Verificar se chave existe
    'nome' in d                  # True
    'telefone' in d              # False

    # Adicionar ou modificar
    d['email'] = 'ana@x.com'     # adiciona
    d['idade'] = 31              # modifica

    # Remover
    del d['email']               # KeyError se não existir
    d.pop('telefone', None)      # remove e retorna, com padrão se não existir
    idade = d.pop('idade')       # remove e retorna o valor

    # setdefault: retorna valor se existe, se não existe cria com padrão
    d.setdefault('tags', [])     # se 'tags' não existe, cria como lista vazia
    d.setdefault('tags', []).append('vip')

    # Limpar tudo
    d.clear()

    return d


# ============================================================
# ITERAR SOBRE DICT
# ============================================================

def iterar():
    """Formas de percorrer dicts."""
    d = {'a': 1, 'b': 2, 'c': 3}

    # Por chaves (default)
    for chave in d:
        print(chave, d[chave])

    # Equivalente explícito
    for chave in d.keys():
        print(chave)

    # Por valores
    for valor in d.values():
        print(valor)

    # Por chave e valor juntos (mais comum)
    for chave, valor in d.items():
        print(f'{chave}: {valor}')

    # Ordenar por chave
    for chave in sorted(d):
        print(chave, d[chave])

    # Ordenar por valor
    for chave, valor in sorted(d.items(), key=lambda x: x[1]):
        print(chave, valor)

    # Top N valores maiores
    top2 = sorted(d.items(), key=lambda x: x[1], reverse=True)[:2]


# ============================================================
# DICT COMPREHENSION
# ============================================================

def comprehension():
    """Criar dict de forma compacta."""

    # Quadrados
    quadrados = {x: x ** 2 for x in range(5)}
    # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

    # Inverter chaves e valores
    d = {'a': 1, 'b': 2, 'c': 3}
    invertido = {v: k for k, v in d.items()}

    # Filtrar
    idades = {'Ana': 30, 'Bruno': 17, 'Clara': 25}
    adultos = {nome: idade for nome, idade in idades.items() if idade >= 18}

    # Transformar valores
    precos = {'café': 5, 'açúcar': 3}
    com_imposto = {k: v * 1.1 for k, v in precos.items()}

    # A partir de lista (contagem)
    palavras = ['maçã', 'banana', 'maçã', 'uva', 'banana', 'maçã']
    contagem = {p: palavras.count(p) for p in set(palavras)}

    return quadrados, adultos, com_imposto


# ============================================================
# MERGE (COMBINAR DICTS)
# ============================================================

def merge_dicts():
    """Combinar dicionários."""
    a = {'x': 1, 'y': 2}
    b = {'y': 20, 'z': 30}

    # Python 3.9+ usa operador |
    juntos = a | b                   # {'x': 1, 'y': 20, 'z': 30} (b vence em conflito)

    # Python 3.5+ usa desempacotamento
    juntos2 = {**a, **b}             # mesmo resultado

    # update modifica in place
    a_copia = a.copy()
    a_copia.update(b)                # a_copia agora tem {'x':1, 'y':20, 'z':30}

    return juntos


# ============================================================
# PADROES COMUNS
# ============================================================

def padroes_comuns():
    """Coisas que aparecem toda hora."""

    # Contar ocorrências (alternativa manual ao Counter)
    palavras = ['a', 'b', 'a', 'c', 'b', 'a']
    contagem = {}
    for p in palavras:
        contagem[p] = contagem.get(p, 0) + 1
    # {'a': 3, 'b': 2, 'c': 1}

    # Agrupar valores (alternativa manual ao defaultdict)
    pares = [('fruta', 'maçã'), ('fruta', 'uva'), ('bebida', 'água')]
    grupos = {}
    for categoria, item in pares:
        if categoria not in grupos:
            grupos[categoria] = []
        grupos[categoria].append(item)
    # {'fruta': ['maçã', 'uva'], 'bebida': ['água']}

    # Filtrar dict
    d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    filtrado = {k: v for k, v in d.items() if v > 2}

    # Converter dict em lista de tuplas (para ordenar por exemplo)
    lista_pares = list(d.items())

    # Valor máximo e sua chave
    d = {'A': 10, 'B': 25, 'C': 15}
    chave_maior = max(d, key=d.get)          # 'B'
    valor_maior = d[chave_maior]             # 25

    # Inverter com cuidado (valores duplicados viram conflito)
    original = {'a': 1, 'b': 2, 'c': 1}
    invertido = {v: k for k, v in original.items()}   # cuidado: {1: 'c', 2: 'b'}

    # Dict aninhado
    relatorio = {
        'vendas': {'janeiro': 100, 'fevereiro': 150},
        'custos': {'janeiro': 60, 'fevereiro': 70}
    }
    relatorio['vendas']['janeiro']           # 100

    return contagem, grupos, filtrado, chave_maior


# ============================================================
# ARMADILHAS
# ============================================================

def armadilhas():
    """Pontos de atenção."""

    # Chaves só podem ser imutáveis (str, int, tuple)
    d = {(1, 2): 'ponto'}            # tupla como chave funciona
    # d = {[1, 2]: 'ponto'}          # ERRO: lista não pode ser chave

    # Acesso direto causa KeyError
    d = {'a': 1}
    # d['b']                         # KeyError
    d.get('b')                       # None (seguro)
    d.get('b', 0)                    # 0 (com padrão)

    # Cópia é rasa por padrão
    import copy
    original = {'nomes': ['Ana', 'Bruno']}
    copia = original.copy()
    copia['nomes'].append('Clara')   # MODIFICA o original também!
    # Use deepcopy para dicts aninhados:
    copia_ok = copy.deepcopy(original)


if __name__ == '__main__':
    q, adultos, com_imp = comprehension()
    print('Quadrados:', q)
    print('Adultos:', adultos)
    print('Com imposto:', com_imp)

    contagem, grupos, filt, maior = padroes_comuns()
    print('Contagem:', contagem)
    print('Grupos:', grupos)
    print('Chave maior:', maior)
