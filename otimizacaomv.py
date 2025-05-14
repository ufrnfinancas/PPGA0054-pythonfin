import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import minimize
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configurar style dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Lista das principais ações do Ibovespa (versão reduzida para testes)
ibovespa_tickers = [
    'ABEV3.SA', 'B3SA3.SA', 'BBAS3.SA', 'BBDC4.SA', 'BBSE3.SA', 
    'BEEF3.SA', 'BRAP4.SA', 'BRFS3.SA', 'CCRO3.SA', 'CMIG4.SA', 
    'ELET3.SA', 'ENGI11.SA', 'HYPE3.SA', 'ITSA4.SA', 'ITUB4.SA',
    'LREN3.SA', 'MGLU3.SA', 'PETR3.SA', 'PETR4.SA', 'VALE3.SA',
    'WEGE3.SA', 'RENT3.SA', 'VIVT3.SA'
]

# Período de análise (reduzido para testes)
start_date = datetime.now() - timedelta(days=730)  # 2 anos em vez de 3
end_date = datetime.now()

# Taxa livre de risco (CDI Brasil - aproximação)
RISK_FREE_RATE = 0.12  # 12% ao ano

print("Baixando dados históricos...")
# Baixar dados históricos com tratamento de erro
try:
    data = yf.download(ibovespa_tickers, start=start_date, end=end_date)['Close']
except Exception as e:
    print(f"Erro ao baixar dados: {e}")
    # Fallback para menos ativos se houver erro
    ibovespa_tickers = ibovespa_tickers[:10]
    data = yf.download(ibovespa_tickers, start=start_date, end=end_date)['Close']

# Limpar dados
data = data.dropna(thresh=len(data) * 0.7, axis=1)  # Less strict threshold
data = data.dropna()
print(f"Análise com {len(data.columns)} ações após limpeza dos dados")

# Calcular retornos logarítmicos
returns = np.log(data / data.shift(1)).dropna()

# Calcular estatísticas básicas
mean_returns = returns.mean() * 252  # Anualizado
cov_matrix = returns.cov() * 252  # Anualizado

# Funções otimizadas para cálculo
def portfolio_return(weights, mean_returns):
    """Calcula apenas o retorno do portfólio"""
    return np.sum(mean_returns * weights)

def portfolio_variance(weights, cov_matrix):
    """Calcula apenas a variância do portfólio"""
    return np.dot(weights.T, np.dot(cov_matrix, weights))

def portfolio_volatility(weights, cov_matrix):
    """Calcula apenas a volatilidade do portfólio"""
    return np.sqrt(portfolio_variance(weights, cov_matrix))

def sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate):
    """Calcula o Sharpe ratio"""
    return (portfolio_return(weights, mean_returns) - risk_free_rate) / portfolio_volatility(weights, cov_matrix)

# Funções para otimização (otimizadas)
def negative_sharpe(weights, mean_returns, cov_matrix, risk_free_rate):
    """Função objetivo para maximizar Sharpe ratio"""
    return -sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate)

def minimize_variance(weights, mean_returns, cov_matrix):
    """Função objetivo para minimizar variância"""
    return portfolio_variance(weights, cov_matrix)

def return_constraint(weights, mean_returns, target_return):
    """Restrição de retorno target"""
    return portfolio_return(weights, mean_returns) - target_return

# Configurar otimização
n_assets = len(mean_returns)
bounds = tuple((0, 1) for _ in range(n_assets))
sum_constraint = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}

# Guess inicial: equal weight
x0 = np.array([1. / n_assets] * n_assets)

# 1. Portfolio com máximo Sharpe ratio
print("\nOtimizando portfólio com máximo Sharpe ratio...")
result_sharpe = minimize(negative_sharpe, x0, 
                        args=(mean_returns, cov_matrix, RISK_FREE_RATE),
                        method='SLSQP', bounds=bounds, constraints=sum_constraint,
                        options={'maxiter': 1000, 'ftol': 1e-9})

optimal_weights_sharpe = result_sharpe.x
max_sharpe_return = portfolio_return(optimal_weights_sharpe, mean_returns)
max_sharpe_vol = portfolio_volatility(optimal_weights_sharpe, cov_matrix)
max_sharpe_ratio = sharpe_ratio(optimal_weights_sharpe, mean_returns, cov_matrix, RISK_FREE_RATE)

# 2. Portfolio com mínima variância
print("Otimizando portfólio com mínima variância...")
result_min_var = minimize(minimize_variance, x0, 
                         args=(mean_returns, cov_matrix),
                         method='SLSQP', bounds=bounds, constraints=sum_constraint,
                         options={'maxiter': 1000, 'ftol': 1e-9})

min_var_weights = result_min_var.x
min_var_return = portfolio_return(min_var_weights, mean_returns)
min_var_vol = portfolio_volatility(min_var_weights, cov_matrix)
min_var_sharpe = sharpe_ratio(min_var_weights, mean_returns, cov_matrix, RISK_FREE_RATE)

