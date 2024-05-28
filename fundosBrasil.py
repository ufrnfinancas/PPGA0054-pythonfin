# Fundos de Investimento - CVM
'''
PL dos fundos
Variação de cota
Dados de um fundo pelo seu nome
Comparar fundos

- Sites
data.anbima.com.br
maisretorno.com/comparacao-fundos

- Desempenho
https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS

- Cadastral
http://dados.cvm.gov.br/dados/FI/CAD/DADOS

'''
import zipfile
import io # alocar buffer de RAM
import requests # solicitar o arquivo no site
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#%%
# Fetch
arquivo = 'inf_diario_fi_202404.csv'
link = 'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_202404.zip'

r = requests.get(link)
zf = zipfile.ZipFile(io.BytesIO(r.content)) # o arquivo zipado aberto

arquivo_fi = zf.open(arquivo)
linhas = arquivo_fi.readlines()
linhas = [i.strip().decode('ISO-8859-1') for i in linhas]
linhas = [i.split(';') for i in linhas]
linhas[1]

df = pd.DataFrame(linhas, columns = linhas[0])
informes_diarios = df[1:].reset_index()
informes_diarios.dtypes
informes_diarios[['VL_TOTAL','VL_QUOTA','VL_PATRIM_LIQ','CAPTC_DIA', 'RESG_DIA', 'NR_COTST']] = informes_diarios[['VL_TOTAL','VL_QUOTA','VL_PATRIM_LIQ','CAPTC_DIA', 'RESG_DIA', 'NR_COTST']].apply(pd.to_numeric)
informes_diarios.shape
informes_diarios.head()

# Análises
informes_diarios.DT_COMPTC.unique() # achar as datas únicas

#Comparando PL
comparativo = informes_diarios[informes_diarios['DT_COMPTC'] == '2024-04-30']
comparativo
comparativo.sort_values('VL_PATRIM_LIQ').CNPJ_FUNDO.iloc[-1]

# Variação da cota
fundo = informes_diarios[informes_diarios['CNPJ_FUNDO'] == '01.597.187/0001-15']
fundo.VL_QUOTA.plot()
plt.show()

# Agora dados cadastrais
url = 'http://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv'
cadastral = pd.read_csv(url, sep = ';', encoding='ISO-8859-1')
cadastral.shape

# Fundo de maior PL
cadastral[cadastral['CNPJ_FUNDO'] == comparativo.sort_values('VL_PATRIM_LIQ').CNPJ_FUNDO.iloc[-1]]

# Retorna um fundo de acordo com o cnpj
fundoselec = cadastral[cadastral['CNPJ_FUNDO'] == '34.218.740/0001-10']
pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
fundoselec 

# Retorna um (ou mais) fundo(s) de acordo com o nome - trechos do nome
#selecao = cadastral[cadastral['DENOM_SOCIAL'].str.contains('ALASKA') & cadastral['GESTOR'].str.contains('ALASKA INVESTIMENTOS LTDA.')] 
selecao = cadastral[cadastral['DENOM_SOCIAL'].str.contains('AVANTGARDE')] 
selecao.CNPJ_FUNDO
selecao.index
selecao.shape
selecao.head()
# Analisando os fundos
fundo_df = pd.DataFrame(columns = ['Fundo', 'Classe', 'PL'])

for cnpj in selecao.CNPJ_FUNDO:
    fundo = cadastral[cadastral['CNPJ_FUNDO'] == cnpj]
    fundo_df.loc[cnpj] = [fundo['DENOM_SOCIAL'].values[0], fundo['CLASSE'].values[0], fundo['VL_PATRIM_LIQ'].values[0]]

fundo_df
sns.barplot(data=fundo_df, x=fundo_df.index, y=fundo_df.PL)
plt.xticks(rotation=270)
plt.show() 
#%%