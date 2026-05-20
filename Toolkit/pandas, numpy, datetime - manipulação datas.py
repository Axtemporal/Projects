"""
03_datas.py
Manipulação de datas com atenção ao formato brasileiro (dd/mm/yyyy).
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def converter_data_br(serie):
    """
    Converte série para datetime assumindo formato BR (dia primeiro).
    Valores inválidos viram NaT em vez de quebrar.

    Exemplo:
        df['data'] = converter_data_br(df['data'])
    """
    return pd.to_datetime(serie, errors='coerce', dayfirst=True)


def converter_data_multi_formato(serie, formatos=None):
    """
    Tenta vários formatos de data em sequência.
    Útil quando a coluna tem formatos misturados.
    """
    if formatos is None:
        formatos = [
            '%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y',
            '%m/%d/%Y', '%d/%m/%y', '%Y%m%d'
        ]

    resultado = pd.Series([pd.NaT] * len(serie), index=serie.index)
    for fmt in formatos:
        mask = resultado.isna() & serie.notna()
        if not mask.any():
            break
        try:
            convertido = pd.to_datetime(serie[mask], format=fmt, errors='coerce')
            resultado.loc[mask] = convertido
        except Exception:
            continue
    return resultado


def adicionar_features_data(df, col_data, prefixo=None):
    """
    Cria colunas derivadas a partir de uma coluna de data.
    Útil para análise por ano, mês, trimestre, dia útil.
    """
    df = df.copy()
    df[col_data] = pd.to_datetime(df[col_data])
    p = prefixo if prefixo else col_data
    df[f'{p}_ano'] = df[col_data].dt.year
    df[f'{p}_mes'] = df[col_data].dt.month
    df[f'{p}_trimestre'] = df[col_data].dt.quarter
    df[f'{p}_dia'] = df[col_data].dt.day
    df[f'{p}_dia_semana'] = df[col_data].dt.dayofweek  # 0=segunda
    df[f'{p}_nome_dia'] = df[col_data].dt.day_name()
    df[f'{p}_eh_util'] = df[col_data].dt.dayofweek < 5
    df[f'{p}_ano_mes'] = df[col_data].dt.to_period('M').astype(str)
    return df


def dias_uteis(inicio, fim):
    """
    Retorna DatetimeIndex com dias úteis entre duas datas.
    Não considera feriados (só exclui sábado e domingo).

    Exemplo:
        dias = dias_uteis('2025-01-01', '2025-12-31')
    """
    return pd.bdate_range(inicio, fim)


def somar_meses(data, n):
    """
    Soma n meses respeitando fim de mês.
    somar_meses('2025-01-31', 1) retorna 2025-02-28.
    """
    return pd.to_datetime(data) + pd.DateOffset(months=n)


def diferenca_dias(data_inicio, data_fim):
    """Diferença em dias entre duas datas ou séries."""
    return (pd.to_datetime(data_fim) - pd.to_datetime(data_inicio)).dt.days


def diferenca_anos(data_inicio, data_fim):
    """
    Diferença em anos (float) considerando dias corridos.
    Útil para calcular idade ou duration.
    """
    return diferenca_dias(data_inicio, data_fim) / 365.25


# ============================================================
# Resample e janelas moveis
# ============================================================

def resample_financeiro(df, col_data, regra='M', agg='last'):
    """
    Resample típico de séries financeiras.

    regra: 'D' diário, 'W' semanal, 'M' mensal, 'Q' trimestral, 'A' anual
    agg: 'last' (fechamento), 'mean' (média), 'ohlc' (abre/alta/baixa/fecha)

    Exemplo:
        mensal = resample_financeiro(df, 'data', 'M', 'last')
    """
    df = df.copy()
    df[col_data] = pd.to_datetime(df[col_data])
    return df.set_index(col_data).resample(regra).agg(agg)


def media_movel(serie, janela=21):
    """Média móvel simples. Janela padrão de 21 dias úteis (1 mês)."""
    return serie.rolling(window=janela).mean()


def media_movel_exponencial(serie, periodo=21):
    """Média móvel exponencial (mais peso em dados recentes)."""
    return serie.ewm(span=periodo, adjust=False).mean()


def volatilidade_movel(retornos, janela=21, periodos_ano=252):
    """
    Volatilidade anualizada em janela móvel.
    """
    return retornos.rolling(janela).std() * np.sqrt(periodos_ano)


# ============================================================
# Feriados brasileiros (simplificado)
# ============================================================

def feriados_fixos_br(ano):
    """
    Retorna lista de feriados nacionais com data fixa.
    Não inclui Carnaval, Páscoa, Corpus Christi (dependem de cálculo).
    """
    return [
        pd.Timestamp(f'{ano}-01-01'),  # Confraternização
        pd.Timestamp(f'{ano}-04-21'),  # Tiradentes
        pd.Timestamp(f'{ano}-05-01'),  # Trabalho
        pd.Timestamp(f'{ano}-09-07'),  # Independência
        pd.Timestamp(f'{ano}-10-12'),  # Padroeira
        pd.Timestamp(f'{ano}-11-02'),  # Finados
        pd.Timestamp(f'{ano}-11-15'),  # República
        pd.Timestamp(f'{ano}-12-25'),  # Natal
    ]


def dias_uteis_br(inicio, fim, feriados=None):
    """
    Dias úteis excluindo feriados fornecidos.

    Exemplo:
        fer = feriados_fixos_br(2025) + feriados_fixos_br(2026)
        dias = dias_uteis_br('2025-01-01', '2026-01-01', fer)
    """
    dias = pd.bdate_range(inicio, fim)
    if feriados:
        dias = dias.difference(pd.DatetimeIndex(feriados))
    return dias
