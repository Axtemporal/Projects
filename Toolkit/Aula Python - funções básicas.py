"""
01_controle_fluxo.py
if, elif, else, while, for, break, continue, pass, match.
"""


# ============================================================
# IF, ELIF, ELSE
# ============================================================

def exemplos_if():
    """Condicionais básicas."""
    x = 10

    # Forma completa
    if x > 20:
        resultado = 'alto'
    elif x > 5:
        resultado = 'médio'
    else:
        resultado = 'baixo'

    # Expressão ternária (if inline)
    resultado = 'par' if x % 2 == 0 else 'ímpar'

    # Múltiplas condições
    if x > 0 and x < 100:
        pass
    if x < 0 or x > 100:
        pass
    if not x:                  # x é falsy (0, '', None, [], {})
        pass

    # Checar pertencimento
    if x in [1, 2, 3]:
        pass
    if x in range(1, 11):      # 1 até 10
        pass

    # Encadear comparações (forma pythônica)
    if 0 < x < 100:            # equivalente a 0 < x and x < 100
        pass

    return resultado


def valores_falsy():
    """
    O que é considerado False num if.
    Útil para checagens rápidas.
    """
    exemplos = [False, 0, 0.0, '', [], {}, set(), None]
    for v in exemplos:
        print(f'{v!r:15} -> {bool(v)}')


# ============================================================
# FOR LOOP
# ============================================================

def exemplos_for():
    """For loops, a forma mais comum de iterar em Python."""

    # Sobre lista
    for item in [10, 20, 30]:
        print(item)

    # Sobre range (sequência de números)
    for i in range(5):              # 0, 1, 2, 3, 4
        pass
    for i in range(1, 11):          # 1 até 10
        pass
    for i in range(0, 100, 10):     # 0, 10, 20, ... 90
        pass
    for i in range(10, 0, -1):      # 10, 9, 8, ... 1 (contagem regressiva)
        pass

    # Com índice usando enumerate
    cores = ['vermelho', 'verde', 'azul']
    for i, cor in enumerate(cores):
        print(f'{i}: {cor}')

    # Enumerate começando de outro número
    for i, cor in enumerate(cores, start=1):
        print(f'{i}: {cor}')

    # Sobre duas listas juntas usando zip
    nomes = ['Ana', 'Bruno']
    idades = [30, 25]
    for nome, idade in zip(nomes, idades):
        print(f'{nome} tem {idade} anos')

    # Sobre dicionário
    pessoa = {'nome': 'Ana', 'idade': 30}
    for chave in pessoa:                    # chaves
        print(chave)
    for valor in pessoa.values():           # valores
        print(valor)
    for chave, valor in pessoa.items():     # chave e valor juntos
        print(f'{chave}: {valor}')

    # Sobre string (caractere por caractere)
    for letra in 'Python':
        print(letra)


# ============================================================
# WHILE LOOP
# ============================================================

def exemplos_while():
    """
    While executa enquanto a condição for verdadeira.
    Use quando você não sabe de antemão quantas iterações precisa.
    """

    # While básico
    contador = 0
    while contador < 5:
        print(contador)
        contador += 1

    # Loop infinito com condição de saída no meio
    while True:
        # simulando input do usuário
        resposta = 'sair'
        if resposta == 'sair':
            break
        # processar algo

    # While com else (raramente usado)
    # else executa quando o while termina naturalmente (sem break)
    n = 3
    while n > 0:
        n -= 1
    else:
        print('Loop terminou sem break')


# ============================================================
# BREAK, CONTINUE, PASS
# ============================================================

def exemplos_break_continue():
    """
    break: sai do loop imediatamente.
    continue: pula para a próxima iteração.
    pass: não faz nada (placeholder).
    """

    # break: parar quando encontrar
    for i in range(100):
        if i == 5:
            break
        print(i)          # imprime 0 até 4

    # continue: pular algumas iterações
    for i in range(10):
        if i % 2 == 0:    # pular pares
            continue
        print(i)          # imprime 1, 3, 5, 7, 9

    # pass: placeholder para código ainda não escrito
    def funcao_a_implementar():
        pass

    for i in range(3):
        pass              # loop válido que não faz nada


# ============================================================
# LOOPS ANINHADOS
# ============================================================

def exemplos_loops_aninhados():
    """Loops dentro de loops."""

    # Tabuada 2x2
    for i in range(1, 4):
        for j in range(1, 4):
            print(f'{i} x {j} = {i*j}')

    # Matriz
    matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    for linha in matriz:
        for valor in linha:
            print(valor, end=' ')
        print()           # quebra de linha a cada linha da matriz

    # break em loop aninhado só sai do interno
    for i in range(3):
        for j in range(3):
            if j == 2:
                break
            print(f'{i},{j}')


# ============================================================
# MATCH (Python 3.10+)
# ============================================================

def exemplos_match(valor):
    """
    Match/case é o switch/case do Python (versão 3.10 em diante).
    Se sua prova rodar Python 3.9 ou anterior, use if/elif.
    """
    match valor:
        case 1:
            return 'um'
        case 2 | 3:                 # valor 2 OU 3
            return 'dois ou três'
        case int() if valor > 10:   # com condição
            return 'maior que dez'
        case [a, b]:                # match por padrão (lista de 2)
            return f'lista de dois: {a}, {b}'
        case _:                     # default
            return 'outro'


if __name__ == '__main__':
    print('=== Valores falsy ===')
    valores_falsy()

    print('\n=== If expressão ===')
    print(exemplos_if())

    print('\n=== Match ===')
    print(exemplos_match(15))
