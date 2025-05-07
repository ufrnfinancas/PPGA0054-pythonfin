import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Simulação de retornos aleatórios (mercado eficiente)
np.random.seed(42)
n_days = 252 * 5  # 5 anos de pregões
returns = np.random.normal(loc=0.0003, scale=0.02, size=n_days)
dates = pd.date_range(start="2018-01-01", periods=n_days, freq='B')  # dias úteis

# Série de preços a partir dos retornos simulados
price = 100 * (1 + pd.Series(returns, index=dates)).cumprod()

# Estratégia ingênua: comprar se retorno anterior foi positivo
signal = pd.Series(np.where(pd.Series(returns).shift(1) > 0, 1, 0), index=dates)
strategy_returns = signal * returns

# Cálculo dos acumulados
buy_hold = (1 + pd.Series(returns, index=dates)).cumprod()
strategy = (1 + pd.Series(strategy_returns, index=dates)).cumprod()

# Plotando resultados
plt.figure(figsize=(12,6))
plt.plot(buy_hold, label='Buy and Hold', linewidth=2)
plt.plot(strategy, label='Estratégia baseada no retorno anterior', linestyle='--')
plt.title('Simulação: Testando Hipótese de Mercado Eficiente')
plt.xlabel('Data')
plt.ylabel('Valor da carteira (base 1)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
