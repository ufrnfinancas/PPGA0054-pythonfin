# Comparativo Selic x Índices

import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import seaborn as sns

def extracao_bcb(codigo, data_inicio, data_fim):
    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json&dataInicial={}&dataFinal={}'.format(codigo, data_inicio, data_fim)
    df = pd.read_json(url)
    df.set_index('data', inplace=True)
    df.index = pd.to_datetime(df.index, dayfirst=True)
    df.columns = ['SELIC']
    df['SELIC'] = df['SELIC']/100
    return df

data_inicio = '01/01/1995'
data_fim = '31/03/2024'
dados=[]
dados = extracao_bcb(4390, data_inicio=data_inicio, data_fim=data_fim)
indices = ['^BVSP']

for i in indices:
    dados[i] = yf.download(i, start='1995-01-01', end='2024-03-31', interval='1mo')['Adj Close'].pct_change()

dados
dados = dados.iloc[1:]
dados = dados + 1
dados.head()

acumulado = dados.cumprod()

plt.figure(figsize=(10,6))
sns.set_style('darkgrid')
sns.set_palette('mako')
plt.title('Ibovespa x Selic')
sns.lineplot(data=acumulado)
plt.show()