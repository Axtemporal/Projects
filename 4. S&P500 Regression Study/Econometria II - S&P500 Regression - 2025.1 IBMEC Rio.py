# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 23:23:14 2026

@author: axtem
"""

!pip install arch pandas_datareader statsmodels


# Simulação de um processo ARCH(1) com parâmetros alpha0=0.1 e alpha1=0.8
# Nota: certifique-se de ter instalados os pacotes `arch`, `pandas_datareader`, `statsmodels` etc. via pip antes de executar.
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from arch import arch_model
from statsmodels.graphics.tsaplots import plot_acf
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox

# 1. Simulação do processo ARCH(1) para T=1000 períodos
T = 1000
alpha0 = 0.1
alpha1 = 0.8

# Arrays para epsilon (série simulada) e h (variância condicional)
epsilon = np.zeros(T)
h = np.zeros(T)

# Valor inicial de h (variância condicional no período 0) - assumimos variância incondicional para inicializar
h[0] = alpha0 / (1 - alpha1)

# Gerando ruído aleatório z_t ~ N(0,1) para t = 0,...,T-1
z = np.random.normal(size=T)

# Calculando epsilon[0] com base em h[0]
epsilon[0] = np.sqrt(h[0]) * z[0]

# Iteração para gerar a série ARCH(1)
for t in range(1, T):
    # h_t = alpha0 + alpha1 * (epsilon_{t-1})^2
    h[t] = alpha0 + alpha1 * (epsilon[t-1] ** 2)
    # epsilon_t = sqrt(h_t) * z_t
    epsilon[t] = np.sqrt(h[t]) * z[t]


# 2. Plotar a série simulada epsilon_t e a variância condicional h_t
plt.figure()
plt.plot(epsilon, label="epsilon_t")
plt.title("Série simulada $\epsilon_t$")
plt.xlabel("Período")
plt.ylabel("$\epsilon_t$")
plt.show()

plt.figure()
plt.plot(h, color='orange', label="h_t")
plt.title("Variância condicional $h_t$")
plt.xlabel("Período")
plt.ylabel("$h_t$")
plt.show()



# 3. Baixar preços diários do S&P 500 (ano de 2018) via API do FRED
start_date = "2018-01-01"
end_date = "2018-12-31"
sp500 = web.DataReader('SP500', 'fred', start_date, end_date)



# 4. Calcular retornos logarítmicos diários e volatilidade móvel de 20 dias
# Cálculo dos retornos logarítmicos diários (usando preço de fechamento do índice)
sp500['LogReturn'] = np.log(sp500['SP500'] / sp500['SP500'].shift(1))
# Remover o primeiro valor NaN resultante da diferença
returns = sp500['LogReturn'].dropna()

# Calcular a volatilidade histórica móvel de 20 dias (desvio padrão dos últimos 20 retornos)
vol_20 = returns.rolling(window=20).std()



# 5. Plotar os retornos diários e a volatilidade móvel de 20 dias
plt.figure()
plt.plot(returns, label="Retorno diário")
plt.title("Retornos logarítmicos diários - S&P 500 (2018)")
plt.xlabel("Data")
plt.ylabel("Retorno logarítmico")
plt.axhline(0, color='black', linewidth=0.8)  # linha horizontal em 0 para referência
plt.show()

plt.figure()
plt.plot(vol_20, color='red', label="Volatilidade 20 dias")
plt.title("Volatilidade móvel de 20 dias - S&P 500 (2018)")
plt.xlabel("Data")
plt.ylabel("Desvio padrão dos retornos (20 dias)")
plt.show()



# 6. Estimar um modelo GARCH(1,1) com média constante para os retornos (em %)
# Escalar os retornos por 100 para tê-los em porcentagem
returns_pct = returns * 100

# Definir e ajustar o modelo GARCH(1,1)
model = arch_model(returns_pct, mean='Constant', vol='GARCH', p=1, q=1)
result = model.fit(disp='off')




# 7. Análise dos resultados do modelo GARCH(1,1) - gráficos de diagnóstico
# (a) Volatilidade condicional estimada vs. volatilidade histórica (20 dias)
# Obter volatilidade condicional estimada (desvio padrão condicional) do modelo GARCH
cond_vol = result.conditional_volatility
# Converter em Série pandas para alinhar com datas (mesmo índice dos retornos)
cond_vol = pd.Series(cond_vol, index=returns_pct.index)
# Volatilidade histórica de 20 dias em % (desvio padrão * 100)
hist_vol_20 = vol_20 * 100

plt.figure()
plt.plot(cond_vol, label="Volatilidade condicional (GARCH)")
plt.plot(hist_vol_20, label="Volatilidade histórica (20 dias)", alpha=0.7)
plt.title("Volatilidade condicional estimada vs. volatilidade histórica (20 dias)")
plt.xlabel("Data")
plt.ylabel("Volatilidade (%)")
plt.legend()
plt.show()






# (b) Resíduos padronizados do modelo GARCH(1,1)
# (resíduo = retorno - média ajustada; padronizado = resíduo / desvio padrão condicional)
residuals = result.resid
std_resid = residuals / result.conditional_volatility
std_resid = pd.Series(std_resid, index=returns_pct.index)

plt.figure()
plt.plot(std_resid, label="Resíduo padronizado")
plt.title("Resíduos padronizados do modelo GARCH(1,1)")
plt.xlabel("Data")
plt.ylabel("Resíduo padronizado")
plt.axhline(0, color='black', linewidth=0.8)
plt.show()




# (c) ACF dos resíduos padronizados
plt.figure()
plot_acf(std_resid, ax=plt.gca(), lags=20, zero=False)
plt.title("ACF dos resíduos padronizados")
plt.xlabel("Defasagem (lag)")
plt.ylabel("Autocorrelação")
plt.show()





# (d) ACF dos quadrados dos resíduos padronizados
plt.figure()
plot_acf(std_resid**2, ax=plt.gca(), lags=20, zero=False)
plt.title("ACF dos quadrados dos resíduos padronizados")
plt.xlabel("Defasagem (lag)")
plt.ylabel("Autocorrelação")
plt.show()



# (e) Gráfico Q-Q dos resíduos padronizados (comparação com distribuição normal)
plt.figure()
sm.qqplot(std_resid, line='s', ax=plt.gca())
plt.title("Gráfico Q-Q dos resíduos padronizados")
plt.show()



# 8. Exibir no console o sumário da estimação GARCH(1,1) e o teste Ljung-Box (lag 10) para resíduos^2
print("Sumário da estimação GARCH(1,1):")
print(result.summary())

# Teste de Ljung-Box para autocorrelação dos resíduos ao quadrado (lag = 10)
lb_test = acorr_ljungbox(std_resid**2, lags=[10], return_df=True)
lb_stat = lb_test['lb_stat'].iloc[0]
lb_pvalue = lb_test['lb_pvalue'].iloc[0]
print(f"\nTeste Ljung-Box (lag 10) dos resíduos ao quadrado:")
print(f"Estatística LB(10) = {lb_stat:.3f}, p-valor = {lb_pvalue:.3f}")






