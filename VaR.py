import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Asset and its weight
asset = 'BOVA11.SA'
weight = 1.0  # Since there's only one asset, the weight is 1

start = '2015-05-05'
asset_data = yf.download(asset, start=start)['Close']
asset_returns = asset_data.pct_change()

# VaR calculation
confidence_level = 0.95
historical_var = np.nanpercentile(asset_returns, (1-confidence_level)*100)

# Plot
plt.hist(asset_returns, bins=10, density=True, alpha=0.6, color='g', label='Retornos')
plt.axvline(x=historical_var, color='r', linestyle='--', label=f'{confidence_level*100}% VaR')
plt.xlabel('Retornos')
plt.ylabel('Frequência')
plt.legend()
plt.title('Cálculo do Value at Risk (VaR) Histórico para BOVA11.SA')
print(f"VaR histórico a {confidence_level*100}% de confiança: {historical_var:.4f}")
plt.show()
