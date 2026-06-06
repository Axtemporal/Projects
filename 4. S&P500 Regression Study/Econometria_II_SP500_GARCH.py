# -*- coding: utf-8 -*-
"""
Econometria II - Modelagem de Volatilidade (ARCH/GARCH) - S&P 500
2025.1 - IBMEC Rio
@author: axtem

Objetivo:
    1) Simular um processo ARCH(1) e ilustrar a clusterizacao de volatilidade.
    2) Estimar um modelo GARCH(1,1) para os retornos diarios do S&P 500 e
       avaliar a qualidade do ajuste por meio de diagnosticos.

Dependencias (instalar no terminal antes de rodar):
    pip install arch statsmodels pandas numpy matplotlib yfinance pandas_datareader

Observacao sobre os dados:
    A funcao baixar_sp500() tenta varias fontes em ordem (yfinance, Stooq, FRED).
    Basta ter conexao com a internet. Se nenhuma fonte responder, o script
    levanta um erro explicito em vez de prosseguir com dados invalidos.
"""

import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from arch import arch_model
from statsmodels.graphics.tsaplots import plot_acf
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import adfuller
from scipy import stats

warnings.filterwarnings("ignore")

# Semente para reprodutibilidade da parte simulada
np.random.seed(42)

# Pasta onde os graficos serao salvos (a propria pasta do script)
import os
PASTA_SAIDA = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else "."


# ===========================================================================
# 1. SIMULACAO DE UM PROCESSO ARCH(1)
# ===========================================================================
# Modelo:
#   epsilon_t = sqrt(h_t) * z_t,   z_t ~ N(0,1)
#   h_t       = alpha0 + alpha1 * epsilon_{t-1}^2
# A condicao de estacionariedade da variancia exige alpha1 < 1.
# A variancia incondicional vale alpha0 / (1 - alpha1).

T = 1000
alpha0 = 0.1
alpha1 = 0.8

epsilon = np.zeros(T)   # serie simulada
h = np.zeros(T)         # variancia condicional

# Inicializacao em h_0 = variancia incondicional
h[0] = alpha0 / (1 - alpha1)

# Choques z_t ~ N(0,1)
z = np.random.normal(size=T)

epsilon[0] = np.sqrt(h[0]) * z[0]
for t in range(1, T):
    h[t] = alpha0 + alpha1 * (epsilon[t - 1] ** 2)
    epsilon[t] = np.sqrt(h[t]) * z[t]


# 1b. Graficos da serie simulada e da variancia condicional
plt.figure()
plt.plot(epsilon, linewidth=0.8)
plt.title(r"Serie simulada $\epsilon_t$ - ARCH(1)")
plt.xlabel("Periodo")
plt.ylabel(r"$\epsilon_t$")
plt.axhline(0, color="black", linewidth=0.8)
plt.tight_layout()
plt.savefig(os.path.join(PASTA_SAIDA, "fig1_arch_serie.png"), dpi=150)
plt.show()

plt.figure()
plt.plot(h, color="orange", linewidth=0.8)
plt.title(r"Variancia condicional $h_t$ - ARCH(1)")
plt.xlabel("Periodo")
plt.ylabel(r"$h_t$")
plt.tight_layout()
plt.savefig(os.path.join(PASTA_SAIDA, "fig2_arch_variancia.png"), dpi=150)
plt.show()


# ===========================================================================
# 2. DADOS REAIS: PRECOS DIARIOS DO S&P 500
# ===========================================================================
DATA_INICIO = "2015-01-01"
DATA_FIM = "2024-12-31"


def baixar_sp500(inicio=DATA_INICIO, fim=DATA_FIM):
    """Baixa o preco de fechamento diario do S&P 500 tentando varias fontes.

    Ordem das tentativas:
        1) yfinance         (ticker ^GSPC)
        2) Stooq            (via pandas_datareader, simbolo ^SPX)
        3) FRED             (via pandas_datareader, serie SP500; ~10 anos)
    Retorna uma Series pandas indexada por data, sem valores ausentes.
    """
    # --- Fonte 1: yfinance ---
    try:
        import yfinance as yf
        df = yf.download("^GSPC", start=inicio, end=fim, progress=False, auto_adjust=False)
        if df is not None and len(df) > 0:
            preco = df["Close"]
            if isinstance(preco, pd.DataFrame):
                preco = preco.iloc[:, 0]
            preco = preco.dropna()
            preco.name = "SP500"
            print(f"[dados] Fonte: yfinance | {len(preco)} observacoes "
                  f"({preco.index.min().date()} a {preco.index.max().date()})")
            return preco
    except Exception as e:
        print(f"[dados] yfinance indisponivel: {e}")

    # --- Fonte 2: Stooq ---
    try:
        import pandas_datareader.data as web
        df = web.DataReader("^SPX", "stooq", inicio, fim).sort_index()
        if df is not None and len(df) > 0:
            preco = df["Close"].dropna()
            preco.name = "SP500"
            print(f"[dados] Fonte: Stooq | {len(preco)} observacoes "
                  f"({preco.index.min().date()} a {preco.index.max().date()})")
            return preco
    except Exception as e:
        print(f"[dados] Stooq indisponivel: {e}")

    # --- Fonte 3: FRED (cobre apenas ~10 anos recentes) ---
    try:
        import pandas_datareader.data as web
        df = web.DataReader("SP500", "fred", inicio, fim)
        preco = df["SP500"].dropna()
        preco.name = "SP500"
        print(f"[dados] Fonte: FRED | {len(preco)} observacoes "
              f"({preco.index.min().date()} a {preco.index.max().date()})")
        return preco
    except Exception as e:
        print(f"[dados] FRED indisponivel: {e}")

    raise RuntimeError(
        "Nao foi possivel baixar os dados do S&P 500 de nenhuma fonte. "
        "Verifique a conexao com a internet e os pacotes instalados."
    )


