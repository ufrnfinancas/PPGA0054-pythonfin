# Ibov dolarizado

import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# dates
start = "2007-01-01"
end = "2024-01-05"

# data
ibov = yf.download('^BVSP', start = start, end = end
                   )['Close']

usdbrl = yf.download('USDBRL=X', start = start, end = end
                   )['Close'] 

# dataframe
ibovdf = pd.DataFrame(ibov)
ibovdf.columns = ['IBOV']

usdbrldf = pd.DataFrame(usdbrl)
usdbrldf.columns = ['USDBRL']

ibovusd = pd.merge(ibovdf, usdbrldf, 
                   left_index = True, right_index = True, how = 'inner')

# dolarizando o ibov
ibovusd['IBOVUSD'] = ibovusd['IBOV'] / ibovusd['USDBRL']

# plot
plt.figure(figsize = (10, 6), dpi = 120)
plt.plot(ibovusd.index, ibovusd['IBOVUSD'], label = 'Ibovespa dolarizado', color = 'green')
plt.xlabel('Data')
plt.ylabel('Ibovespa em Dólar')
plt.title('Ibovespa em Dólar desde ' + start[:4])
plt.legend()
plt.grid(True)
plt.show()

# comparando
fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (6, 6), dpi = 120)

ax1.plot(ibovusd.index, ibovusd['IBOV'], label = 'Ibov em Reais', color = 'green')
ax1.set_xlabel('Data')
ax1.set_ylabel('Valor em Reais')
ax1.set_title('Ibov em Reais')
ax1.grid(True)

ax2.plot(ibovusd.index, ibovusd['IBOVUSD'], label = 'Ibov em Dólar', color = 'blue')
ax2.set_xlabel('Data')
ax2.set_ylabel('Valor em Dólar')
ax2.set_title('Ibov em Dólar')
ax2.grid(True)

plt.tight_layout()
plt.show()