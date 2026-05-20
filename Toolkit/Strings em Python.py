"""
05_strings.py
Strings em Python: criação, métodos, f-string, format, split, replace.
"""


# ============================================================
# CRIAR STRINGS
# ============================================================

def formas_de_criar():
    """Strings podem usar aspas simples, duplas ou triplas."""
    s1 = 'simples'
    s2 = "duplas"
    s3 = 'pode ter "aspas duplas" dentro'
    s4 = "pode ter 'aspas simples' dentro"

    # Múltiplas linhas
    s5 = """linha 1
    linha 2
    linha 3"""

    # Raw string (ignora escapes, útil para regex)
    caminho = r'C:\Users\ana'       # barras não são escapes

    # Escape de caracteres
    s6 = 'linha 1\nlinha 2'         # \n quebra linha
    s7 = 'coluna1\tcoluna2'         # \t tab
    s8 = 'aspa: \'simples\''        # escapar aspa


# ============================================================
# F-STRING (FORMATACAO MODERNA)
# ============================================================

def f_strings():
    """
    f-string é a forma mais limpa de formatar strings.
    Python 3.6+.
    """
    nome = 'Ana'
    idade = 30
    saldo = 1234.567

    # Básico
    f'{nome} tem {idade} anos'              # 'Ana tem 30 anos'

    # Com expressões
    f'{nome.upper()} tem {idade + 5} anos daqui 5 anos'

    # Formatação numérica
    f'{saldo:.2f}'                          # '1234.57' (2 casas decimais)
    f'{saldo:,.2f}'                         # '1,234.57' (com separador)
    f'{saldo:10.2f}'                        # '   1234.57' (largura 10)
    f'{saldo:<10.2f}'                       # '1234.57   ' (esquerda)
    f'{saldo:>10.2f}'                       # '   1234.57' (direita)
    f'{saldo:^10.2f}'                       # ' 1234.57  ' (centralizado)
    f'{saldo:010.2f}'                       # '0001234.57' (preenche com 0)

    # Percentual
    taxa = 0.1234
    f'{taxa:.2%}'                           # '12.34%'

    # Notação científica
    f'{1234567:.2e}'                        # '1.23e+06'

    # Inteiro com padding
    f'{5:03d}'                              # '005'
    f'{255:X}'                              # 'FF' (hexadecimal)

    # Data (se for objeto datetime)
    from datetime import datetime
    data = datetime(2025, 8, 15)
    f'{data:%d/%m/%Y}'                      # '15/08/2025'
    f'{data:%A, %d de %B de %Y}'            # 'Friday, 15 de August de 2025'

    # Debug (Python 3.8+): mostra nome e valor
    x = 42
    f'{x=}'                                 # 'x=42'

    # Valor dentro de expressão (nested)
    casas = 3
    f'{saldo:.{casas}f}'                    # '1234.567'


def formato_br():
    """
    Python f-string usa ponto como decimal e vírgula como separador.
    Para formato BR (vírgula decimal), precisa converter.
    """
    valor = 1234567.89

    # Padrão internacional
    s1 = f'{valor:,.2f}'                    # '1,234,567.89'

    # Padrão brasileiro (truque de substituição)
    s2 = f'{valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    # '1.234.567,89'

    return s1, s2


# ============================================================
# METODO FORMAT (MAIS ANTIGO, AINDA FUNCIONAL)
# ============================================================

def metodo_format():
    """.format() era a forma padrão antes do f-string."""
    nome = 'Ana'
    idade = 30

    # Por posição
    '{} tem {} anos'.format(nome, idade)
    '{0} tem {1} anos, {0} é legal'.format(nome, idade)    # reutilizar

    # Por nome
    '{n} tem {i} anos'.format(n=nome, i=idade)

    # Com formatação (igual f-string)
    '{:.2f}'.format(3.14159)                # '3.14'


# ============================================================
# METODOS DE STRING
# ============================================================

