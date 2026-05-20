"""
01_io_leitura.py
Funções para ler CSV, Excel e PDF.
"""

import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# Inspecao inicial
# ============================================================

def ver_arquivo_bruto(caminho, n=10):
    """
    Mostra as primeiras n linhas cruas de um arquivo de texto.
    Use quando você não sabe qual é o separador ou encoding.

    Exemplo:
        ver_arquivo_bruto('dados.csv')
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    for enc in encodings:
        try:
            with open(caminho, 'r', encoding=enc) as f:
                print(f'Encoding testado: {enc}')
                for i, linha in enumerate(f):
                    if i >= n:
                        break
                    print(repr(linha))
            return
        except UnicodeDecodeError:
            continue
    print('Nenhum encoding funcionou. Pode ser arquivo binário.')


def visao_geral(df, nome=''):
    """
    Imprime resumo útil do DataFrame. Primeira coisa a fazer depois de carregar.
    """
    print(f'=== {nome} ===' if nome else '===')
    print(f'Shape: {df.shape[0]} linhas x {df.shape[1]} colunas')
    print(f'\nTipos de dados:')
    print(df.dtypes)
    print(f'\nNulos por coluna:')
    nulos = df.isna().sum()
    print(nulos[nulos > 0] if nulos.sum() > 0 else 'Sem nulos')
    print(f'\nDuplicatas: {df.duplicated().sum()}')
    print(f'\nAmostra:')
    print(df.head())


# ============================================================
# CSV
# ============================================================

def ler_csv_br(caminho, **kwargs):
    """
    Lê CSV no padrão brasileiro (separador ponto-e-vírgula, vírgula decimal).

    Exemplo:
        df = ler_csv_br('vendas.csv')
    """
    defaults = {
        'sep': ';',
        'decimal': ',',
        'thousands': '.',
        'encoding': 'utf-8'
    }
    defaults.update(kwargs)
    return pd.read_csv(caminho, **defaults)


def ler_csv_robusto(caminho):
    """
    Tenta combinações de encoding e separador até encontrar uma que funcione.
    Use quando não sabe o formato do arquivo.
    """
    encodings = ['utf-8', 'latin-1', 'cp1252', 'utf-8-sig']
    seps = [',', ';', '\t', '|']

    melhor = None
    melhor_cols = 0

    for enc in encodings:
        for sep in seps:
            try:
                df = pd.read_csv(caminho, encoding=enc, sep=sep, nrows=5)
                if df.shape[1] > melhor_cols:
                    melhor_cols = df.shape[1]
                    melhor = (enc, sep)
            except Exception:
                continue

    if melhor is None:
        raise ValueError('Não consegui ler o arquivo.')

    enc, sep = melhor
    print(f'Usando encoding={enc}, sep={sep!r}')
    return pd.read_csv(caminho, encoding=enc, sep=sep)


def ler_csv_grande(caminho, chunk=100_000, filtro=None, **kwargs):
    """
    Lê CSV gigante em blocos, opcionalmente filtrando cada bloco.

    Exemplo:
        def so_petr(df):
            return df[df['ticker'] == 'PETR4']
        df = ler_csv_grande('historico.csv', filtro=so_petr)
    """
    partes = []
    for bloco in pd.read_csv(caminho, chunksize=chunk, **kwargs):
        if filtro is not None:
            bloco = filtro(bloco)
        partes.append(bloco)
    return pd.concat(partes, ignore_index=True)


# ============================================================
# Excel
# ============================================================

def ler_excel_todas_abas(caminho):
    """
    Lê todas as abas de um Excel num dict {nome_aba: DataFrame}.

    Exemplo:
        abas = ler_excel_todas_abas('relatorio.xlsx')
        print(list(abas.keys()))
        df_vendas = abas['Vendas']
    """
    return pd.read_excel(caminho, sheet_name=None)


def listar_abas(caminho):
    """Retorna lista com nomes das abas de um Excel."""
    return pd.ExcelFile(caminho).sheet_names


def ler_varios_excel(pasta, padrao='*.xlsx', aba=0):
    """
    Lê todos os Excels de uma pasta e empilha num único DataFrame.
    Adiciona coluna 'arquivo_origem' para rastrear.

    Exemplo:
        df = ler_varios_excel('./dados/', '*.xlsx')
    """
    dfs = []
    for arq in sorted(Path(pasta).glob(padrao)):
        df = pd.read_excel(arq, sheet_name=aba)
        df['arquivo_origem'] = arq.name
        dfs.append(df)
    if not dfs:
        raise ValueError(f'Nenhum arquivo encontrado em {pasta} com padrão {padrao}')
    return pd.concat(dfs, ignore_index=True)


def ler_excel_com_cabecalho_estranho(caminho, linhas_pular=0, aba=0):
    """
    Para Excels onde o cabeçalho não está na primeira linha.
    Exemplo comum: relatório com título, em branco, depois tabela.

    Exemplo:
        df = ler_excel_com_cabecalho_estranho('relatorio.xlsx', linhas_pular=3)
    """
    return pd.read_excel(caminho, sheet_name=aba, skiprows=linhas_pular)


# ============================================================
# PDF
# ============================================================

def pdf_extrair_texto(caminho):
    """
    Extrai texto de PDF página por página.
    Retorna lista de strings (uma por página).

    Requer: pip install pdfplumber
    """
    import pdfplumber
    paginas = []
    with pdfplumber.open(caminho) as pdf:
        for p in pdf.pages:
            paginas.append(p.extract_text() or '')
    return paginas


def pdf_texto_completo(caminho):
    """Retorna todo o texto do PDF como uma string única."""
    return '\n\n'.join(pdf_extrair_texto(caminho))


def pdf_extrair_tabelas(caminho, pagina=None):
    """
    Extrai tabelas de PDF usando pdfplumber. Retorna lista de DataFrames.
    pagina=None extrai de todas. pagina=0 só da primeira.

    Funciona melhor em PDFs com tabelas bem estruturadas.

    Requer: pip install pdfplumber
    """
    import pdfplumber
    tabelas = []
    with pdfplumber.open(caminho) as pdf:
        paginas = pdf.pages if pagina is None else [pdf.pages[pagina]]
        for i, p in enumerate(paginas):
            for j, t in enumerate(p.extract_tables()):
                if t and len(t) > 1:
                    df = pd.DataFrame(t[1:], columns=t[0])
                    df.attrs['pagina'] = i
                    df.attrs['tabela_idx'] = j
                    tabelas.append(df)
    return tabelas


def pdf_via_tabula(caminho, paginas='all'):
    """
    Alternativa para tabelas com bordas bem definidas.
    Requer Java instalado na máquina.

    Requer: pip install tabula-py

    Exemplo:
        tabelas = pdf_via_tabula('balanco.pdf', paginas='1-3')
    """
    import tabula
    return tabula.read_pdf(caminho, pages=paginas, multiple_tables=True)


def pdf_buscar_regex(caminho, padrao):
    """
    Procura ocorrências de um regex no texto do PDF inteiro.
    Útil para pegar valores específicos (CNPJ, datas, valores monetários).

    Exemplo:
        valores = pdf_buscar_regex('relatorio.pdf', r'R\\$\\s*[\\d.,]+')
        datas = pdf_buscar_regex('relatorio.pdf', r'\\d{2}/\\d{2}/\\d{4}')
    """
    import re
    texto = pdf_texto_completo(caminho)
    return re.findall(padrao, texto)


def pdf_paginas_com_termo(caminho, termo):
    """
    Retorna lista de números de página onde o termo aparece.
    Útil para navegar PDFs longos.
    """
    paginas = pdf_extrair_texto(caminho)
    return [i for i, texto in enumerate(paginas) if termo.lower() in texto.lower()]
