# Risco x Retorno

import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ativos = ['PETR4.SA',	'ITUB4.SA',	'BBDC4.SA', 'VALE3.SA',	'ABEV3.SA',	
          'BBAS3.SA',	'B3SA3.SA', 'ITSA4.SA',	'BRFS3.SA',	'GGBR4.SA']

inicio = '2021-01-04'
fim = '2023-12-30'

df = yf.download(ativos, start=inicio, end=fim)['Adj Close']
df.head()
df.tail()
df.plot(figsize=(10,10))
plt.show()

df.iloc[0]
normalizado = df/df.iloc[0]
normalizado.loc['2021-01-04']
normalizado.iloc[-1]
normalizado.plot(figsize=(10,10));
plt.show()

retornos_diarios = df.pct_change()
retornos_diarios.head()
retornos_diarios.dropna(inplace=True)
retornos_diarios
retornos_diarios.plot(figsize=(10,10))
plt.show()

retornos_diarios.std()
volatilidade = pd.DataFrame(retornos_diarios.std(), columns=['Vol'])
volatilidade

retornos_medios = pd.DataFrame(retornos_diarios.mean(), columns=['Retornos'])
retornos_medios

#Juntando dataframes

risco_retorno = pd.concat([retornos_medios,volatilidade], axis=1)
risco_retorno

sns.scatterplot(data=risco_retorno, x='Volatilidade', y='Retorno')
plt.show()

risco_retorno.index

plt.subplots(figsize=(10,8))
sns.scatterplot(data=risco_retorno, x='Vol',  y='Retornos')
for i in range(risco_retorno.shape[0]):
  plt.text(x=risco_retorno.Vol[i], y=risco_retorno.Retornos[i], s=risco_retorno.index[i],
           fontdict=dict(color='red', size=12),
           bbox=dict(facecolor='yellow'))
plt.show()