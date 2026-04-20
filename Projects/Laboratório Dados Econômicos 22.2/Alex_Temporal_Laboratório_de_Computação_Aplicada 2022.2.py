

# Trabalho de Alex Temporal - Laboratório de Computação Aplicada

# Quais foram as etapas do impacto da Covid e como diferentes áreas da economia reagiram?

#Momento 1: Desaceleração Econômica

# Having fun with data!

# imports
import urllib.request as urlreq
import json
import pandas as pd
import matplotlib.pyplot as plt
#Seaborn é para fazer gráficos melhores (não tem no Spyder mas funciona bem no colab)
import seaborn as sns
sns.set(style="dark")
import numpy as np
from datetime import datetime


#% matplotlib inline

# Ferramenta 1: GET FRED (pega as séries no FRED)
# FRED api documentation - https://research.stlouisfed.org/docs/api/fred/series.html
# api_key and series_id cannot be null

def get_FRED(api_key='b2812b037affbee10b8148d7fe15e552', file_type='json', series_id='', observation_start='', observation_end=''):
    
    # O que faz:
    # ensure series_id is not blank, since it has no default 
    #if series_id != '': 
    
    # set parameter strings, nulls will be not be included
    series_id = '&series_id=' + series_id
    file_type = '&file_type=' + file_type
    api_key = '&api_key=' + api_key
    if observation_start != '': observation_start = '&observation_start=' + observation_start
    if observation_end != '': observation_end = '&observation_end=' + observation_end
    
    # Abre o  url
    url_req_string = 'https://api.stlouisfed.org/fred/series/observations?'+ series_id + api_key + file_type + observation_start + observation_end
    url_response = urlreq.urlopen(url_req_string).read()
    url_data = json.loads(url_response)

    return pd.io.json.json_normalize(url_data, 'observations')

#Ferramenta 2: COMPILE FRED (Lê os dados que foram conseguidos pela função GET FRED)

def compile_FRED(series_names, series_ids, obs_start, obs_end):
  # series_names - a list of human readable terms for the data series (e.g. gdp)
  # series_ids - a list of the FRED ids corresponding to series_names
  # observation_start - formatted as YYYY-MM-DD
  # observation_end - formatted as YYYY-MM-DD
   
  # output is a pandas df joined on observation dates and labeled with series_names
  macro_data = pd.DataFrame()
  
  for i in range(len(series_names)):
    if i == 0: # for the first series, establish dates, all other data series will be joined on these dates
      macro_data['date'], macro_data[series_names[i]] = get_FRED(series_id=series_ids[i], observation_start=obs_start, observation_end=obs_end)['date'], get_FRED(series_id=series_ids[i], observation_start=obs_start, observation_end=obs_end)['value'].astype(float)
  
    else: # for all other dates, get the data and join on first variable dates
      temp_data = pd.DataFrame()
      temp_data['date'], temp_data[series_names[i]] = get_FRED(series_id=series_ids[i], observation_start=obs_start, observation_end=obs_end)['date'], get_FRED(series_id=series_ids[i], observation_start=obs_start, observation_end=obs_end)['value'].astype(float)
      
      macro_data = macro_data.merge(temp_data[['date',series_names[i]]], how='inner', on='date')
      
  #transformo em float no astype(float)
  return macro_data

# Extraindo o CPI:
series_names = ['cpi']
series_ids = ['CPIAUCSL']

US_data = compile_FRED(series_names, series_ids, obs_start = '2016-01-01', obs_end = '2021-07-01')

US_data['cpi inflation rate'] = 100*US_data['cpi'].pct_change() 

US_data = US_data.dropna()
#Tira os valores em A, tira as linhas associadas a observações


#verificando a efetividade
US_data.head()


type(US_data['date'].iloc[0]) #verificando

US_data['datas'] = pd.to_datetime(US_data['date'],format = '%Y-%m-%d')


US_data.set_index('datas', inplace = True)
#deixa as variaveis de data bonitas no gráfico