def metodos_strings():
    """Métodos mais comuns."""
    s = '  Olá, Mundo  '

    # Remover espaços
    s.strip()                    # 'Olá, Mundo'
    s.lstrip()                   # 'Olá, Mundo  '
    s.rstrip()                   # '  Olá, Mundo'
    s.strip(' ,')                # remove espaços E vírgulas do início/fim

    # Case
    s.upper()                    # '  OLÁ, MUNDO  '
    s.lower()                    # '  olá, mundo  '
    s.title()                    # '  Olá, Mundo  '
    s.capitalize()               # '  olá, mundo  ' (só primeira letra)
    s.swapcase()                 # inverte case

    # Substituir
    s.replace('Mundo', 'Python')
    s.replace('o', 'O', 1)       # só a primeira ocorrência

    # Checar conteúdo
    s.startswith('  Olá')        # True
    s.endswith('  ')             # True
    'Olá' in s                   # True (operador in é mais idiomático)

    s = 'Python123'
    s.isdigit()                  # False (tem letras)
    s.isalpha()                  # False (tem dígitos)
    s.isalnum()                  # True (só letras e dígitos)
    'PYTHON'.isupper()           # True
    'python'.islower()           # True
    '   '.isspace()              # True (só espaços)
    '123.45'.replace('.','').isdigit()  # True

    # Contar
    'banana'.count('a')          # 3

    # Procurar posição
    'banana'.find('na')          # 2 (posição da primeira ocorrência)
    'banana'.find('xyz')         # -1 (não encontrado)
    'banana'.index('na')         # 2 (como find, mas ValueError se não achar)
    'banana'.rfind('na')         # 4 (procura do final para o início)

    # Repetir
    'ab' * 3                     # 'ababab'


# ============================================================
# SPLIT E JOIN
# ============================================================

def split_join():
    """Quebrar e juntar strings."""

    # Split: string para lista
    'a,b,c'.split(',')                    # ['a', 'b', 'c']
    'a  b  c'.split()                     # ['a', 'b', 'c'] (qualquer whitespace)
    'linha1\nlinha2\nlinha3'.splitlines() # ['linha1', 'linha2', 'linha3']
    'a,b,c,d'.split(',', 2)               # ['a', 'b', 'c,d'] (limite 2)
    'a=b=c'.rsplit('=', 1)                # ['a=b', 'c'] (split da direita)

    # Join: lista para string
    ','.join(['a', 'b', 'c'])             # 'a,b,c'
    ' '.join(['Python', 'é', 'legal'])    # 'Python é legal'
    '\n'.join(['linha1', 'linha2'])       # 'linha1\nlinha2'

    # Cuidado: join só aceita lista de STRINGS
    numeros = [1, 2, 3]
    ','.join(str(n) for n in numeros)     # '1,2,3'


# ============================================================
# SLICE DE STRING
# ============================================================

def slice_string():
    """Strings funcionam como listas de caracteres."""
    s = 'Python'

    s[0]                         # 'P'
    s[-1]                        # 'n'
    s[0:3]                       # 'Pyt'
    s[:3]                        # 'Pyt'
    s[3:]                        # 'hon'
    s[::-1]                      # 'nohtyP' (inverter)
    s[::2]                       # 'Pto' (passo 2)
    len(s)                       # 6

    # Strings são IMUTÁVEIS: não dá para s[0] = 'X'
    # Para modificar, crie nova:
    s = 'X' + s[1:]              # 'Xython'


# ============================================================
# VERIFICACOES UTEIS
# ============================================================

def verificacoes():
    """Padrões de validação simples."""
    s = 'ana@exemplo.com'

    # Validar email grosseiramente
    tem_arroba = '@' in s and '.' in s

    # Padronizar para comparação
    normalizado = s.strip().lower()

    # Remover múltiplos espaços
    import re
    limpo = re.sub(r'\s+', ' ', '  texto   com   espaços  ').strip()

    # Só letras e números (remover especiais)
    import re
    so_alnum = re.sub(r'[^a-zA-Z0-9]', '', 'abc-123_xyz!')  # 'abc123xyz'


# ============================================================
# CONVERSOES
# ============================================================

def conversoes():
    """String para outros tipos e vice-versa."""

    # String para número
    int('42')                    # 42
    int('42', 16)                # 66 (hexadecimal)
    float('3.14')                # 3.14
    float('1e3')                 # 1000.0

    # Número para string
    str(42)                      # '42'
    str(3.14)                    # '3.14'

    # String para lista de caracteres
    list('abc')                  # ['a', 'b', 'c']

    # Lista de caracteres para string
    ''.join(['a', 'b', 'c'])     # 'abc'

    # Cuidado com conversões que falham
    try:
        int('abc')               # ValueError
    except ValueError:
        pass


if __name__ == '__main__':
    padrao, br = formato_br()
    print('Internacional:', padrao)
    print('Brasileiro:   ', br)

    nome = 'Ana'
    print(f'\n{nome.upper()} tem saldo de R$ {1234.5:,.2f}'.replace('.', '@').replace(',', '.').replace('@', ','))
