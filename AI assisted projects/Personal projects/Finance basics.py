"""
05_financas.py
Cálculos financeiros essenciais para análise de ativos e portfólios.
Foco em retornos, risco, drawdown, métricas de desempenho e portfólio.
"""

import pandas as pd
import numpy as np


# ============================================================
# Retornos
# ============================================================

def retorno_simples(precos):
    """
    Retorno aritmético: (P_t / P_{t-1}) - 1

    Exemplo:
        df['retorno'] = retorno_simples(df['fechamento'])
    """
    return precos.pct_change()


def retorno_log(precos):
    """
    Retorno logarítmico: ln(P_t / P_{t-1}).
    Aditivo no tempo, mais usado em modelos quantitativos.
    """
    return np.log(precos / precos.shift(1))


def retorno_acumulado(retornos):
    """
    Retorno acumulado a partir de série de retornos simples.
    (1+r1)(1+r2)...(1+rn) - 1
    """
    return (1 + retornos).cumprod() - 1


def retorno_total(precos):
    """Retorno total entre início e fim da série."""
    return precos.iloc[-1] / precos.iloc[0] - 1


def retorno_anualizado(retornos, periodos_ano=252):
    """
    Anualiza uma série de retornos pela média geométrica.
    periodos_ano: 252 (diário), 52 (semanal), 12 (mensal), 4 (trimestral)
    """
    n = len(retornos.dropna())
    if n == 0:
        return np.nan
    acumulado = (1 + retornos.dropna()).prod()
    return acumulado ** (periodos_ano / n) - 1


def cagr(precos, periodos_ano=252):
    """
    Compound Annual Growth Rate a partir de série de preços.
    """
    n = len(precos.dropna())
    if n < 2:
        return np.nan
    total = precos.iloc[-1] / precos.iloc[0]
    return total ** (periodos_ano / n) - 1


# ============================================================
# Risco
# ============================================================

def volatilidade_anualizada(retornos, periodos_ano=252):
    """
    Volatilidade anualizada: desvio padrão vezes raiz de periodos_ano.
    """
    return retornos.std() * np.sqrt(periodos_ano)


def downside_deviation(retornos, mar=0, periodos_ano=252):
    """
    Desvio padrão só dos retornos abaixo do MAR (minimum acceptable return).
    Usado no Sortino.
    """
    abaixo = retornos[retornos < mar] - mar
    return np.sqrt((abaixo ** 2).mean()) * np.sqrt(periodos_ano)


def max_drawdown(precos):
    """
    Máxima queda desde o pico histórico.
    Retorna dict com valor, data do pico e data do fundo.

    Exemplo:
        dd = max_drawdown(df['preco'])
        print(f"Max DD: {dd['max_drawdown']:.2%}")
    """
    acumulado = precos / precos.iloc[0]
    pico = acumulado.cummax()
    dd_serie = (acumulado / pico) - 1

    data_fundo = dd_serie.idxmin()
    data_pico = acumulado[:data_fundo].idxmax()

    return {
        'max_drawdown': dd_serie.min(),
        'data_pico': data_pico,
        'data_fundo': data_fundo,
        'dias_drawdown': (data_fundo - data_pico).days if hasattr(data_fundo, 'days') or hasattr(data_fundo, 'date') else None,
        'serie_drawdown': dd_serie
    }


def var_historico(retornos, nivel=0.05):
    """
    Value at Risk histórico.
    nivel=0.05 para VaR 95%.
    """
    return retornos.quantile(nivel)


def cvar_historico(retornos, nivel=0.05):
    """
    Conditional VaR: média das perdas piores que o VaR.
    Também chamado Expected Shortfall.
    """
    var = var_historico(retornos, nivel)
    return retornos[retornos <= var].mean()


def var_parametrico(retornos, nivel=0.05):
    """
    VaR assumindo distribuição normal dos retornos.
    """
    from scipy import stats
    return retornos.mean() + stats.norm.ppf(nivel) * retornos.std()


# ============================================================
# Metricas ajustadas ao risco
# ============================================================