sns.lineplot(x = US_data.index, y = US_data['cpi inflation rate'])


#A forte desacelaração econômica gerada pelas políticas de lockdown adotadas pelo governo americano geraram desaceleração na economia que pode ser observado atravéz do Índicie de Preços aos Consumidores dos Estados Unidos, o CPI.

#A escolha por iniciar a análise pela inflação se deu por conta da relevância dessa variável na definição de outros indicadores macroeconômicos

#Nota-se uma forte mudança no comportamento dos consumidores ao analisarmos o uso de crédito:


series_names = ['Consumer Loans (US$ Billons)']
series_ids = ['CCLACBW027SBOG']
US_data = compile_FRED(series_names, series_ids, obs_start = '2016-01-01', obs_end = '2022-10-26')
US_data['Consumer Loans (US$ Billons)'] = 100*US_data['Consumer Loans (US$ Billons)'].pct_change()
US_data = US_data.dropna()

type(US_data['date'].iloc[0])


US_data['datas'] = pd.to_datetime(US_data['date'],format = '%Y-%m-%d')


US_data.set_index('datas', inplace = True)


sns.lineplot(x = US_data.index, y = US_data['Consumer Loans (US$ Billons)'])


#Do outro lado da balança, a diminuição do consumo se tornou uma grande preoucpação dos prestadores de serviços e da indústria pois a redução dos rendimentos pode significar a insolvência e inadimplência por conta da inviabilidade do negócio naquele momento.

#Sem dúvidas muitos tiveram que fechar as portas. Uma medida tomada foi a tomada de crédito para financiar suas operações a fim de não falirem:


series_names = ['Commercial and Industrial Loans (US$ Billons)']
series_ids = ['TOTCI']
US_data = compile_FRED(series_names, series_ids, obs_start = '2016-07-24', obs_end = '2022-10-26')
US_data['Commercial and Industrial Loans (US$ Billons)'] = 100*US_data['Commercial and Industrial Loans (US$ Billons)'].pct_change()
US_data = US_data.dropna()
US_data.head()


type(US_data['date'].iloc[0])


US_data['datas'] = pd.to_datetime(US_data['date'],format = '%Y-%m-%d')


US_data.set_index('datas', inplace = True)


sns.lineplot(x = US_data.index, y = US_data['Commercial and Industrial Loans (US$ Billons)'])



#Partindo da análise microeconômica sobre o consumidor, constata-se que existe aversão ao risco, que tornou-se forte durante a pandemia devido às incertezas que todas as mudanças repentina geraram.

#As incertezas por conta do desconhecimento acerca do vírus possuiam notória importância, entretanto, para o mercado as incertezas foram marcantes quanto á atuação dos governos, o que pode ser observado no Global Economic Policy Uncertainty Index, o índicie que mede a incerteza quanto à atuação da politica econômica, isto é, politica fiscal, monetária, cambial e de renda.


series_names = ['Global Economic Policy Uncertainty Index']
series_ids = ['GEPUCURRENT']
US_data = compile_FRED(series_names, series_ids, obs_start = '2016-01-01', obs_end = '2022-09-01')
US_data = US_data.dropna()
US_data.head()

type(US_data['date'].iloc[0])


US_data['datas'] = pd.to_datetime(US_data['date'],format = '%Y-%m-%d')

US_data.set_index('datas', inplace = True)

sns.lineplot(x = US_data.index, y = US_data['Global Economic Policy Uncertainty Index'])





# Momento 2: Resposta por meio da Política Econômica

#Após grandes preocupações quanto às ações a serem tomadas pelo FED, no dia 3 de maio de 2020 a diminuição da taxa de juros foi a alternativa mais plausível para combater um possível cenário de recessão dado pela deflação corrente no período

#A renomada economista Claudia Sahm, membra do Board of Directors do FED elaborou um indicador de recessão que é atualmente considerado um importante indicador. A relevância se dá pela capacidade de indicar uma possível recesão muito antes dos metodos tradicionais

