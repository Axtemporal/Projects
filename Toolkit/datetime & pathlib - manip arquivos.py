"""
buscar_arquivos.py
Buscar arquivos por padrão, extensão, data, tamanho.
"""

from pathlib import Path
from datetime import datetime, timedelta
import fnmatch


# ============================================================
# Busca com glob
# ============================================================

def buscar_por_extensao(pasta, extensao):
    """
    Busca arquivos com uma extensão específica (não recursivo).

    Exemplo:
        buscar_por_extensao('./dados', '.csv')
    """
    if not extensao.startswith('.'):
        extensao = '.' + extensao
    return sorted([p for p in Path(pasta).iterdir()
                   if p.is_file() and p.suffix == extensao])


def buscar_por_extensao_recursivo(pasta, extensao):
    """
    Busca arquivos com extensão em pasta e subpastas.

    Exemplo:
        buscar_por_extensao_recursivo('./projeto', '.py')
    """
    if not extensao.startswith('.'):
        extensao = '.' + extensao
    return sorted(Path(pasta).rglob(f'*{extensao}'))


def buscar_por_padrao(pasta, padrao, recursivo=False):
    """
    Busca por padrão glob (aceita curingas * e ?).

    Exemplos de padrão:
        'relatorio_*.xlsx'     # começa com relatorio_
        '2025_*.csv'           # começa com 2025_
        '*[0-9].txt'           # termina com dígito antes do .txt
        '?????.csv'            # exatamente 5 caracteres no nome

    Exemplo:
        buscar_por_padrao('./dados', 'rel_2025*.xlsx', recursivo=True)
    """
    metodo = Path(pasta).rglob if recursivo else Path(pasta).glob
    return sorted(metodo(padrao))


def buscar_varias_extensoes(pasta, extensoes, recursivo=True):
    """
    Busca arquivos de várias extensões de uma vez.

    Exemplo:
        buscar_varias_extensoes('./', ['.xlsx', '.xls', '.csv'])
    """
    resultados = []
    metodo = Path(pasta).rglob if recursivo else Path(pasta).glob
    for ext in extensoes:
        ext = ext if ext.startswith('.') else '.' + ext
        resultados.extend(metodo(f'*{ext}'))
    return sorted(set(resultados))


# ============================================================
# Filtros por metadados
# ============================================================

def filtrar_por_tamanho(arquivos, min_bytes=None, max_bytes=None):
    """
    Filtra lista de Paths por tamanho.

    Exemplo:
        grandes = filtrar_por_tamanho(arquivos, min_bytes=1024*1024)  # > 1MB
    """
    resultado = []
    for p in arquivos:
        if not p.is_file():
            continue
        tam = p.stat().st_size
        if min_bytes is not None and tam < min_bytes:
            continue
        if max_bytes is not None and tam > max_bytes:
            continue
        resultado.append(p)
    return resultado


def filtrar_por_data_modificacao(arquivos, apos=None, antes=None):
    """
    Filtra por data de modificação.
    apos, antes podem ser datetime ou string 'yyyy-mm-dd'.

    Exemplo:
        recentes = filtrar_por_data_modificacao(arquivos, apos='2025-01-01')
    """
    def parse(d):
        if d is None:
            return None
        if isinstance(d, str):
            return datetime.fromisoformat(d)
        return d

    apos_dt = parse(apos)
    antes_dt = parse(antes)

    resultado = []
    for p in arquivos:
        if not p.is_file():
            continue
        mod = datetime.fromtimestamp(p.stat().st_mtime)
        if apos_dt and mod < apos_dt:
            continue
        if antes_dt and mod > antes_dt:
            continue
        resultado.append(p)
    return resultado


def arquivos_modificados_ultimas_horas(pasta, horas=24, padrao='*'):
    """
    Atalho para pegar arquivos modificados recentemente.
    """
    limite = datetime.now() - timedelta(hours=horas)
    arquivos = Path(pasta).rglob(padrao)
    return [p for p in arquivos if p.is_file() and
            datetime.fromtimestamp(p.stat().st_mtime) > limite]


# ============================================================
# Ordenacao
# ============================================================

def ordenar_por_data(arquivos, mais_novo_primeiro=True):
    """Ordena lista de Paths pela data de modificação."""
    return sorted(arquivos,
                  key=lambda p: p.stat().st_mtime,
                  reverse=mais_novo_primeiro)


def ordenar_por_tamanho(arquivos, maior_primeiro=True):
    """Ordena por tamanho."""
    return sorted(arquivos,
                  key=lambda p: p.stat().st_size,
                  reverse=maior_primeiro)


# ============================================================
# Buscar por conteudo
# ============================================================

def buscar_nos_nomes(pasta, termo, recursivo=True, case_sensitive=False):
    """
    Busca arquivos cujo NOME contém um termo.

    Exemplo:
        buscar_nos_nomes('./', 'relatorio')
    """
    metodo = Path(pasta).rglob if recursivo else Path(pasta).glob
    termo_ajustado = termo if case_sensitive else termo.lower()
    resultado = []
    for p in metodo('*'):
        if not p.is_file():
            continue
        nome = p.name if case_sensitive else p.name.lower()
        if termo_ajustado in nome:
            resultado.append(p)
    return sorted(resultado)


def buscar_nos_conteudos(pasta, termo, extensao='.txt',
                          recursivo=True, encoding='utf-8'):
    """
    Busca arquivos cujo CONTEÚDO contém um termo.
    Só vale para arquivos de texto.

    Exemplo:
        buscar_nos_conteudos('./', 'PETR4', extensao='.csv')
    """
    encontrados = []
    arquivos = buscar_por_extensao_recursivo(pasta, extensao) if recursivo \
               else buscar_por_extensao(pasta, extensao)

    for p in arquivos:
        try:
            with open(p, 'r', encoding=encoding) as f:
                if termo in f.read():
                    encontrados.append(p)
        except (UnicodeDecodeError, PermissionError):
            continue
    return encontrados


# ============================================================
# Padroes uteis
# ============================================================

def bateu_padrao(nome_arquivo, padrao):
    """
    Verifica se nome de arquivo bate com um padrão glob.

    Exemplo:
        bateu_padrao('relatorio_2025.csv', 'relatorio_*.csv')  # True
    """
    return fnmatch.fnmatch(nome_arquivo, padrao)


if __name__ == '__main__':
    # Teste rápido
    arquivos = buscar_por_extensao('.', '.py')
    print(f'Encontrados {len(arquivos)} arquivos .py')
