# Dashboard desempenho B3.py


import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


import yfinance as yf

# Defina o ticker e o período desejado
ticker = "^BVSP"  # Ticker para o índice Bovespa
start_date = "2022-01-01"
end_date = "2023-01-01"

# Obtenha os dados utilizando a API do Yahoo Finance
data = yf.download(ticker, start=start_date, end=end_date)


# Visualização simples dos dados
fig = px.line(data, x=data.index, y="Close", title="Desempenho do Índice Bovespa")
fig.show()


# Crie um gráfico de linha para o desempenho do índice Bovespa
fig1 = px.line(data, x=data.index, y="Close", title="Desempenho do Índice Bovespa")

# Crie um gráfico de barras para o volume de negociações do índice Bovespa
fig2 = px.bar(data, x=data.index, y="Volume", title="Volume de Negociações do Índice Bovespa")

# Crie o dashboard combinando os dois gráficos
dashboard = go.Figure()
dashboard.add_trace(fig1.data[0])
dashboard.add_trace(fig2.data[0])

# Personalize o layout do dashboard
dashboard.update_layout(title="Dashboard do Desempenho da Bolsa Brasileira")


dashboard.show()

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf

# Defina o ticker e o período desejado
ticker = "^BVSP"  # Ticker para o índice Bovespa
start_date = "2019-01-01"
end_date = "2023-07-31"

# Obtenha os dados utilizando a API do Yahoo Finance
data = yf.download(ticker, start=start_date, end=end_date)

# Crie o gráfico de desempenho do índice Bovespa (com eixo y à esquerda)
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
fig1.update_layout(title="Desempenho do Índice Bovespa", xaxis_title="Data", yaxis_title="Preço")

# Crie o gráfico de volume de negociações do índice Bovespa (com eixo y à direita)
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=data.index, y=data['Volume'], mode='lines', name='Volume'))
fig2.update_layout(title="Volume de Negociações do Índice Bovespa", xaxis_title="Data", yaxis_title="Volume")

# Combine os dois gráficos em um dashboard utilizando subplots com eixos y independentes
dashboard = go.Figure()
dashboard.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close', yaxis='y'))
dashboard.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume', yaxis='y2'))

# Defina a configuração de eixos para cada gráfico
dashboard.update_layout(
    title="Dashboard do Desempenho da Bolsa Brasileira",
    xaxis_title="Data",
    yaxis=dict(title="Preço", side="left", showline=True),
    yaxis2=dict(title="Volume", side="right", overlaying="y", showline=True)
)

# Exiba o dashboard
dashboard.show()














