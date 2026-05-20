'''
Trabalho de Computação 2023.2
Alex Temporal e M.V.
'''

'''
Nesse projeto objetivamos criar uma ferramenta para 
investidores que buscam otimizar suas alocações de portfólio.
Ao longo do código o usuário dirá quais ações ele está 
interessado em investir e a partir de uma análise do desempenho 
da açõa em termos de risco e retorno ao longo de um determinado 
período passado (Backtest) diremos qual é a melhor alocação, em 
termos do portfólio com o melhor índice Sharpe. Além disso, o programa 
retorna o histórico de rentabilidade das ações escolhidas, apontando a 
com maior destaque, um gráfico de risco e retorno dos ativos, um gráfico 
com a simulação de Markovitz com os possíveis portófios (testamos 100.000)
e, por fim, um gráfico com a composição recomendada da carteira.

Além disso, ao final do programa auxiliamos o investidor a entender mais 
sobre os ativos que tem interesse em investir. Através do pacote Quantstats
emitimos relatórios completos com diversos dados sobre o desempenho da empresa. 
Possibilitamos que sejam emitidos relatórios para quantas ações intererssarem o 
usuário

'''

#Instalando pacotes necessários


!pip install pandas
!pip install numpy
!pip install yfinance
!pip install seaborn
!pip install matplotlib.pyplot
!pip install datetime
!pip install quantstats
!pip install investpy


#Importando os pacotes que serão utilizados e escrevendo suas abreviações


import pandas as pd
import numpy as np
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import quantstats as qs
import investpy as inv
import logging

#Aqui entra o input das ações que o usuário deseja analisar

#Item da lista
#Item da lista

# utilizamos uma base de dados do Investing.com com todas as ações listadas para verificar se o ticker inserido existe na bolsa brasileira
lista_tickers = inv.get_stocks_list("brazil")


ativos = list()
n = 0

# Se for digitado pare as adições de ativos no portfólio param
while n != 'pare':

#Input dos tickers, deixando bem claro ao usuário como deve ser feito o processo e o que ele deve digitar se deseja parar
  n = input('digite o Ticker da ação com letras maiúsculas, seguido do seu número. Digite um por vez, essa mensagem retornará para o próximo ticker, caso deseje parar digite "pare": ')


#se a ação estiver na base de dados do Investing.com ...
  if n in lista_tickers:
# Resposta positiva!
    print("A ação foi encontrada...")
    print("Adicionando na lista de ações a serem analisadas.")
    n = n+".SA"
    ativos.append(n)
    print("A composição atual de ativos sendo analisados é: ", ativos)
  if n == 'pare':
 #Resposta de finalização!
    print('Seleção finalizada')
  else:
 #resposta negativa!
    print("A ação não foi encontrada, verificar digitação do Ticker.")


'''
Aqui é por onde coletamos os dados de cotação das 
ações a serem analisadas da base de dados do Yahoo 
Finance, que temos acesso através do pacote Yfinance. 
É importante a verificação que fizemos anteriormente 
pois não pode haver nenhum erro na escrita do ticker, 
senão não aparecerá na análise!

Selecionamos o período 01/01/2020 até o dia que o código 
é rodado, o pacote datetime permite esse luxo a nosso código!
'''


tickers = ativos
end_time = datetime.datetime.now().strftime("%Y-%m-%d")
stocks = yf.download(tickers, start= '2020-01-01', end= end_time)
stocks.head()


'''
Estabelecemos a normalização de que na data de início 
todas as ações possuem o valor de 1 e vão variando a medida 
que suas cotações mudam nos dias de negociação. Chegamos então 
nas variações de rentabilidade delas no período.
'''

stocks_adj_close = stocks.loc[:, 'Adj Close']
stocks_adj_close_norm = stocks_adj_close / stocks_adj_close.iloc[0,:]

'''
O objetivo desse chunk é plotar os retornos diários para melhor 
visualizar o desempenho dos ativos. Lembrando que todos começam e
m 1 no dia 01/01/2020

Para aprofundar a análise, colocamos em azul mais forte a série 
da ação com melhor desempenho
'''

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
plt.title('Preços de Fechamento Ajustados Normalizados')
plt.xlabel('Data')
plt.ylabel('Preços Normalizados')
plt.grid(True)
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()
plt.savefig('figure1.png', dpi=300)



'''
Como prática de mercado, risco tem equivalência a variância dos portfólios, 
isto é, a volatilidade dos ativos no mercado determinam seu risco. Asssim, 
podemos aprofundar nossa análise nos termos de rentabilidade e risco dos ativos 
e, por sua vez, dos possíveis portfólios

'''

stocks_returns = stocks_adj_close_norm.pct_change()
summary_stocks = stocks_returns.describe().T.loc[:,["mean", "std"]]
summary_stocks["mean"] = summary_stocks["mean"] * 252
summary_stocks["std"] = summary_stocks["std"]*np.sqrt(252)


#gráficos com ambos compondo so eixos


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
plt.xlabel('Volatilidade Anualizada', fontsize=15)

plt.ylabel('Retornos Anualizados', fontsize=15)
plt.title('Risco vs. Retorno', fontsize=20)
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig('figure3.png', dpi=300)

plt.show()