# 3. Fronteira eficiente (menos pontos para maior velocidade)
print("Calculando fronteira eficiente...")
n_portfolios = 30  # Reduzido para aumentar velocidade
target_returns = np.linspace(min_var_return, max_sharpe_return*1.2, n_portfolios)
frontier_volatilities = np.zeros(n_portfolios)
frontier_weights = np.zeros((n_portfolios, n_assets))

# Otimização vetorizada da fronteira eficiente
for i, target in enumerate(target_returns):
    constraints = [sum_constraint, 
                   {'type': 'eq', 'fun': return_constraint, 'args': (mean_returns, target)}]
    
    result = minimize(minimize_variance, x0, 
                     args=(mean_returns, cov_matrix),
                     method='SLSQP', bounds=bounds, constraints=constraints,
                     options={'maxiter': 1000, 'ftol': 1e-9})
    
    if result.success:
        frontier_volatilities[i] = portfolio_volatility(result.x, cov_matrix)
        frontier_weights[i] = result.x
    else:
        frontier_volatilities[i] = np.nan
        frontier_weights[i] = np.nan

# Plotar resultados
fig = plt.figure(figsize=(16, 12))

# 1. Gráfico da Fronteira Eficiente
ax1 = plt.subplot(2, 3, 1)
valid_points = ~np.isnan(frontier_volatilities)
plt.plot(frontier_volatilities[valid_points], target_returns[valid_points], 
         'b-', linewidth=2, label='Fronteira Eficiente')
plt.scatter(max_sharpe_vol, max_sharpe_return, color='red', s=100, marker='*', 
           label=f'Máximo Sharpe ({max_sharpe_ratio:.3f})')
plt.scatter(min_var_vol, min_var_return, color='green', s=100, marker='o', 
           label='Mínima Variância')

# Adicionar ativos individuais
asset_vols = np.sqrt(np.diag(cov_matrix))
for i, (ret, vol) in enumerate(zip(mean_returns, asset_vols)):
    plt.scatter(vol, ret, alpha=0.6, s=30)

plt.xlabel('Volatilidade (Desvio Padrão)')
plt.ylabel('Retorno Esperado')
plt.title('Fronteira Eficiente - Ibovespa')
plt.legend()
plt.grid(True, alpha=0.3)

# 2. Capital Allocation Line (CAL)
ax2 = plt.subplot(2, 3, 2)
cal_x = np.linspace(0, max_sharpe_vol*1.5, 100)
cal_y = RISK_FREE_RATE + (max_sharpe_return - RISK_FREE_RATE) / max_sharpe_vol * cal_x

plt.plot(frontier_volatilities[valid_points], target_returns[valid_points], 
         'b-', linewidth=2, label='Fronteira Eficiente')
plt.plot(cal_x, cal_y, 'r--', linewidth=2, label='Capital Allocation Line')
plt.scatter(0, RISK_FREE_RATE, color='orange', s=100, marker='D', label='Ativo Livre de Risco')
plt.scatter(max_sharpe_vol, max_sharpe_return, color='red', s=100, marker='*', 
           label='Portfolio Tangente')

plt.xlabel('Volatilidade')
plt.ylabel('Retorno Esperado')
plt.title('Capital Allocation Line')
plt.legend()
plt.grid(True, alpha=0.3)

# 3. Pesos do portfólio com máximo Sharpe ratio
ax3 = plt.subplot(2, 3, 3)
weights_df = pd.DataFrame({'Ativo': data.columns, 'Peso': optimal_weights_sharpe})
weights_df = weights_df.sort_values('Peso', ascending=False).head(8)

plt.bar(range(len(weights_df)), weights_df['Peso'])
plt.xticks(range(len(weights_df)), [a.replace('.SA', '') for a in weights_df['Ativo']], 
           rotation=45, ha='right')
plt.ylabel('Peso no Portfólio')
plt.title('Top 8 Ativos - Portfólio Máximo Sharpe')

# 4. Comparação de métricas
ax4 = plt.subplot(2, 3, 4)
equal_weights = np.array([1/n_assets] * n_assets)
equal_return = portfolio_return(equal_weights, mean_returns)
equal_vol = portfolio_volatility(equal_weights, cov_matrix)
equal_sharpe = sharpe_ratio(equal_weights, mean_returns, cov_matrix, RISK_FREE_RATE)

metrics = pd.DataFrame({
    'Portfolio': ['Máximo Sharpe', 'Mínima Variância', 'Equal Weight'],
    'Retorno (%)': [max_sharpe_return*100, min_var_return*100, equal_return*100],
    'Volatilidade (%)': [max_sharpe_vol*100, min_var_vol*100, equal_vol*100],
    'Sharpe Ratio': [max_sharpe_ratio, min_var_sharpe, equal_sharpe]
})

x = np.arange(len(metrics))
width = 0.25

plt.bar(x - width, metrics['Retorno (%)'], width, label='Retorno (%)', alpha=0.8)
plt.bar(x, metrics['Volatilidade (%)'], width, label='Volatilidade (%)', alpha=0.8)
plt.bar(x + width, metrics['Sharpe Ratio']*10, width, label='Sharpe Ratio (x10)', alpha=0.8)

