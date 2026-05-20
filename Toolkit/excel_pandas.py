"""
excel_pandas.py
Ler e escrever arquivos .xlsx com pandas.
Para controle fino de formatação, use excel_openpyxl.py.
"""

import pandas as pd
from pathlib import Path


# ============================================================
# Leitura
# ============================================================

def ler_excel(caminho, aba=0, **kwargs):
    """
    Lê uma aba do Excel. aba pode ser nome ou índice.

    Parâmetros úteis:
        sheet_name=0              # índice ou nome da aba
        sheet_name=None           # lê TODAS as abas (retorna dict)
        sheet_name=['Aba1','Aba2'] # lista de abas
        header=0                  # linha do cabeçalho
        header=[0,1]              # cabeçalho multi-nível
        skiprows=3                # pula linhas iniciais
        nrows=100                 # lê só N linhas
        usecols='A:C'             # lê só algumas colunas por letra
        usecols=[0,1,3]           # por índice
    """
    return pd.read_excel(caminho, sheet_name=aba, **kwargs)


def listar_abas(caminho):
    """
    Lista nomes das abas de um Excel sem carregar dados.
    """
    return pd.ExcelFile(caminho).sheet_names


def ler_todas_abas(caminho, **kwargs):
    """
    Lê todas as abas num dict {nome_aba: DataFrame}.

    Exemplo:
        abas = ler_todas_abas('relatorio.xlsx')
        print(list(abas.keys()))
        df = abas['Vendas']
    """
    return pd.read_excel(caminho, sheet_name=None, **kwargs)


def ler_aba_especifica(caminho, nome_aba, **kwargs):
    """Lê uma aba específica pelo nome."""
    return pd.read_excel(caminho, sheet_name=nome_aba, **kwargs)


def ler_excel_com_cabecalho_deslocado(caminho, linhas_pular, aba=0):
    """
    Para relatórios onde a tabela não começa na primeira linha.
    Muito comum em reports de ERP.

    Exemplo:
        # Relatório com título, linha em branco, depois tabela
        df = ler_excel_com_cabecalho_deslocado('rel.xlsx', 3)
    """
    return pd.read_excel(caminho, sheet_name=aba, skiprows=linhas_pular)


def ler_excel_range(caminho, range_excel, aba=0):
    """
    Lê um range específico do Excel. Útil para pegar só parte da aba.

    Exemplo:
        df = ler_excel_range('x.xlsx', 'B3:F50')
    """
    # Separa inicio e fim
    inicio, fim = range_excel.split(':')
    col_ini = ''.join(c for c in inicio if c.isalpha())
    col_fim = ''.join(c for c in fim if c.isalpha())
    linha_ini = int(''.join(c for c in inicio if c.isdigit()))
    linha_fim = int(''.join(c for c in fim if c.isdigit()))

    return pd.read_excel(
        caminho, sheet_name=aba,
        usecols=f'{col_ini}:{col_fim}',
        skiprows=linha_ini - 1,
        nrows=linha_fim - linha_ini + 1,
        header=0
    )


# ============================================================
# Escrita simples
# ============================================================

def escrever_excel(df, caminho, aba='Dados', **kwargs):
    """
    Escreve DataFrame em Excel. Sobrescreve se existir.
    """
    defaults = {'index': False}
    defaults.update(kwargs)
    df.to_excel(caminho, sheet_name=aba, **defaults)


def escrever_multiplas_abas(caminho, dfs_dict, **kwargs):
    """
    Escreve várias abas num único Excel.
    dfs_dict é um dict {nome_aba: DataFrame}.

    Exemplo:
        escrever_multiplas_abas('resultado.xlsx', {
            'Resumo': df_resumo,
            'Dados Brutos': df_bruto,
            'Análise': df_analise
        })
    """
    defaults = {'index': False}
    defaults.update(kwargs)
    with pd.ExcelWriter(caminho, engine='openpyxl') as writer:
        for nome_aba, df in dfs_dict.items():
            df.to_excel(writer, sheet_name=nome_aba, **defaults)


