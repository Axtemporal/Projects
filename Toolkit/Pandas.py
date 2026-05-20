
import pandas as pd


import sys

pd.DataFrame()

DF = pd.read_csv()

# pd.read_excel() diversos arquivos legíveis
#delimiter para tratar tabs

type(DF)

DF.to_excel()

DF.tail()
DF.head()
DF.columns
DF.index
DF.info #tamanho, colunas e tipo de dado de cada coluna
df.describe #estatisticas descritivas,colunas n num. tb
df.shape #linhas x colunas
df.lenght #linhas


df.columns[:5] #para a sprimeiras 5
df[df.columns[-5:]] #para as ultimas 5

df[[c for c in df.columns of 'Time' in c]] #pesca coluna com Time no nome

df.selectdtypes('int') 

df['airline'] #busca exatamente a coluna
df[['airline']] # para ter uma dataframe com os dados da coluna 

df.iloc[1,3] #busca por localização, row x column
df.iloc[[5]] # pega a linha 5 e faz dataframe
df.iloc[:, 1] # queremos todas as rows, apenas da primeira coluna


df.loc[:,['airline','Origin',]] #deixa de buscar por numerico, busca por nome
df.loc['airline'] == 'Spirit Air Lines' #booleano, filtra para apenas os que são spirit


#multiplos filtros
df.loc[(df['airline'] =='Spirit') & (df['FlightDate'] == '2021-09-09')]

#inverso de multiplos filtros
df.loc[~((df['airline'] =='Spirit') & (df['FlightDate'] == '2021-09-09'))]



#forma alternativa Query. 
#colunas, pode ser string se colocar em ""
df.query('(dept time > 1130) and (Origin == "GRU")')

# Sumarização

df.['DeptTime'].min()
df.['DeptTime'].max() 
df.['DeptTime'].mean()
df.['DeptTime'].var()
df.['DeptTime'].std() #standard deviation
df.['DeptTime'].count()

df.['DeptTime'].sum() #soma a coluna
df.['DeptTime'].quantile()


# para aplicar multiplas estatisticas
df[['DeptTime´','depdelay']].agg(['mean','min','max'])

#unicos

df['airline'].unique() #valores unicos

df['airline'].nunique() #numero de valores unicos

#rank, shift

df['airline'].rank()

df['airline'].rank(method='dense')
df['airline'].rank(method='first')

#mudar ordem
df[['airline']].shift(1)

# agrupar

df.groupby('airline')['DepDelay']

df.groupby('airline')[['DepDelay']].mean()

df.groupby('airline')[['DepDelay']].agg(['mean','min','max'])

#new coluns

df.assing(novacoluna = valor nova coluna)


#Sorting

df.sort_values(coluna de referencia)
df.sort_values(coluna de referencia, ascending=False)

.sort_index
 

#missing data
df['DeptTime´','depdelay'].isna() #true ou false para valores faltantes
df['DeptTime´','depdelay'].isna().sum() #conta todos

df['DeptTime´','depdelay'].dropna(subset=['depdelay']) #pega linahs com valores faltando nessa col
df['DeptTime´','depdelay'].fillna(0) #preenche valores


#combining data

df1 = df.query('airline == "Southwest"').copy()
df2 = df.query('airline == "Deslta"').copy()

pd.concat([df1,df2], axis=1)

pd.concat

pd.merge(df1,df2, on=['airline'])

pd.merge(df1,df2, left_on=['airline'], right_on=['airline'])