def sharpe(retornos, taxa_livre_risco=0, periodos_ano=252):
    """
    Sharpe ratio anualizado.
    taxa_livre_risco no mesmo período dos retornos.

    Exemplo (diário, CDI médio de 11% a.a.):
        cdi_diario = (1.11) ** (1/252) - 1
        s = sharpe(retornos, cdi_diario)
    """
    excesso = retornos - taxa_livre_risco
    if excesso.std() == 0:
        return np.nan
    return (excesso.mean() / excesso.std()) * np.sqrt(periodos_ano)


def sortino(retornos, taxa_livre_risco=0, periodos_ano=252):
    """
    Sortino: como Sharpe, mas só penaliza volatilidade negativa.
    """
    excesso = retornos - taxa_livre_risco
    dd = downside_deviation(retornos, taxa_livre_risco, periodos_ano=1)
    if dd == 0:
        return np.nan
    return (excesso.mean() * periodos_ano) / dd


def calmar(precos, periodos_ano=252):
    """
    Calmar ratio: retorno anualizado dividido pelo max drawdown absoluto.
    """
    ret_anual = cagr(precos, periodos_ano)
    dd = abs(max_drawdown(precos)['max_drawdown'])
    if dd == 0:
        return np.nan
    return ret_anual / dd


def information_ratio(retornos_ativo, retornos_benchmark, periodos_ano=252):
    """
    IR: retorno ativo (alfa) dividido pelo tracking error.
    """
    excesso = retornos_ativo - retornos_benchmark
    if excesso.std() == 0:
        return np.nan
    return (excesso.mean() / excesso.std()) * np.sqrt(periodos_ano)


def tracking_error(retornos_ativo, retornos_benchmark, periodos_ano=252):
    """Volatilidade anualizada da diferença entre ativo e benchmark."""
    excesso = retornos_ativo - retornos_benchmark
    return excesso.std() * np.sqrt(periodos_ano)


# ============================================================
# Beta e regressao
# ============================================================

def beta_simples(retornos_ativo, retornos_mercado):
    """
    Beta via covariância: cov(ativo, mercado) / var(mercado).
    """
    df = pd.DataFrame({'a': retornos_ativo, 'm': retornos_mercado}).dropna()
    cov = df['a'].cov(df['m'])
    var = df['m'].var()
    return cov / var if var else np.nan


def capm(retornos_ativo, retornos_mercado, taxa_livre=0):
    """
    Regressão CAPM: R_ativo - Rf = alfa + beta * (R_mercado - Rf).
    Retorna dict com alfa, beta, r-quadrado, e p-valor do beta.

    Exemplo:
        res = capm(ret_petr, ret_ibov, cdi_diario)
    """
    df = pd.DataFrame({
        'ativo': retornos_ativo - taxa_livre,
        'mercado': retornos_mercado - taxa_livre
    }).dropna()

    x = df['mercado']
    y = df['ativo']

    beta, alfa = np.polyfit(x, y, 1)
    pred = alfa + beta * x
    ss_res = ((y - pred) ** 2).sum()
    ss_tot = ((y - y.mean()) ** 2).sum()
    r2 = 1 - ss_res / ss_tot if ss_tot else np.nan

    return {'alfa': alfa, 'beta': beta, 'r2': r2}


def correlacao_matriz(df_retornos):
    """Matriz de correlação entre ativos."""
    return df_retornos.corr()


# ============================================================
# Portfolio
# ============================================================

def retorno_portfolio(df_retornos, pesos):
    """
    Série de retornos de portfólio dado DataFrame e pesos.
    pesos deve somar 1.

    Exemplo:
        pesos = [0.4, 0.3, 0.3]
        ret_port = retorno_portfolio(df[['PETR4', 'VALE3', 'ITUB4']], pesos)
    """
    pesos = np.array(pesos)
    return (df_retornos * pesos).sum(axis=1)


def volatilidade_portfolio(df_retornos, pesos, periodos_ano=252):
    """
    Volatilidade anualizada do portfólio considerando matriz de covariância.
    """
    pesos = np.array(pesos)
    cov = df_retornos.cov() * periodos_ano
    var_port = pesos @ cov.values @ pesos.T
    return np.sqrt(var_port)


def pesos_minima_variancia(df_retornos):
    """
    Portfólio de mínima variância (sem restrição de venda a descoberto).
    Solução analítica: inv(cov) * uns / (uns' * inv(cov) * uns).
    """
    cov = df_retornos.cov().values
    inv_cov = np.linalg.inv(cov)
    uns = np.ones(len(cov))
    pesos = inv_cov @ uns / (uns @ inv_cov @ uns)
    return pd.Series(pesos, index=df_retornos.columns)


