"""
csv_pandas.py
Leitura e escrita de CSV com pandas. O caminho mais comum.
"""

import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# Leitura basica
# ============================================================

def ler_csv(caminho, **kwargs):
    """
    Lê CSV padrão internacional (vírgula como separador).

    Parâmetros úteis:
        sep=';'              # separador
        decimal=','          # decimal BR
        thousands='.'        # separador de milhares BR
        encoding='latin-1'   # se utf-8 não funcionar
        header=None          # se não tem cabeçalho
        names=['a','b','c']  # define nomes das colunas
        skiprows=3           # pula linhas iniciais
        usecols=['a','c']    # lê só algumas colunas
        nrows=100            # lê só N linhas
        parse_dates=['data'] # converte colunas em datetime
        dayfirst=True        # datas BR (dd/mm/yyyy)
        na_values=['-', 'n/a', 'NULL']  # o que considerar como NaN
        dtype={'cpf': str}   # força tipo de coluna
    """
    return pd.read_csv(caminho, **kwargs)


def ler_csv_br(caminho, **kwargs):
    """CSV no padrão brasileiro."""
    defaults = {'sep': ';', 'decimal': ',', 'thousands': '.', 'encoding': 'utf-8'}
    defaults.update(kwargs)
    return pd.read_csv(caminho, **defaults)


def ler_csv_com_datas(caminho, colunas_data, **kwargs):
    """
    Lê CSV já convertendo colunas específicas como datas.

    Exemplo:
        df = ler_csv_com_datas('vendas.csv', ['data_venda', 'data_entrega'])
    """
    defaults = {'parse_dates': colunas_data, 'dayfirst': True}
    defaults.update(kwargs)
    return pd.read_csv(caminho, **defaults)


def ler_csv_sem_cabecalho(caminho, nomes_colunas, **kwargs):
    """
    Para arquivos sem cabeçalho onde você define os nomes.

    Exemplo:
        df = ler_csv_sem_cabecalho('dados.csv', ['id', 'nome', 'valor'])
    """
    defaults = {'header': None, 'names': nomes_colunas}
    defaults.update(kwargs)
    return pd.read_csv(caminho, **defaults)


def ler_csv_chunks(caminho, tamanho_chunk=50000, **kwargs):
    """
    Lê CSV em pedaços. Retorna iterador de DataFrames.
    Use quando o arquivo não cabe na memória.

    Exemplo:
        for bloco in ler_csv_chunks('gigante.csv'):
            processar(bloco)
    """
    defaults = {'chunksize': tamanho_chunk}
    defaults.update(kwargs)
    return pd.read_csv(caminho, **defaults)


# ============================================================
# Escrita
# ============================================================

def escrever_csv(df, caminho, **kwargs):
    """
    Escreve CSV padrão (vírgula, sem índice).
    """
    defaults = {'index': False, 'encoding': 'utf-8'}
    defaults.update(kwargs)
    df.to_csv(caminho, **defaults)


def escrever_csv_br(df, caminho, **kwargs):
    """
    CSV no padrão BR que abre direto no Excel brasileiro.
    utf-8-sig preserva acentos quando o Excel abre o arquivo.
    """
    defaults = {
        'sep': ';',
        'decimal': ',',
        'index': False,
        'encoding': 'utf-8-sig'
    }
    defaults.update(kwargs)
    df.to_csv(caminho, **defaults)


def anexar_csv(df, caminho, sep=',', encoding='utf-8'):
    """
    Adiciona DataFrame a um CSV existente. Não escreve cabeçalho se já existir.
    """
    existe = Path(caminho).exists()
    df.to_csv(caminho, mode='a', header=not existe, index=False,
              sep=sep, encoding=encoding)


# ============================================================
# Inspecionar antes de processar
# ============================================================

def ler_primeiras_linhas(caminho, n=5, **kwargs):
    """
    Lê só as primeiras N linhas para inspeção rápida.
    Útil para verificar estrutura antes de processar.
    """
    defaults = {'nrows': n}
    defaults.update(kwargs)
    return pd.read_csv(caminho, **defaults)


def inspecionar_csv(caminho, n=5):
    """
    Mostra infos rápidas do CSV sem carregar tudo.
    """
    amostra = pd.read_csv(caminho, nrows=n)
    print(f'Colunas ({len(amostra.columns)}):')
    for c in amostra.columns:
        print(f'  {c} ({amostra[c].dtype})')
    print(f'\nPrimeiras {n} linhas:')
    print(amostra)


# ============================================================
# Combinacoes comuns
# ============================================================

def ler_varios_csvs(arquivos, **kwargs):
    """
    Lê vários CSVs e concatena vertical. Adiciona coluna de origem.

    Exemplo:
        df = ler_varios_csvs(['jan.csv', 'fev.csv', 'mar.csv'])
    """
    dfs = []
    for arq in arquivos:
        df = pd.read_csv(arq, **kwargs)
        df['arquivo_origem'] = Path(arq).name
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


def csv_para_excel(caminho_csv, caminho_xlsx, aba='Dados', **kwargs_leitura):
    """
    Conversão rápida de CSV para Excel.

    Exemplo:
        csv_para_excel('dados.csv', 'dados.xlsx', sep=';')
    """
    df = pd.read_csv(caminho_csv, **kwargs_leitura)
    df.to_excel(caminho_xlsx, index=False, sheet_name=aba)


if __name__ == '__main__':
    # Teste rápido
    import tempfile
    df = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'y', 'z']})
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
        caminho = f.name
    escrever_csv(df, caminho)
    print(ler_csv(caminho))