#The empirical results indicated that the exchange rate and money supply ratios were reasons of the increase in inflation

#There is also increasing pressure on the inflation rates due to the domestic money supply and exchange rate



series_names = ['Federal Funds Effective Rate']
series_ids = ['DFF']
US_data = compile_FRED(series_names, series_ids, obs_start = '2017-11-04', obs_end = '2022-10-01') 
US_data = US_data.dropna()
US_data.head()




type(US_data['date'].iloc[0])


US_data['datas'] = pd.to_datetime(US_data['date'],format = '%Y-%m-%d')


US_data.set_index('datas', inplace = True)

sns.lineplot(x = US_data.index, y = US_data['Federal Funds Effective Rate'])




series_names1 = ['Real-time Sahm Rule Recession Indicator']
series_ids1 = ['SAHMREALTIME']
US_data1 = compile_FRED(series_names1, series_ids1, obs_start = '1959-12-01', obs_end = '2022-10-01')
US_data1 = US_data1.dropna()
US_data1.head()


US_data1['datas'] = pd.to_datetime(US_data1['date'],format = '%Y-%m-%d')


type(US_data1['date'].iloc[0])

US_data1.set_index('datas', inplace = True)


sns.lineplot(x = US_data1.index, y = US_data1['Real-time Sahm Rule Recession Indicator'])



#Pode-se notar no ano de 2020 uma elevação sem precedentes do indicador. Sendo ele muito relevante para o FED, é possivel notar uma correlação forte entre a diminuição da taxa de juros e o risco de recessão. De certo o reconhecimento do FED de que há a necessidade de agir mostra que um problema é real e deve receber atenção.

#a série em Azul representa a taxa de juros americana e a série laranja representa a Sahm Rule Recession indicator no período.



series_names1 = ['Real-time Sahm Rule Recession Indicator']
series_ids1 = ['SAHMREALTIME']
US_data1 = compile_FRED(series_names1, series_ids1, obs_start = '2017-11-04', obs_end = '2022-10-01')
US_data1 = US_data1.dropna()
US_data1.head()


US_data1['datas'] = pd.to_datetime(US_data1['date'],format = '%Y-%m-%d')


type(US_data1['date'].iloc[0])


US_data1.set_index('datas', inplace = True)

sns.lineplot(x = US_data.index, y = US_data['Federal Funds Effective Rate'])
sns.lineplot(x = US_data1.index, y = US_data1['Real-time Sahm Rule Recession Indicator'])

#É conhecido que uma das ferramentas do banco central para incentivar a economia por meio da redução da taxa de juros é o aumento da oferta monetária. Podemos observar o M1, que constata o papel moeda em poder público e depositos a vista em bancos comerciais, o nível de liquidez da economia.

#A partir do gráfico podemos ver um forte aumento nesse agregado monetário gerado pela injeção monetária do FED na economia


series_names1 = ['M1']
series_ids1 = ['M1SL']
US_data1 = compile_FRED(series_names1, series_ids1, obs_start = '2017-11-04', obs_end = '2022-10-01')
US_data1 = US_data1.dropna()
US_data1.head()

US_data1['datas'] = pd.to_datetime(US_data1['date'],format = '%Y-%m-%d')

type(US_data1['date'].iloc[0])

US_data1.set_index('datas', inplace = True)

sns.lineplot(x = US_data1.index, y = US_data1['M1'])



#Conclusão
#Nota-se que a chegada do covid 19 nos Estados Unidos teve grandes impactos que repercutiram por toda a economia, como observado no momento 1. Em seguida a resposta do FED para esse relevante evento teve grande relevância macroeconômica dada a intensa resposta proferida.

#É essencial pontuar que movimentações similares ocorreram ao redor do mundo pois todos os países apresentaram impactos por conta do covid. Além disso, a relevância do Momento 2 para outras economias ao redor do mundo já que os Estados Unidos possuem grande relevância econômica.











