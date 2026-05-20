Cheatsheet Python Básico
Consulta rápida das estruturas mais usadas.
Condicionais
```python
if x > 0:
    ...
elif x == 0:
    ...
else:
    ...

# Inline (expressão ternária)
resultado = 'par' if x % 2 == 0 else 'ímpar'

# Encadear
if 0 < x < 100: ...          # mesmo que (0 < x) and (x < 100)
if x in [1, 2, 3]: ...
if x not in lista: ...
```
Loops
```python
# For com range
for i in range(10):          # 0 até 9
for i in range(1, 11):       # 1 até 10
for i in range(0, 100, 10):  # passo 10
for i in range(10, 0, -1):   # contagem regressiva

# For com índice
for i, item in enumerate(lista, start=1):
    ...

# For com duas listas
for a, b in zip(lista1, lista2):
    ...

# For em dict
for chave, valor in d.items():
    ...

# While
while cond:
    ...

# Quebrar e pular
break       # sai do loop
continue    # pula para próxima iteração
pass        # placeholder, não faz nada
```
Funções
```python
def f(a, b, c=10):             # c tem valor padrão
    return a + b + c

def f(*args, **kwargs):        # args tupla, kwargs dict
    ...

# Chamadas
f(1, 2)                        # posicional
f(a=1, b=2)                    # nomeado
f(*[1, 2, 3])                  # desempacota lista
f(**{'a':1, 'b':2})            # desempacota dict

# Lambda
dobro = lambda x: x * 2
soma = lambda a, b: a + b

# Retorno múltiplo
def f():
    return 1, 2, 3
a, b, c = f()
```
Listas
```python
lista = [1, 2, 3]
lista[0]               # primeiro
lista[-1]              # último
lista[1:3]             # fatia
lista[::-1]            # inverter

# Métodos que modificam
lista.append(4)        # adiciona no fim
lista.insert(0, 0)     # na posição
lista.extend([5, 6])   # vários no fim
lista.remove(3)        # remove primeira ocorrência
lista.pop()            # remove e retorna último
lista.pop(0)           # remove e retorna da posição
lista.sort()           # ordena in place
lista.sort(reverse=True)
lista.sort(key=lambda x: x.algo)
lista.reverse()

# Que retornam valor
len(lista)
sum(lista)
max(lista), min(lista)
lista.count(x)
lista.index(x)
sorted(lista)          # nova lista ordenada
reversed(lista)        # iterador reverso

# Comprehension
[x*2 for x in lista]
[x for x in lista if x > 0]
['+' if x > 0 else '-' for x in lista]

# Desempacotar
a, b, c = [1, 2, 3]
primeiro, *resto = [1, 2, 3, 4]
*inicio, ultimo = [1, 2, 3, 4]

# Copiar
copia = lista.copy()
copia = lista[:]
copia = list(lista)
import copy; copia = copy.deepcopy(lista)   # profunda
```
Dicionários
```python
d = {'a': 1, 'b': 2}

# Acesso
d['a']                 # 1 (KeyError se faltar)
d.get('a')             # 1
d.get('c', 0)          # 0 (padrão)
'a' in d               # True

# Modificar
d['c'] = 3
d.update({'d': 4, 'e': 5})
del d['a']
d.pop('b', None)       # remove com padrão

# Iterar
for k in d: ...
for k in d.keys(): ...
for v in d.values(): ...
for k, v in d.items(): ...

# Comprehension
{k: v*2 for k, v in d.items()}
{k: v for k, v in d.items() if v > 0}

# Combinar
{**d1, **d2}           # Python 3.5+
d1 | d2                # Python 3.9+

# setdefault
d.setdefault('lista', []).append('x')
```
Strings
```python
s = 'Python'

# f-string (preferido)
f'{nome} tem {idade} anos'
f'{valor:,.2f}'        # 1,234.56
f'{taxa:.2%}'          # 12.34%
f'{n:05d}'             # 00042 (5 dígitos com zeros)
f'{x:>10}'             # alinhado à direita em 10 chars
f'{data:%d/%m/%Y}'

# Métodos
s.strip()              # remove espaços das pontas
s.lower() / s.upper()  # case
s.title()              # Capitaliza Cada Palavra
s.replace('a', 'b')
s.split(',')           # string → lista
s.split()              # por whitespace
','.join(['a','b'])    # lista → string
s.startswith('P')
s.endswith('n')
s.count('o')
s.find('x')            # -1 se não achar
'x' in s

# Conversões
int('42'), float('3.14')
str(42)

# Formato BR (truque)
f'{1234.56:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
```
Coleções
```python
from collections import Counter, defaultdict, deque

# Counter: contar
c = Counter(['a', 'b', 'a', 'c'])
c.most_common(2)

# defaultdict: valor padrão automático
d = defaultdict(list)
d['chave'].append('valor')    # cria lista automaticamente

d = defaultdict(int)
d['contador'] += 1            # começa em 0

# deque: fila dupla rápida
d = deque([1, 2, 3])
d.append(4)
d.appendleft(0)
d.pop()
d.popleft()

# Set: únicos
s = {1, 2, 3}
s.add(4)
s.discard(5)
a | b      # união
a & b      # interseção
a - b      # diferença

# Tupla: imutável
t = (1, 2, 3)
a, b, c = t
```
Iteração
```python
# enumerate
for i, x in enumerate(lista, start=1): ...

# zip
for a, b in zip(l1, l2): ...
for a, b, c in zip(l1, l2, l3): ...

# map e filter
list(map(int, ['1','2','3']))                  # conversão em lote
list(filter(lambda x: x > 0, [-1, 0, 1, 2]))   # filtrar

# Generator expression (economiza memória)
sum(x**2 for x in range(1000))
any(x > 10 for x in lista)
all(x > 0 for x in lista)

# Próximo que satisfaz condição
primeiro = next((x for x in lista if x > 10), None)

# itertools comuns
from itertools import chain, combinations, product, accumulate, groupby, islice
chain([1,2], [3,4])            # concatenar iteráveis
combinations([1,2,3], 2)       # combinações
product([1,2], ['a','b'])      # produto cartesiano
accumulate([1,2,3,4])          # soma acumulada
islice(iter_infinito, 10)      # primeiros N de um infinito
```
Try/Except
```python
try:
    ...
except ValueError as e:
    ...
except (TypeError, KeyError):
    ...
except Exception as e:         # qualquer erro (evite usar muito)
    ...
else:
    ...                        # só se não deu erro
finally:
    ...                        # sempre executa

# Lançar erro
raise ValueError('mensagem')

# Padrão de conversão segura
def converter(v):
    try:
        return float(v)
    except (ValueError, TypeError):
        return None
```
Arquivos
```python
# Ler
with open('x.txt', 'r', encoding='utf-8') as f:
    texto = f.read()             # tudo como string
    linhas = f.readlines()       # lista de linhas
    for linha in f:              # linha por linha (lazy)
        ...

# Escrever
with open('x.txt', 'w', encoding='utf-8') as f:
    f.write('conteúdo')
    f.writelines(['linha1\n', 'linha2\n'])

# Anexar
with open('x.txt', 'a', encoding='utf-8') as f:
    f.write('mais conteúdo')

# JSON
import json
with open('x.json') as f:
    dados = json.load(f)
with open('x.json', 'w') as f:
    json.dump(dados, f, indent=2, ensure_ascii=False)
```
Type hints (opcional)
```python
def somar(a: int, b: int) -> int:
    return a + b

def processar(dados: list, taxa: float = 1.0) -> dict:
    ...

from typing import Optional, List, Dict, Tuple
def f(x: Optional[int] = None) -> List[str]:
    ...
```
Dicas rápidas para a prova
Print para debugar. Não tem medo de encher de `print(variavel)` ou `print(f'{var=}')` para entender o que está acontecendo.
Tipo da variável. `type(x)` mostra o tipo. `isinstance(x, int)` checa se é do tipo.
Ver atributos e métodos. `dir(objeto)` lista tudo. `help(objeto.metodo)` mostra docstring.
Truthy/falsy. `if lista:` é mais pythônico que `if len(lista) > 0:`. Valores falsy: `False, 0, '', [], {}, None`.
Não modifique lista enquanto itera. Use list comprehension ou itere sobre cópia: `for x in lista[:]:`.
Evite mutáveis como argumento padrão. `def f(x=[])` tem bug clássico. Use `def f(x=None): x = x or []`.