# ============================================================
# Valor do dinheiro no tempo
# ============================================================

def npv(taxa, fluxos):
    """
    Valor presente líquido.
    fluxos[0] é o investimento inicial (normalmente negativo).

    Exemplo:
        vpl = npv(0.10, [-1000, 300, 400, 500])
    """
    return sum(f / (1 + taxa) ** t for t, f in enumerate(fluxos))


def irr(fluxos, chute=0.1, max_iter=1000, tol=1e-8):
    """
    Taxa interna de retorno via Newton-Raphson.
    Para casos com múltiplos sinais trocados, use scipy.optimize.brentq.

    Exemplo:
        taxa = irr([-1000, 300, 400, 500])
    """
    taxa = chute
    for _ in range(max_iter):
        npv_val = sum(f / (1 + taxa) ** t for t, f in enumerate(fluxos))
        dnpv = sum(-t * f / (1 + taxa) ** (t + 1) for t, f in enumerate(fluxos))
        if abs(dnpv) < tol:
            break
        nova = taxa - npv_val / dnpv
        if abs(nova - taxa) < tol:
            return nova
        taxa = nova
    return taxa


def valor_presente(valor_futuro, taxa, periodos):
    """PV = FV / (1+r)^n"""
    return valor_futuro / (1 + taxa) ** periodos


def valor_futuro(valor_presente, taxa, periodos):
    """FV = PV * (1+r)^n"""
    return valor_presente * (1 + taxa) ** periodos


def pmt(valor_presente_val, taxa, periodos):
    """
    Pagamento periódico de um empréstimo (Tabela Price).

    Exemplo (financiamento de 100k em 60 meses a 1% a.m.):
        parcela = pmt(100000, 0.01, 60)
    """
    if taxa == 0:
        return valor_presente_val / periodos
    return valor_presente_val * taxa / (1 - (1 + taxa) ** -periodos)


def taxa_equivalente(taxa, de_periodos, para_periodos):
    """
    Converte taxa entre períodos (ex: anual para mensal).

    Exemplo:
        taxa_mensal = taxa_equivalente(0.12, 1, 12)  # 12% a.a. para mensal
    """
    return (1 + taxa) ** (de_periodos / para_periodos) - 1


# ============================================================
# Resumo geral
# ============================================================

def resumo_desempenho(precos, taxa_livre_risco=0, periodos_ano=252):
    """
    Dashboard de métricas para um ativo. Use quando pedirem "analise este ativo".

    Exemplo:
        res = resumo_desempenho(df['PETR4'])
        for k, v in res.items():
            print(f'{k}: {v}')
    """
    precos = precos.dropna()
    ret = retorno_simples(precos).dropna()
    dd = max_drawdown(precos)

    return {
        'periodo_inicio': precos.index[0] if hasattr(precos.index, '__getitem__') else None,
        'periodo_fim': precos.index[-1] if hasattr(precos.index, '__getitem__') else None,
        'n_observacoes': len(precos),
        'retorno_total': retorno_total(precos),
        'cagr': cagr(precos, periodos_ano),
        'vol_anualizada': volatilidade_anualizada(ret, periodos_ano),
        'sharpe': sharpe(ret, taxa_livre_risco, periodos_ano),
        'sortino': sortino(ret, taxa_livre_risco, periodos_ano),
        'calmar': calmar(precos, periodos_ano),
        'max_drawdown': dd['max_drawdown'],
        'var_95': var_historico(ret, 0.05),
        'cvar_95': cvar_historico(ret, 0.05),
        'melhor_dia': ret.max(),
        'pior_dia': ret.min(),
        'pct_dias_positivos': (ret > 0).mean()
    }


def comparar_ativos(df_precos, taxa_livre_risco=0, periodos_ano=252):
    """
    Retorna DataFrame com resumo_desempenho para cada coluna.

    Exemplo:
        tabela = comparar_ativos(df_precos[['PETR4', 'VALE3', 'ITUB4']])
    """
    return pd.DataFrame({
        col: resumo_desempenho(df_precos[col], taxa_livre_risco, periodos_ano)
        for col in df_precos.columns
    })
