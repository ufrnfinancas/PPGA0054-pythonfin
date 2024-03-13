# Descriptive statistics
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.2f' % x)
import numpy as np
import datetime
import pandas_datareader.data as web   #pandas-datareader
import yfinance as yf
yf.pdr_override()
import matplotlib.pyplot as plt
from IPython.core.display import display, HTML   #ipython
display(HTML("<style>.container { width:100% !important; }</style>"))
import statsmodels.api as sm

# dates
start = datetime.datetime(2001, 1, 2)
end = datetime.datetime(2023, 10, 9)

## Ibovespa

# fetch
bvsp = web.get_data_yahoo('^BVSP',start,end) 

# specific dates
bvsp.head(3)
bvsp.tail(3)
bvsp.loc['2023-05-22'] 
bvsp.loc['2023-06-01':'2023-06-16'] 

# price plot
bvsp['Adj Close'].plot()
plt.xlabel("Data")
plt.ylabel("Preço ajustado")
plt.title("Ibovespa - Preço")
plt.show()

bvsp_daily_returns = bvsp['Adj Close'].pct_change()
bvsp_monthly_returns = bvsp['Adj Close'].resample('M').ffill().pct_change()

# daily returns plot
fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
ax1.plot(bvsp_daily_returns)
ax1.set_xlabel("Data")
ax1.set_ylabel("Retornos")
ax1.set_title("Ibovespa - Retornos Diários")
plt.show()

# monthly returns plot
fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
ax1.plot(bvsp_monthly_returns)
ax1.set_xlabel("Data")
ax1.set_ylabel("Retornos")  
ax1.set_title("Ibovespa - Retornos mensais")
plt.show()

# histogram
fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
bvsp_daily_returns.plot.hist(bins = 60)
ax1.set_xlabel("Retornos diários")
ax1.set_ylabel("Q")
ax1.set_title("Ibovespa - Retornos Diários")
plt.show()

## Uma ação qualquer

# fetch
acao = web.get_data_yahoo('BRFS3.SA',start,end) 

# specific dates
acao.head(3)
acao.tail(3)
acao.loc['2023-05-22'] 
acao.loc['2023-06-01':'2023-06-16'] 

# price plot
acao['Adj Close'].plot()
plt.xlabel("Data")
plt.ylabel("Preço ajustado")
plt.title("Ação - Preço")
plt.show()

acao_daily_returns = acao['Adj Close'].pct_change()
acao_monthly_returns = acao['Adj Close'].resample('M').ffill().pct_change()

# daily returns plot
fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
ax1.plot(acao_daily_returns)
ax1.set_xlabel("Data")
ax1.set_ylabel("Retornos")
ax1.set_title("Ação - Retornos Diários")
plt.show()

# monthly returns plot
fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
ax1.plot(acao_monthly_returns)
ax1.set_xlabel("Data")
ax1.set_ylabel("Retorno")  
ax1.set_title("Ação - Retornos Mensais")
plt.show()

# histogram
fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
acao_daily_returns.plot.hist(bins = 60)
ax1.set_xlabel("Retornos diários")
ax1.set_ylabel("Q")
ax1.set_title("Ação - Retornos Diários")
plt.show()


## Modelo de fator único (CAPM?)
# dates
start = datetime.datetime(2018, 11, 2)
end = datetime.datetime(2023, 10, 9)

# fetch
bvsp = web.get_data_yahoo('^BVSP',start,end) 
acao = web.get_data_yahoo('BRFS3.SA',start,end)

bvsp_monthly_returns = bvsp['Adj Close'].resample('M').ffill().pct_change()
acao_monthly_returns = acao['Adj Close'].resample('M').ffill().pct_change()

ibovret = bvsp_monthly_returns.fillna(method='ffill')
acaoret = acao_monthly_returns.fillna(method='ffill')
ibovret.shape
acaoret.shape

# Plot
plt.scatter(ibovret, acaoret)
plt.xlabel('Ibovespa')
plt.ylabel('Ação')
plt.title('Scatter Plot Ação x Ibovespa')
plt.show()

# OLS
premio = ibovret - ((1+0.125783)**(1/252)-1)

df = pd.DataFrame({'Acao': acaoret, 'Premio': premio})
df = df.fillna(method='bfill')

# Add a constant (intercept) to the model
Premio = sm.add_constant(df['Premio'])

# Fit the OLS regression model with an intercept
model = sm.OLS(df['Acao'], Premio).fit()

# Print the regression summary
print(model.summary())

# Get the summary table as text
summary_text = model.summary().as_text()
# Create a figure and axis for the text
fig, ax = plt.subplots(figsize=(20, 20))
ax.axis('off')  # Turn off axis
# Display the summary text as a figure
ax.text(0, 0.5, summary_text, fontsize=12, family='monospace')
# Save the figure as an image
plt.show()