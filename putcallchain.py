#### Chain
import pandas as pd
import requests

### The chain

subjacente = 'PETR4'  

##### Para um vencimento
vencimento = '2024-04-19'      # YYYY-MM-DD
def optionchaindate(subjacente, vencimento):
    url = f'https://opcoes.net.br/listaopcoes/completa?idAcao={subjacente}&listarVencimentos=false&cotacoes=true&vencimentos={vencimento}'
    r = requests.get(url).json()
    x = ([subjacente, vencimento, i[0].split('_')[0], i[2], i[3], i[5], i[8], i[9], i[10]] for i in r['data']['cotacoesOpcoes'])
    return pd.DataFrame(x, columns=['subjacente', 'vencimento', 'ativo', 'tipo', 'modelo', 'strike', 'preco', 'negocios', 'volume'])

chain = optionchaindate(subjacente, vencimento)
chain_filtered = chain[chain['negocios'] >= 10]

# Filter for CALL and PUT options separately
calls = chain_filtered[chain_filtered['tipo'] == 'CALL']
puts = chain_filtered[chain_filtered['tipo'] == 'PUT']
# Merge CALL and PUT options on the 'strike' column
merged_df = pd.merge(calls[['strike', 'ativo']], puts[['strike', 'ativo']], on='strike', suffixes=('_call', '_put'))
# Rename columns for clarity
merged_df.rename(columns={'ativo_call': 'ativo_call', 'ativo_put': 'ativo_put'}, inplace=True)
merged_df['subjacente'] = subjacente
pcpairs = merged_df[['subjacente', 'ativo_call', 'ativo_put', 'strike']]

pclist = pcpairs.values.tolist()
len(pclist)
