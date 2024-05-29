### Box Spread

import matplotlib.pyplot as plt
import numpy as np

# Primeiro um spread de alta com calls

# Dados hipotéticos
st = 32.62
strike_prices = [28.20, 35.45]
call_premiums = [4.95, 0.53]

# Preços para o eixo x (variação no preço do ativo subjacente)
underlying_prices = np.arange(0, 80, 0.5)

# Lucro e Prejuízo para Bull Spread com Calls
bull_profit = np.where(underlying_prices <= strike_prices[0], 0,
                       np.where(underlying_prices <= strike_prices[1] , underlying_prices - strike_prices[0],
                                strike_prices[1] - strike_prices[0]))
bull_profit = bull_profit - call_premiums[0] + call_premiums[1]

# Plotagem do gráfico de lucros e prejuízos da Bull Spread com Calls
plt.figure(figsize=(10, 6))
plt.plot(underlying_prices, bull_profit, label='Bull Spread com Calls', color='green')
plt.xlabel('Preço do Ativo Subjacente')
plt.ylabel('Lucro/Prejuízo')
plt.title('Gráfico de Lucros e Prejuízos - Bull Spread com Calls')
plt.axvline(st, color='black', linestyle='--', linewidth=0.7, label='Spot')
plt.axvline(strike_prices[0], color='red', linestyle='--', linewidth=0.7, label='Strike 1')
plt.axvline(strike_prices[1], color='blue', linestyle='--', linewidth=0.7, label='Strike 2')
plt.legend()
plt.grid(True)
plt.savefig('bull_spread_calls.png')
plt.show()

# Agora um spread de baixa com puts

# Dados hipotéticos
st = 32.62
strike_prices = [28.20, 35.45]
put_premiums = [0.22, 2.93]

# Preços para o eixo x (variação no preço do ativo subjacente)
underlying_prices = np.arange(0, 80, 0.5)

# Lucro e Prejuízo para Bear Spread com Puts
bear_profit = np.where(underlying_prices <= strike_prices[0], strike_prices[1] - strike_prices[0],
                       np.where(underlying_prices <= strike_prices[1] , strike_prices[1]- underlying_prices,
                                0))
bear_profit = bear_profit + put_premiums[0] - put_premiums[1]

# Plotagem do gráfico de lucros e prejuízos da Bear Spread com Puts
plt.figure(figsize=(10, 6))
plt.plot(underlying_prices, bear_profit, label='Bear Spread com Puts', color='green')
plt.xlabel('Preço do Ativo Subjacente')
plt.ylabel('Lucro/Prejuízo')
plt.title('Gráfico de Lucros e Prejuízos - Bear Spread com Puts')
plt.axvline(st, color='black', linestyle='--', linewidth=0.7, label='Spot')
plt.axvline(strike_prices[0], color='red', linestyle='--', linewidth=0.7, label='Strike 1')
plt.axvline(strike_prices[1], color='blue', linestyle='--', linewidth=0.7, label='Strike 2')
plt.legend()
plt.grid(True)
plt.savefig('bear_spread_puts.png')
plt.show()

# Combina o Bull Spread com o Bear Spread e temos o Box Spread
box_profit = bull_profit + bear_profit

# Plotagem do gráfico de lucros e prejuízos da Box Spread
plt.figure(figsize=(10, 6))
plt.plot(underlying_prices, box_profit, label='Box Spread', color='green')
plt.xlabel('Preço do Ativo Subjacente')
plt.ylabel('Lucro/Prejuízo')
plt.title('Gráfico de Lucros e Prejuízos - Box Spread')
plt.axvline(st, color='black', linestyle='--', linewidth=0.7, label='Spot')
plt.axvline(strike_prices[0], color='red', linestyle='--', linewidth=0.7, label='Strike 1')
plt.axvline(strike_prices[1], color='blue', linestyle='--', linewidth=0.7, label='Strike 2')
plt.legend()
plt.grid(True)
plt.savefig('box_spread.png')
plt.show()