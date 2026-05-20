"""
02_limpeza.py
Tratamento de dados sujos. Foco em padrão brasileiro de formatação.
"""

import pandas as pd
import numpy as np
import re
import unicodedata


# ============================================================
# Texto
# ============================================================

def remover_acentos(texto):
    """
    Remove acentos mantendo a letra base.
    'São Paulo' vira 'Sao Paulo'.
    """
    if pd.isna(texto):
        return texto
    nfkd = unicodedata.normalize('NFKD', str(texto))
    return ''.join(c for c in nfkd if not unicodedata.combining(c))


def normalizar_texto(serie):
    """
    Pipeline padrão de limpeza de texto: strip, lower, sem acento, sem espaço duplo.

    Exemplo:
        df['cidade'] = normalizar_texto(df['cidade'])
    """
    return (serie.astype(str)
                 .str.strip()
                 .str.lower()
                 .apply(remover_acentos)
                 .str.replace(r'\s+', ' ', regex=True))


def padronizar_nomes_colunas(df):
    """
    Padroniza colunas para snake_case sem acento.
    'Nome Completo' vira 'nome_completo'.
    """
    df = df.copy()
    novas = []
    for c in df.columns:
        c2 = remover_acentos(str(c)).lower().strip()
        c2 = re.sub(r'[\s\-]+', '_', c2)
        c2 = re.sub(r'[^\w]', '', c2)
        novas.append(c2)
    df.columns = novas
    return df


# ============================================================
# Numeros em formato BR
# ============================================================

def valor_br_para_float(valor):
    """
    Converte número em formato BR para float.

    'R$ 1.234,56'   vira 1234.56
    '1.234,56'      vira 1234.56
    '(1.234,56)'    vira -1234.56  (contábil)
    '12,5%'         vira 0.125

    Exemplo:
        df['preco'] = df['preco'].apply(valor_br_para_float)
    """
    if pd.isna(valor):
        return np.nan
    if isinstance(valor, (int, float)):
        return float(valor)

    s = str(valor).strip()
    if not s:
        return np.nan

    eh_percentual = '%' in s
    negativo = (s.startswith('(') and s.endswith(')')) or '-' in s

    s = re.sub(r'[^\d,.]', '', s)
    s = s.replace('.', '').replace(',', '.')

    try:
        num = float(s)
        if negativo:
            num = -abs(num)
        if eh_percentual:
            num = num / 100
        return num
    except ValueError:
        return np.nan


def percentual_para_float(valor):
    """
    '12,5%' vira 0.125 (decimal).
    Se quiser manter como 12.5, divida por 100 depois.
    """
    if pd.isna(valor):
        return np.nan
    s = str(valor).replace('%', '').replace(',', '.').strip()
    try:
        return float(s) / 100
    except ValueError:
        return np.nan


def converter_colunas_numericas(df, colunas):
    """
    Aplica valor_br_para_float em várias colunas de uma vez.

    Exemplo:
        df = converter_colunas_numericas(df, ['receita', 'ebitda', 'lucro'])
    """
    df = df.copy()
    for col in colunas:
        df[col] = df[col].apply(valor_br_para_float)
    return df


def formatar_valor_br(valor, casas=2, com_simbolo=True):
    """
    Formata float como string no padrão BR.
    1234.56 vira 'R$ 1.234,56'.
    """
    if pd.isna(valor):
        return ''
    s = f'{valor:,.{casas}f}'
    s = s.replace(',', 'X').replace('.', ',').replace('X', '.')
    return f'R$ {s}' if com_simbolo else s


# ============================================================
# Nulos e duplicatas
# ============================================================

def resumo_nulos(df):
    """Resumo de valores nulos por coluna."""
    nulos = df.isna().sum()
    pct = (nulos / len(df) * 100).round(2)
    resumo = pd.DataFrame({'nulos': nulos, 'pct': pct})
    return resumo[resumo['nulos'] > 0].sort_values('nulos', ascending=False)


def preencher_nulos(df, estrategia='mediana'):
    """
    Preenche nulos: mediana/média para numéricos, moda para texto.
    estrategia: 'mediana', 'media', 'zero'
    """
    df = df.copy()
    for col in df.columns:
        if not df[col].isna().any():
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            if estrategia == 'mediana':
                df[col] = df[col].fillna(df[col].median())
            elif estrategia == 'media':
                df[col] = df[col].fillna(df[col].mean())
            else:
                df[col] = df[col].fillna(0)
        else:
            moda = df[col].mode()
            if len(moda) > 0:
                df[col] = df[col].fillna(moda[0])
    return df


def remover_duplicatas(df, chave=None, manter='first'):
    """
    Remove duplicatas, opcionalmente por subset de colunas.
    manter: 'first', 'last', ou False (remove todas)
    """
    antes = len(df)
    df = df.drop_duplicates(subset=chave, keep=manter)
    print(f'Removidas {antes - len(df)} duplicatas.')
    return df


# ============================================================
# Outliers
# ============================================================

def detectar_outliers_iqr(serie, fator=1.5):
    """
    Retorna máscara booleana marcando outliers pelo IQR.

    Exemplo:
        mask = detectar_outliers_iqr(df['preco'])
        df_limpo = df[~mask]
        outliers = df[mask]
    """
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    iqr = q3 - q1
    inf = q1 - fator * iqr
    sup = q3 + fator * iqr
    return (serie < inf) | (serie > sup)


def detectar_outliers_zscore(serie, limite=3):
    """
    Marca outliers com |z-score| acima do limite.
    """
    z = (serie - serie.mean()) / serie.std()
    return z.abs() > limite


def winsorizar(serie, limite_inf=0.01, limite_sup=0.99):
    """
    Substitui valores extremos pelos limites do percentil.
    Alternativa a remover outliers.

    Exemplo:
        df['retorno'] = winsorizar(df['retorno'])
    """
    inf = serie.quantile(limite_inf)
    sup = serie.quantile(limite_sup)
    return serie.clip(lower=inf, upper=sup)


# ============================================================
# Validacao
# ============================================================

def validar_ranges(df, regras):
    """
    Verifica se colunas estão dentro dos ranges esperados.
    regras: dict {coluna: (min, max)}

    Exemplo:
        problemas = validar_ranges(df, {
            'idade': (0, 120),
            'preco': (0, None),
            'percentual': (0, 1)
        })
    """
    problemas = {}
    for col, (minimo, maximo) in regras.items():
        if col not in df.columns:
            continue
        mask = pd.Series([False] * len(df), index=df.index)
        if minimo is not None:
            mask |= df[col] < minimo
        if maximo is not None:
            mask |= df[col] > maximo
        if mask.any():
            problemas[col] = df[mask]
    return problemas