sp500 = baixar_sp500()

# 2b. Grafico do nivel de preco do S&P 500
plt.figure()
plt.plot(sp500, color="navy", linewidth=0.9)
plt.title("Niveis diarios do Indice S&P 500")
plt.xlabel("Data")
plt.ylabel("Preco de fechamento")
plt.tight_layout()
plt.savefig(os.path.join(PASTA_SAIDA, "fig0_preco.png"), dpi=150)
plt.show()


# ===========================================================================
# 3. RETORNOS LOGARITMICOS E VOLATILIDADE MOVEL DE 20 DIAS
# ===========================================================================
log_return = np.log(sp500 / sp500.shift(1))
returns = log_return.dropna()

vol_20 = returns.rolling(window=20).std()


# 3a. ANALISE DESCRITIVA dos retornos
print("\n" + "=" * 70)
print("ANALISE DESCRITIVA DOS RETORNOS LOGARITMICOS DIARIOS")
print("=" * 70)
desc = pd.DataFrame({
    "Estatistica": ["N. observacoes", "Media", "Desvio-padrao", "Minimo",
                    "Maximo", "Assimetria (skewness)", "Curtose"],
    "Valor": [
        int(returns.count()),
        returns.mean(),
        returns.std(),
        returns.min(),
        returns.max(),
        stats.skew(returns),
        stats.kurtosis(returns, fisher=False),
    ],
})
print(desc.to_string(index=False))


# 3b. TESTE DE ESTACIONARIEDADE (Dickey-Fuller Aumentado - ADF)
def reporta_adf(serie, nome):
    adf_stat, p, lags, nobs, crit, _ = adfuller(serie.dropna(), autolag="AIC")
    print(f"\nADF - {nome}:")
    print(f"  Estatistica = {adf_stat:.3f} | p-valor = {p:.4f} | lags = {lags}")
    print(f"  Valores criticos: 1% = {crit['1%']:.3f}, 5% = {crit['5%']:.3f}")
    if p < 0.05:
        print("  -> Rejeita H0: serie ESTACIONARIA (sem raiz unitaria).")
    else:
        print("  -> Nao rejeita H0: serie possui RAIZ UNITARIA (nao estacionaria).")

print("\n" + "=" * 70)
print("TESTE DE RAIZ UNITARIA (ADF)")
print("=" * 70)
reporta_adf(sp500, "Preco do S&P 500 (nivel)")
reporta_adf(returns, "Retornos logaritmicos")


# 3c. Graficos dos retornos e da volatilidade movel
plt.figure()
plt.plot(returns, linewidth=0.7)
plt.title("Retornos logaritmicos diarios - S&P 500")
plt.xlabel("Data")
plt.ylabel("Retorno logaritmico")
plt.axhline(0, color="black", linewidth=0.8)
plt.tight_layout()
plt.savefig(os.path.join(PASTA_SAIDA, "fig3_retornos.png"), dpi=150)
plt.show()

plt.figure()
plt.plot(vol_20, color="red", linewidth=0.8)
plt.title("Volatilidade movel de 20 dias - S&P 500")
plt.xlabel("Data")
plt.ylabel("Desvio-padrao dos retornos (20 dias)")
plt.tight_layout()
plt.savefig(os.path.join(PASTA_SAIDA, "fig4_vol20.png"), dpi=150)
plt.show()


# ===========================================================================
# 4. ESTIMACAO DO MODELO GARCH(1,1) COM MEDIA CONSTANTE
# ===========================================================================
returns_pct = returns * 100

# 4a. SELECAO DE MODELO por AIC/BIC
print("\n" + "=" * 70)
print("COMPARACAO DE MODELOS POR AIC / BIC")
print("=" * 70)
especificacoes = [("ARCH(1)", 1, 0), ("GARCH(1,1)", 1, 1),
                  ("GARCH(1,2)", 1, 2), ("GARCH(2,1)", 2, 1)]
comparacao = []
for nome, p, q in especificacoes:
    res_tmp = arch_model(returns_pct, mean="Constant", vol="GARCH",
                         p=p, q=q).fit(disp="off")
    comparacao.append((nome, res_tmp.aic, res_tmp.bic))
