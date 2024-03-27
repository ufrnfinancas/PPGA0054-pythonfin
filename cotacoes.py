import yfinance as yf
import matplotlib.pyplot as plt

#%%
# Ativos e Ibovespa
assets = ['ABEV3.SA', 'CIEL3.SA', 'COGN3.SA', 'EGIE3.SA', 'KLBN11.SA', 
          'LWSA3.SA', 'MGLU3.SA', 'MRFG3.SA', 'MULT3.SA', 'PETZ3.SA' ]
ibovdata = ['^BVSP']

start = '2015-01-02'
end = '2024-02-29'

# Coleta de dados
data = yf.download(assets, period = '1d', start = start, end = end)
ibov = yf.download(ibovdata, period = '1d', start = start, end = end)

# Normalizando os preços
datanorm = data['Adj Close']/data['Adj Close'].iloc[0]

# Removendo .SA dos títulos das séries
string_to_remove = '.SA'
datanorm.rename(columns=lambda x: x.replace(string_to_remove, ''), inplace=True)

# Plot

datanorm.plot()
font_type = "Arial"  
font_size = 11
plt.ylabel('Preço')
plt.xlabel('Data')
plt.title('Performance de Ativos 2024.1 - Normalizado')
plt.legend(fontsize = 6)
ibovnorm = ibov['Adj Close']/ibov['Adj Close'].iloc[0]
ibovnorm.plot(label='IBOV', color='yellow')
plt.show()
# %%
