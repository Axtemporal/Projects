"""
07_erro_excecao.py
Tratamento de erros com try, except, else, finally, raise.
"""


# ============================================================
# TRY/EXCEPT BASICO
# ============================================================

def basico():
    """Estrutura básica de try/except."""

    try:
        resultado = 10 / 0
    except ZeroDivisionError:
        print('Divisão por zero')
        resultado = None

    return resultado


def com_detalhe_do_erro():
    """Pegar a mensagem de erro para log ou análise."""
    try:
        int('abc')
    except ValueError as e:
        print(f'Erro ao converter: {e}')


# ============================================================
# MULTIPLOS EXCEPTS
# ============================================================

def multiplas_excecoes(valor):
    """
    Tratar tipos diferentes de erro de formas diferentes.
    A ordem importa: exceções mais específicas primeiro.
    """
    try:
        num = int(valor)
        resultado = 100 / num
    except ValueError:
        return 'Não é número válido'
    except ZeroDivisionError:
        return 'Não pode ser zero'
    except Exception as e:              # pega qualquer outro erro
        return f'Erro inesperado: {e}'

    return resultado


def agrupar_excecoes(valor):
    """Tratar várias exceções com o mesmo bloco usa tupla."""
    try:
        return int(valor) + 1
    except (ValueError, TypeError) as e:
        return f'Erro de tipo: {e}'


# ============================================================
# ELSE E FINALLY
# ============================================================

def try_completo(caminho):
    """
    try     : código que pode falhar
    except  : o que fazer se der erro
    else    : executa SÓ se o try passar (sem erro)
    finally : SEMPRE executa, com ou sem erro
    """
    f = None
    try:
        f = open(caminho, 'r')
        dados = f.read()
    except FileNotFoundError:
        print('Arquivo não encontrado')
        return None
    except PermissionError:
        print('Sem permissão')
        return None
    else:
        print('Leitura bem sucedida')
        return dados
    finally:
        if f:
            f.close()
        print('Bloco finally sempre executa')


# ============================================================
# RAISE: LANCAR EXCECOES
# ============================================================

def validar_idade(idade):
    """
    raise cria uma exceção nova.
    Use para sinalizar que algo está errado com os dados.
    """
    if not isinstance(idade, int):
        raise TypeError('Idade deve ser inteiro')
    if idade < 0:
        raise ValueError('Idade não pode ser negativa')
    if idade > 150:
        raise ValueError(f'Idade irreal: {idade}')
    return True


def relancar_com_contexto():
    """Capturar, logar e relançar a exceção."""
    try:
        int('abc')
    except ValueError as e:
        print(f'Erro capturado e logado: {e}')
        raise                        # relança a mesma exceção
        # raise RuntimeError('...') from e  # nova exceção encadeada


# ============================================================
# EXCECOES COMUNS
# ============================================================

"""
ValueError          valor com formato inválido (int('abc'))
TypeError           tipo errado ('a' + 1)
KeyError            chave não existe no dict (d['inexistente'])
IndexError          índice fora da lista (lista[999])
AttributeError      atributo não existe (obj.xyz)
FileNotFoundError   arquivo não existe
PermissionError     sem permissão de acesso
ZeroDivisionError   divisão por zero
StopIteration       iterador acabou
IOError             erro de leitura/escrita
ImportError         módulo não encontrado
RuntimeError        erro genérico em tempo de execução
Exception           pai de quase todas as exceções customizáveis
"""


# ============================================================
# EXCECAO CUSTOMIZADA
# ============================================================

class DadoInvalido(Exception):
    """Criar exceção personalizada para casos específicos."""
    pass


class SaldoInsuficiente(Exception):
    """Com atributos extras."""
    def __init__(self, saldo, valor_pedido):
        self.saldo = saldo
        self.valor_pedido = valor_pedido
        super().__init__(f'Saldo {saldo} insuficiente para {valor_pedido}')


def sacar(saldo, valor):
    """Uso de exceção customizada."""
    if valor > saldo:
        raise SaldoInsuficiente(saldo, valor)
    return saldo - valor


# ============================================================
# PADROES COMUNS
# ============================================================

def tentar_converter(valor, tipo=float, padrao=None):
    """
    Padrão muito útil: converter com valor de fallback.
    Evita quebrar processamento por um valor ruim.

    Exemplo:
        df['preco'] = df['preco'].apply(lambda x: tentar_converter(x, float, 0))
    """
    try:
        return tipo(valor)
    except (ValueError, TypeError):
        return padrao


def processar_lista_segura(itens, funcao):
    """
    Processa lista capturando erros individuais.
    Continua mesmo se alguns itens falharem.
    """
    sucessos = []
    erros = []
    for i, item in enumerate(itens):
        try:
            sucessos.append(funcao(item))
        except Exception as e:
            erros.append({'indice': i, 'item': item, 'erro': str(e)})
    return sucessos, erros


def com_retry(funcao, tentativas=3):
    """Retry simples: tenta N vezes antes de desistir."""
    import time
    for i in range(tentativas):
        try:
            return funcao()
        except Exception as e:
            if i == tentativas - 1:
                raise                    # última tentativa, propaga erro
            print(f'Tentativa {i+1} falhou: {e}. Retrying...')
            time.sleep(1)


# ============================================================
# CONTEXT MANAGER (WITH)
# ============================================================

def context_manager():
    """
    'with' garante cleanup automático mesmo se der erro.
    Mais limpo que try/finally para recursos (arquivos, conexões).
    """

    # Abrir arquivo (fecha sozinho no final)
    with open('/tmp/teste.txt', 'w') as f:
        f.write('conteúdo')
    # f.close() é chamado automaticamente aqui, mesmo se der erro

    # Múltiplos context managers
    with open('/tmp/a.txt', 'w') as fa, open('/tmp/b.txt', 'w') as fb:
        fa.write('a')
        fb.write('b')

    # Suprimir exceção com contextlib
    from contextlib import suppress
    with suppress(FileNotFoundError):
        open('inexistente.txt')          # se der erro, é suprimido


# ============================================================
# ASSERT (PARA TESTES E VALIDACAO)
# ============================================================

def com_assert(x):
    """
    assert levanta AssertionError se condição for falsa.
    Use para validar pré-condições ou em testes.
    Em produção com python -O, asserts são ignorados.
    """
    assert x > 0, 'x deve ser positivo'
    assert isinstance(x, (int, float)), 'x deve ser numérico'
    return x ** 0.5


if __name__ == '__main__':
    print(multiplas_excecoes('abc'))       # 'Não é número válido'
    print(multiplas_excecoes('0'))         # 'Não pode ser zero'
    print(multiplas_excecoes('10'))        # 10.0

    print(tentar_converter('1.5', float))  # 1.5
    print(tentar_converter('abc', float, 0))  # 0

    try:
        sacar(100, 200)
    except SaldoInsuficiente as e:
        print(f'Erro: saldo={e.saldo}, pedido={e.valor_pedido}')

    sucessos, erros = processar_lista_segura(
        ['10', '20', 'abc', '30', 'xyz'],
        int
    )
    print(f'Sucessos: {sucessos}')
    print(f'Erros: {erros}')