'''
Aqui podemos observar a principal ferramenta de 
nosso programa, uma simulação de Markovitz! Através 
de um backtest de portfólios com 100.000 testes, podemos 
encontrar o melhor portfólio dentre todos os testes.

'''

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

    ret = (df_port_value.iloc[-1]/df_port_value.iloc[0])**(252/num_days) -1 # retornos anualizados!
    returns.append(ret)

    risk = returns_portfolio.std() * np.sqrt(252)
    risks.append(risk)
    sharpe.append(ret/risk) # desconsiderando o risk free rate do investimento
    percentile = np.percentile(a = returns_portfolio, q = 5) # value at risk
    percent.append(percentile)


dic_ret_risk = {'ret': returns, 'risk': risks, 'sharpe':sharpe, 'alocations': all_aloc, 'percentile': percent }
ret_risk = pd.DataFrame(dic_ret_risk)

coord_max = np.array(sharpe).argmax()
max_sr_risco = risks[coord_max]
max_sr_ret = returns[coord_max]
all_aloc_ret = all_aloc[coord_max]

max_sr_ret,max_sr_risco,all_aloc_ret/100000000


'''
Aqui plotamos a simulação de Markovitz encontrada

Estabelecemos como o ponto azul o resultado com menor risco e maior retorno

'''


x = risks
y = returns
plt.figure(figsize=(12, 8))
plt.scatter(x,y,c = sharpe, cmap = 'viridis', s = 30)
plt.colorbar(label = 'Sharpe Ratio')

plt.scatter(max_sr_risco,max_sr_ret, c = 'blue',s = 10)
plt.xlabel('Riscos')
plt.ylabel('Retornos')
plt.savefig('figure9.png', dpi=300)

plt.show()


'''
Por fim, ordenamos os portfólios possível em ordem 
de melhor para pior. Dessa forma, o primeiro da lista 
tem a composição com melhor desempenho em termos de seu 
indice de Sharpe no período observadp

A conclusão que podemos observar é que se o período de 
backtest é suficiente para traçar um comportamento de 
risco ponderado segundo os retornos do portfólio, assim, 
sendo possível auxiliar na tomada de decisões

'''


# Filtrar o DataFrame com base na máscara
mask01 = ret_risk['ret'] > 0.09
mask02 = ret_risk['risk'] < 0.5
mask = mask01 & mask02
filtered_ret_risk = ret_risk[mask]

# Obter a alocação recomendada para ativos
allocation_df = pd.DataFrame(filtered_ret_risk['alocations'].values.tolist(), columns=tickers)

# Calcular a média das alocações para cada ativo
mean_allocation = allocation_df.mean() / allocation_df.mean().sum()  # Normalizar para 100%

# Criar um gráfico de pizza para mostrar a alocação recomendada
plt.figure(figsize=(8, 8))
plt.pie(mean_allocation, labels=tickers, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title('Alocação Recomendada para Ativos no Portfólio')
plt.axis('equal')  # Assegura que o gráfico de pizza é desenhado como um círculo.
plt.show()

'''
Aqui trabalhamos o pacote quantstats, com objetivo do investidor obter mais informações dos ativos que ele possui interesse, por meio de um input, onde o usuário, colocará o ticker da ação que ele deseja receber relatório. Utilizamos o Ibovespa como o benchmark. Os gráficos apresentados são:

1.Cumulative Returns vs Benchmark (Ibovespa)
2.Cumulative returns vs Benchmark (Ibovespa), log-scale
3.Cumulative returns vs Benchmark (Ibovespa), volatility matched
4.EOY Returns vs Benchmark
5.Distribution of Monthly Returns
6.Daily Active Returns
7.Rolling Beta to Benchmark
8.Rolling Volatility (6-months)
9.Rolling Sharpe (6-months)
10.Rolling Sortino (6-months)
11.Strategy - Worst 5 Drawdown Periods
12.Underwater Plot
13.Strategy - Monthly Active Returns (%)
14.Strategy - Return Quantiles

'''

import quantstats as qs
import investpy as inv
import datetime

qs.extend_pandas()
end_time2 = datetime.datetime.now().strftime("%d/%m/%Y")


# Obter a lista de tickers do mercado brasileiro
lista_tickers = inv.get_stocks_list("brazil")

# Selecionar ativos para análise
ativos = []
n = 0

while n != 'pare':
    n = input('Para obter relatórios sobre o desempenho de uma ação, digite o Ticker com letras maiúsculas, seguido do seu número. Digite um por vez, essa mensagem retornará novamente após emitir o relatório. Caso deseje parar digite "pare": ')

    if n in lista_tickers:
      n = n.lower() + '.sa'
      print("A ação foi encontrada...")
      pergunta = input(f'Você deseja receber o relatório para {n}? (Digite sim ou não)').lower()
      if pergunta == 'sim':
        # Tentar baixar os dados de preços para o ativo
        try:
            stock = qs.utils.download_returns(n)
            qs.reports.full(stock, "^BVSP",output = "output/report_dados.html")
        except Exception as e:
            print(f"Erro ao baixar dados para {n}: {e}")
      elif pergunta == 'nao' or pergunta == 'não':
        print(f"Relatório para {n} ignorado.")
      else:
        print("Opção inválida. Use 'sim' ou 'não'.")
    else:
      if n == 'pare':
        print('## encerrando programa ##')
      else:
        print('ticker não encontrado')



