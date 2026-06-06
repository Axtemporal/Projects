'''
Portfolio Optimization Tool
Markowitz mean-variance optimization with Monte Carlo simulation
'''

'''
This tool helps investors optimize their portfolio allocations.
The user inputs the tickers they want to analyze, and based on a 
risk-return backtest, the program identifies the optimal allocation 
by maximizing the Sharpe ratio. It also outputs:
- Normalized price history with best performer highlighted
- Risk vs. Return scatter plot (annualized)
- Markowitz efficient frontier (100,000 simulated portfolios)
- Recommended portfolio allocation pie chart
- Full QuantStats performance reports benchmarked against Ibovespa
'''

!pip install pandas
!pip install numpy
!pip install yfinance
!pip install seaborn
!pip install matplotlib.pyplot
!pip install datetime
!pip install quantstats
!pip install investpy


import pandas as pd
import numpy as np
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import quantstats as qs
import investpy as inv
import logging

lista_tickers = inv.get_stocks_list("brazil")

ativos = list()
n = 0

while n != 'pare':
  n = input('digite o Ticker da ação com letras maiúsculas, seguido do seu número. Digite um por vez, essa mensagem retornará para o próximo ticker, caso deseje parar digite "pare": ')

  if n in lista_tickers:
    print("A ação foi encontrada...")
    print("Adicionando na lista de ações a serem analisadas.")
    n = n+".SA"
    ativos.append(n)
    print("A composição atual de ativos sendo analisados é: ", ativos)
  if n == 'pare':
    print('Seleção finalizada')
  else:
    print("A ação não foi encontrada, verificar digitação do Ticker.")


tickers = ativos
end_time = datetime.datetime.now().strftime("%Y-%m-%d")
stocks = yf.download(tickers, start= '2020-01-01', end= end_time)
stocks.head()

stocks_adj_close = stocks.loc[:, 'Adj Close']
stocks_adj_close_norm = stocks_adj_close / stocks_adj_close.iloc[0,:]

last_day_max_stock = stocks_adj_close_norm.iloc[-1].idxmax()
plt.figure()
ax = stocks_adj_close_norm.plot(figsize=(12, 6))

for line in ax.lines:
    if line.get_label() == last_day_max_stock:
        line.set_linewidth(1.5)
        line.set_color('blue')

last_day_value = stocks_adj_close_norm.iloc[-1][last_day_max_stock]
label_text = f"{last_day_max_stock} ({last_day_value:.2f})"
plt.annotate(label_text, xy=(stocks_adj_close_norm.index[-1], last_day_value),
             xytext=(10, 10), textcoords='offset points',
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.5"))
plt.title('Normalized Adjusted Closing Prices')
plt.xlabel('Date')
plt.ylabel('Normalized Price')
plt.grid(True)
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()
plt.savefig('figure1.png', dpi=300)

stocks_returns = stocks_adj_close_norm.pct_change()
summary_stocks = stocks_returns.describe().T.loc[:,["mean", "std"]]
summary_stocks["mean"] = summary_stocks["mean"] * 252
summary_stocks["std"] = summary_stocks["std"]*np.sqrt(252)

plt.figure(figsize=(12, 8))
plt.scatter(
    x='std',
    y='mean',
    data=summary_stocks,
    s=100,
    c='mediumpurple',
    alpha=0.6,
    edgecolors='k',
)
for i in summary_stocks.index:
    plt.annotate(i, xy=(summary_stocks.loc[i, 'std'] + 0.003, summary_stocks.loc[i, 'mean'] + 0.001), size=12)
plt.xlabel('Annualized Volatility', fontsize=15)
plt.ylabel('Annualized Return', fontsize=15)
plt.title('Risk vs. Return', fontsize=20)
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig('figure3.png', dpi=300)
plt.show()

# Markowitz simulation — 100,000 portfolios
initial_equity = 10000000
num_assets = len(tickers)
num_port = 100000
num_days = len(stocks_adj_close_norm) -1
returns = []
risks = []
sharpe = []
percent = []
all_aloc = []

for i in range(num_port):
    rand_vect = np.random.random(size = num_assets)
    alocation = (rand_vect/rand_vect.sum())*initial_equity
    all_aloc.append(alocation)

    df_port_value = (stocks_adj_close_norm*alocation).sum(axis=1)
    returns_portfolio = df_port_value.pct_change(periods = 1).dropna()

    ret = (df_port_value.iloc[-1]/df_port_value.iloc[0])**(252/num_days) -1
    returns.append(ret)

    risk = returns_portfolio.std() * np.sqrt(252)
    risks.append(risk)
    sharpe.append(ret/risk)
    percentile = np.percentile(a = returns_portfolio, q = 5)
    percent.append(percentile)

dic_ret_risk = {'ret': returns, 'risk': risks, 'sharpe':sharpe, 'alocations': all_aloc, 'percentile': percent }
ret_risk = pd.DataFrame(dic_ret_risk)

coord_max = np.array(sharpe).argmax()
max_sr_risco = risks[coord_max]
max_sr_ret = returns[coord_max]
all_aloc_ret = all_aloc[coord_max]

max_sr_ret,max_sr_risco,all_aloc_ret/100000000

x = risks
y = returns
plt.figure(figsize=(12, 8))
plt.scatter(x,y,c = sharpe, cmap = 'viridis', s = 30)
plt.colorbar(label = 'Sharpe Ratio')
plt.scatter(max_sr_risco,max_sr_ret, c = 'blue',s = 10)
plt.xlabel('Risk')
plt.ylabel('Return')
plt.savefig('figure9.png', dpi=300)
plt.show()

mask01 = ret_risk['ret'] > 0.09
mask02 = ret_risk['risk'] < 0.5
mask = mask01 & mask02
filtered_ret_risk = ret_risk[mask]

allocation_df = pd.DataFrame(filtered_ret_risk['alocations'].values.tolist(), columns=tickers)
mean_allocation = allocation_df.mean() / allocation_df.mean().sum()

plt.figure(figsize=(8, 8))
plt.pie(mean_allocation, labels=tickers, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title('Recommended Portfolio Allocation')
plt.axis('equal')
plt.show()

# QuantStats full reports benchmarked against Ibovespa
import quantstats as qs
import investpy as inv
import datetime

qs.extend_pandas()
end_time2 = datetime.datetime.now().strftime("%d/%m/%Y")

lista_tickers = inv.get_stocks_list("brazil")

ativos = []
n = 0

while n != 'pare':
    n = input('Enter ticker for QuantStats report (uppercase), or "pare" to stop: ')

    if n in lista_tickers:
      n = n.lower() + '.sa'
      print("Ticker found...")
      pergunta = input(f'Generate report for {n}? (sim/não)').lower()
      if pergunta == 'sim':
        try:
            stock = qs.utils.download_returns(n)
            qs.reports.full(stock, "^BVSP", output="output/report_dados.html")
        except Exception as e:
            print(f"Error downloading data for {n}: {e}")
      elif pergunta == 'nao' or pergunta == 'não':
        print(f"Skipping report for {n}.")
      else:
        print("Invalid option. Use 'sim' or 'não'.")
    else:
      if n == 'pare':
        print('## Program terminated ##')
      else:
        print('Ticker not found. Check spelling.')