def adicionar_aba_sem_apagar(caminho, df, nome_aba):
    """
    Adiciona uma aba nova num Excel existente, sem apagar as outras.
    Exige openpyxl instalado.

    Exemplo:
        adicionar_aba_sem_apagar('relatorio.xlsx', df_novo, 'Análise Extra')
    """
    with pd.ExcelWriter(caminho, engine='openpyxl', mode='a',
                        if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=nome_aba, index=False)


# ============================================================
# Escrita com formatacao basica
# ============================================================

def escrever_excel_formatado(df, caminho, aba='Dados',
                              largura_colunas=None,
                              congelar_painel='A2'):
    """
    Escreve Excel com largura de coluna e painel congelado.
    Já um bom default para entregar relatório.

    Exemplo:
        escrever_excel_formatado(df, 'saida.xlsx',
                                  largura_colunas={'A': 20, 'B': 15, 'C': 12})
    """
    with pd.ExcelWriter(caminho, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=aba, index=False)
        ws = writer.sheets[aba]

        # Congelar painel (mantém cabeçalho fixo ao rolar)
        if congelar_painel:
            ws.freeze_panes = congelar_painel

        # Auto filtro
        ws.auto_filter.ref = ws.dimensions

        # Larguras de coluna
        if largura_colunas:
            for col, largura in largura_colunas.items():
                ws.column_dimensions[col].width = largura
        else:
            # Auto ajuste simples
            for col_idx, col_name in enumerate(df.columns, 1):
                col_letra = chr(64 + col_idx) if col_idx <= 26 else 'AA'
                largura = max(len(str(col_name)),
                              df[col_name].astype(str).str.len().max() if len(df) else 10)
                ws.column_dimensions[col_letra].width = min(largura + 2, 40)


# ============================================================
# Utilitarios
# ============================================================

def excel_para_csv(caminho_xlsx, caminho_csv, aba=0, padrao_br=True):
    """
    Converte Excel em CSV.

    Exemplo:
        excel_para_csv('dados.xlsx', 'dados.csv')
    """
    df = pd.read_excel(caminho_xlsx, sheet_name=aba)
    if padrao_br:
        df.to_csv(caminho_csv, sep=';', decimal=',', index=False, encoding='utf-8-sig')
    else:
        df.to_csv(caminho_csv, index=False, encoding='utf-8')


def excel_todas_abas_para_csvs(caminho_xlsx, pasta_saida, padrao_br=True):
    """
    Converte cada aba de um Excel num CSV separado.
    """
    Path(pasta_saida).mkdir(parents=True, exist_ok=True)
    abas = pd.read_excel(caminho_xlsx, sheet_name=None)
    for nome, df in abas.items():
        nome_limpo = nome.replace(' ', '_').replace('/', '_')
        caminho = Path(pasta_saida) / f'{nome_limpo}.csv'
        if padrao_br:
            df.to_csv(caminho, sep=';', decimal=',', index=False, encoding='utf-8-sig')
        else:
            df.to_csv(caminho, index=False, encoding='utf-8')


def comparar_abas(caminho, aba1, aba2):
    """
    Compara duas abas do mesmo Excel. Retorna diferenças.

    Exemplo:
        diff = comparar_abas('dados.xlsx', 'Antes', 'Depois')
    """
    df1 = pd.read_excel(caminho, sheet_name=aba1)
    df2 = pd.read_excel(caminho, sheet_name=aba2)
    return df1.compare(df2)


if __name__ == '__main__':
    # Teste rápido
    import tempfile
    df = pd.DataFrame({'Nome': ['Ana', 'Bruno'], 'Valor': [100.5, 200.3]})
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        caminho = f.name
    escrever_excel(df, caminho)
    print(ler_excel(caminho))
