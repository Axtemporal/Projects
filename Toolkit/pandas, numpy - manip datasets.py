"""
04_merge_agregacao.py
Combinar e sumarizar datasets. 
"""

import pandas as pd
import numpy as np


# ============================================================
# Merge
# ============================================================

def merge_debug(df1, df2, on=None, how='inner', **kwargs):
    """
    Merge com indicador de origem. Printa contagem para conferir.
    Essencial quando você não tem certeza se as chaves batem.

    Exemplo:
        resultado = merge_debug(vendas, clientes, on='id_cliente', how='left')
    """
    resultado = df1.merge(df2, on=on, how=how, indicator=True, **kwargs)
    print('Origem das linhas:')
    print(resultado['_merge'].value_counts())
    print(f'\nTotal: {len(resultado)} linhas')
    return resultado.drop('_merge', axis=1)


def merge_validado(df1, df2, on, validacao='1:1', how='inner'):
    """
    Merge que falha se a relação não for a esperada.
    Previne bug silencioso de duplicação por chave duplicada.

    validacao: '1:1', '1:m', 'm:1', 'm:m'

    Exemplo:
        df = merge_validado(cotas, cotacoes, 'data', '1:1')
    """
    return df1.merge(df2, on=on, how=how, validate=validacao)


def verificar_chaves(df1, df2, coluna):
    """
    Mostra quantas chaves estão só em cada lado.
    Rode antes do merge para saber o que esperar.

    Exemplo:
        verificar_chaves(vendas, clientes, 'id_cliente')
    """
    k1 = set(df1[coluna].dropna())
    k2 = set(df2[coluna].dropna())
    return {
        'so_em_df1': len(k1 - k2),
        'so_em_df2': len(k2 - k1),
        'em_ambos': len(k1 & k2),
        'total_df1': len(k1),
        'total_df2': len(k2),
        'exemplos_so_df1': list(k1 - k2)[:5],
        'exemplos_so_df2': list(k2 - k1)[:5]
    }


def merge_mais_proximo(df1, df2, col_data, por=None, direcao='backward'):
    """
    Merge as-of: junta pela data mais próxima, não exata.
    Útil para juntar cotações com datas ligeiramente diferentes.

    direcao: 'backward' (usa data anterior), 'forward' (posterior), 'nearest'

    Exemplo:
        combinado = merge_mais_proximo(trades, precos, 'data')
    """
    df1 = df1.sort_values(col_data)
    df2 = df2.sort_values(col_data)
    return pd.merge_asof(df1, df2, on=col_data, by=por, direction=direcao)


def empilhar_dataframes(lista_dfs, adicionar_origem=None):
    """
    Concatena lista de DataFrames adicionando coluna de origem.

    Exemplo:
        df = empilhar_dataframes([df_2023, df_2024, df_2025],
                                  adicionar_origem=['2023', '2024', '2025'])
    """
    if adicionar_origem:
        for df, tag in zip(lista_dfs, adicionar_origem):
            df['origem'] = tag
    return pd.concat(lista_dfs, ignore_index=True)


# ============================================================
# Agregacao
# ============================================================

def resumir_por_grupo(df, grupo, numericas=None):
    """
    Agregação padrão com várias métricas para cada coluna numérica.

    Exemplo:
        resumo = resumir_por_grupo(df, 'setor', ['preco', 'volume'])
    """
    if numericas is None:
        numericas = df.select_dtypes(include=np.number).columns.tolist()
    return df.groupby(grupo)[numericas].agg(
        ['count', 'mean', 'median', 'std', 'min', 'max', 'sum']
    )


def agregar_multiplo(df, grupo, agregacoes):
    """
    Groupby com agregações diferentes por coluna.

    Exemplo:
        agregar_multiplo(df, 'setor', {
            'preco': 'mean',
            'volume': ['sum', 'mean'],
            'retorno': ['mean', 'std', 'max']
        })
    """
    return df.groupby(grupo).agg(agregacoes)


def ranking_por_grupo(df, grupo, coluna, top=10, ascending=False):
    """
    Top N de cada grupo ordenado por uma coluna.

    Exemplo:
        top5_por_setor = ranking_por_grupo(df, 'setor', 'retorno', 5)
    """
    return (df.sort_values(coluna, ascending=ascending)
              .groupby(grupo)
              .head(top))


def contribuicao_percentual(df, coluna, grupo):
    """
    Adiciona coluna com % que cada linha representa dentro do seu grupo.

    Exemplo:
        df = contribuicao_percentual(df, 'receita', 'setor')
    """
    df = df.copy()
    totais = df.groupby(grupo)[coluna].transform('sum')
    df[f'{coluna}_pct_grupo'] = df[coluna] / totais
    return df


def pivot_temporal(df, col_data, col_ativo, col_valor):
    """
    Formato clássico de séries financeiras.
    Linhas = data, colunas = ativo, valores = preço.

    Exemplo:
        precos_wide = pivot_temporal(df, 'data', 'ticker', 'fechamento')
    """
    return df.pivot_table(index=col_data, columns=col_ativo, values=col_valor)


def derreter(df, id_vars, var_name='variavel', value_name='valor'):
    """
    Transforma formato wide para long (inverso do pivot).
    Útil para análise e visualização.

    Exemplo:
        df_long = derreter(df_wide, id_vars=['data'])
    """
    return df.melt(id_vars=id_vars, var_name=var_name, value_name=value_name)


# ============================================================
# Tabelas cruzadas
# ============================================================

def tabela_cruzada(df, linhas, colunas, valores=None, agg='count', normalizar=False):
    """
    Tabela cruzada com contagem ou agregação.
    normalizar: False, 'index' (% por linha), 'columns' (% por coluna), 'all'

    Exemplo:
        tabela_cruzada(df, 'setor', 'ano', 'receita', 'sum')
    """
    if valores is None:
        return pd.crosstab(df[linhas], df[colunas], normalize=normalizar)
    return pd.crosstab(df[linhas], df[colunas], values=df[valores],
                       aggfunc=agg, normalize=normalizar)