plt.xlabel('Tipo de Portfolio')
plt.ylabel('Valor')
plt.title('Comparação de Métricas')
plt.xticks(x, metrics['Portfolio'])
plt.legend()

# 5. Heatmap da Matriz de Correlação
ax5 = plt.subplot(2, 3, 5)
correlation_matrix = returns.corr()
top_assets_idx = optimal_weights_sharpe.argsort()[-10:]  # Top 10 por peso
top_assets = [data.columns[i] for i in top_assets_idx]
top_corr = correlation_matrix.loc[top_assets, top_assets]

# Remover .SA dos labels para melhor visualização
labels = [name.replace('.SA', '') for name in top_corr.columns]
sns.heatmap(top_corr, annot=True, cmap='coolwarm', center=0, fmt='.2f',
            square=True, linewidths=0.5, cbar_kws={"shrink": .5},
            xticklabels=labels, yticklabels=labels)
plt.title('Correlação - Top 10 Ativos')

# 6. Análise com diferentes alocações de risco
ax6 = plt.subplot(2, 3, 6)
w_rf = np.linspace(0, 1, 101)
combined_returns = w_rf * RISK_FREE_RATE + (1 - w_rf) * max_sharpe_return
combined_volatilities = (1 - w_rf) * max_sharpe_vol

plt.plot(combined_volatilities, combined_returns, 'g-', linewidth=3, 
         label='Portfolio com Ativo Livre de Risco')
plt.plot(frontier_volatilities[valid_points], target_returns[valid_points], 
         'b--', linewidth=2, alpha=0.7, label='Fronteira sem Ativo Livre')

plt.scatter(0, RISK_FREE_RATE, color='orange', s=100, marker='D', label='Ativo Livre de Risco')
plt.scatter(max_sharpe_vol, max_sharpe_return, color='red', s=100, marker='*', 
           label='Portfolio Tangente')

# Marcar alguns pontos específicos
for rf_alloc in [0.25, 0.5, 0.75]:
    risky_alloc = 1 - rf_alloc
    ret = rf_alloc * RISK_FREE_RATE + risky_alloc * max_sharpe_return
    vol = risky_alloc * max_sharpe_vol
    plt.scatter(vol, ret, s=60, alpha=0.8, label=f'{rf_alloc*100:.0f}% RF')

plt.xlabel('Volatilidade')
plt.ylabel('Retorno Esperado')
plt.title('Capital Allocation Line')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Resumo dos resultados
print("\n" + "="*60)
print("RESUMO DOS RESULTADOS")
print("="*60)
print(f"\nPortfólio com Máximo Sharpe Ratio:")
print(f"  Retorno Esperado: {max_sharpe_return:.2%}")
print(f"  Volatilidade: {max_sharpe_vol:.2%}")
print(f"  Sharpe Ratio: {max_sharpe_ratio:.3f}")

print(f"\nPortfólio com Mínima Variância:")
print(f"  Retorno Esperado: {min_var_return:.2%}")
print(f"  Volatilidade: {min_var_vol:.2%}")
print(f"  Sharpe Ratio: {min_var_sharpe:.3f}")

print(f"\nPortfólio Equally Weighted:")
print(f"  Retorno Esperado: {equal_return:.2%}")
print(f"  Volatilidade: {equal_vol:.2%}")
print(f"  Sharpe Ratio: {equal_sharpe:.3f}")

print(f"\nTaxa Livre de Risco: {RISK_FREE_RATE:.2%}")

# Principais ativos no portfolio ótimo
print(f"\nPesos dos principais ativos (Máximo Sharpe):")
weights_summary = pd.DataFrame({
    'Ativo': [name.replace('.SA', '') for name in data.columns],
    'Peso': optimal_weights_sharpe
}).sort_values('Peso', ascending=False)

for i in range(min(8, len(weights_summary))):
    if weights_summary.iloc[i]['Peso'] > 0.01:  # Apenas pesos > 1%
        print(f"  {weights_summary.iloc[i]['Ativo']}: {weights_summary.iloc[i]['Peso']:.2%}")

# Análise com combinações de ativo livre de risco
print(f"\n" + "="*60)
print("ANÁLISE COM ATIVO LIVRE DE RISCO")
print("="*60)

for rf_alloc in [0.25, 0.5, 0.75]:
    risky_alloc = 1 - rf_alloc
    combined_return = rf_alloc * RISK_FREE_RATE + risky_alloc * max_sharpe_return
    combined_volatility = risky_alloc * max_sharpe_vol
    combined_sharpe = (combined_return - RISK_FREE_RATE) / combined_volatility
    
    print(f"\nPortfólio {rf_alloc*100:.0f}% livre de risco + {risky_alloc*100:.0f}% arriscado:")
    print(f"  Retorno Esperado: {combined_return:.2%}")
    print(f"  Volatilidade: {combined_volatility:.2%}")
    print(f"  Sharpe Ratio: {combined_sharpe:.3f}")

print(f"\nTempo de execução otimizado! ✨")
print("As principais melhorias incluem:")
print("- Funções específicas para cada cálculo")
print("- Menos pontos na fronteira eficiente")
print("- Período de análise reduzido")
print("- Remoção de cálculos desnecessários")