comp_df = pd.DataFrame(comparacao, columns=["Modelo", "AIC", "BIC"])
print(comp_df.to_string(index=False))
melhor = comp_df.loc[comp_df["BIC"].idxmin(), "Modelo"]
print(f"\nMenor BIC: {melhor} (criterio de parcimonia da disciplina).")

# 4b. ESTIMACAO DO MODELO ESCOLHIDO: GARCH(1,1)
model = arch_model(returns_pct, mean="Constant", vol="GARCH", p=1, q=1)
result = model.fit(disp="off")


# ===========================================================================
# 5. DIAGNOSTICOS DO MODELO
# ===========================================================================
cond_vol = pd.Series(result.conditional_volatility, index=returns_pct.index)
hist_vol_20 = vol_20 * 100

plt.figure()
plt.plot(cond_vol, label="Volatilidade condicional (GARCH)", linewidth=0.9)
plt.plot(hist_vol_20, label="Volatilidade historica (20 dias)", alpha=0.7, linewidth=0.9)
plt.title("Volatilidade condicional (GARCH) vs. historica (20 dias)")
plt.xlabel("Data")
plt.ylabel("Volatilidade (%)")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(PASTA_SAIDA, "fig5_vol_garch_vs_hist.png"), dpi=150)
plt.show()

std_resid = pd.Series(result.resid / result.conditional_volatility,
                      index=returns_pct.index)

plt.figure()
plt.plot(std_resid, linewidth=0.7)
plt.title("Residuos padronizados do GARCH(1,1)")
plt.xlabel("Data")
plt.ylabel("Residuo padronizado")
plt.axhline(0, color="black", linewidth=0.8)
plt.tight_layout()
plt.savefig(os.path.join(PASTA_SAIDA, "fig6_residuos.png"), dpi=150)
plt.show()

plt.figure()
plot_acf(std_resid, ax=plt.gca(), lags=20, zero=False)
plt.title("ACF dos residuos padronizados")
plt.xlabel("Defasagem (lag)")
plt.ylabel("Autocorrelacao")
plt.tight_layout()
plt.savefig(os.path.join(PASTA_SAIDA, "fig7_acf_residuos.png"), dpi=150)
plt.show()

plt.figure()
plot_acf(std_resid ** 2, ax=plt.gca(), lags=20, zero=False)
plt.title("ACF dos quadrados dos residuos padronizados")
plt.xlabel("Defasagem (lag)")
plt.ylabel("Autocorrelacao")
plt.tight_layout()
plt.savefig(os.path.join(PASTA_SAIDA, "fig8_acf_residuos2.png"), dpi=150)
plt.show()

plt.figure()
sm.qqplot(std_resid, line="s", ax=plt.gca())
plt.title("Grafico Q-Q dos residuos padronizados")
plt.tight_layout()
plt.savefig(os.path.join(PASTA_SAIDA, "fig9_qqplot.png"), dpi=150)
plt.show()


# ===========================================================================
# 6. RESULTADOS NO CONSOLE: SUMARIO E TESTE DE LJUNG-BOX
# ===========================================================================
print("\n" + "=" * 70)
print("SUMARIO DA ESTIMACAO GARCH(1,1)")
print("=" * 70)
print(result.summary())

alpha1_hat = result.params.get("alpha[1]", np.nan)
beta1_hat = result.params.get("beta[1]", np.nan)
print(f"\nPersistencia (alpha1 + beta1) = {alpha1_hat + beta1_hat:.4f}")

lb_test = acorr_ljungbox(std_resid ** 2, lags=[10], return_df=True)
lb_stat = lb_test["lb_stat"].iloc[0]
lb_pvalue = lb_test["lb_pvalue"].iloc[0]
print("\nTeste de Ljung-Box (lag 10) dos residuos ao quadrado:")
print(f"  Estatistica LB(10) = {lb_stat:.3f} | p-valor = {lb_pvalue:.4f}")
if lb_pvalue > 0.05:
    print("  -> Nao se rejeita H0: sem autocorrelacao residual relevante (bom ajuste).")
else:
    print("  -> Rejeita-se H0: ainda ha autocorrelacao na variancia (ajuste insuficiente).")


# ===========================================================================
# 7. PREVISAO DE VOLATILIDADE
# ===========================================================================
HORIZONTE = 20
forecast = result.forecast(horizon=HORIZONTE, reindex=False)
vol_prevista = np.sqrt(forecast.variance.values[-1, :])

plt.figure()
plt.plot(range(1, HORIZONTE + 1), vol_prevista, marker="o")
plt.title(f"Previsao da volatilidade condicional - proximos {HORIZONTE} dias")
plt.xlabel("Dias a frente")
plt.ylabel("Volatilidade prevista (%)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(PASTA_SAIDA, "fig10_previsao_volatilidade.png"), dpi=150)
plt.show()

print("\n" + "=" * 70)
print(f"PREVISAO DE VOLATILIDADE - proximos {HORIZONTE} dias (% ao dia)")
print("=" * 70)
print(f"Dia 1: {vol_prevista[0]:.3f}% | Dia 5: {vol_prevista[4]:.3f}% | Dia 20: {vol_prevista[-1]:.3f}%")
