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

# Fetch - MUDAR OS DOIS quando virar o mês
arquivo = 'inf_diario_fi_202504.csv'
link = 'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_202504.zip'

r = requests.get(link)
zf = zipfile.ZipFile(io.BytesIO(r.content))

arquivo_fi = zf.open(arquivo)
linhas = arquivo_fi.readlines()
linhas = [i.strip().decode('ISO-8859-1') for i in linhas]
linhas = [i.split(';') for i in linhas]
df = pd.DataFrame(linhas, columns=linhas[0])
informes_diarios = df[1:].reset_index()
informes_diarios[['VL_TOTAL', 'VL_QUOTA', 'VL_PATRIM_LIQ', 'CAPTC_DIA', 'RESG_DIA', 'NR_COTST']] = informes_diarios[
['VL_TOTAL', 'VL_QUOTA', 'VL_PATRIM_LIQ', 'CAPTC_DIA', 'RESG_DIA', 'NR_COTST']].apply(pd.to_numeric)
# Dados Cadastrais
url = 'http://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv'
cadastral = pd.read_csv(url, sep=';', encoding='ISO-8859-1')
# Filtrar fundos com "quant" na denominação/
selecao = cadastral[cadastral['DENOM_SOCIAL'].str.contains('prev', case=False)]
selecao = selecao[selecao['SIT'] != 'CANCELADA']
# Filtrar dados de fundos selecionados
fundos_selecionados = informes_diarios[informes_diarios['CNPJ_FUNDO_CLASSE'].isin(selecao['CNPJ_FUNDO'])]
# Calcular maiores altas apenas entre fundos selecionados
retornos = fundos_selecionados.pivot(index='DT_COMPTC', columns='CNPJ_FUNDO_CLASSE', values='VL_QUOTA')
retornos = (retornos / retornos.iloc[1] - 1) * 100
maiores_altas = retornos.iloc[-1].sort_values(ascending=False)
# Selecionar as 10 maiores altas
top_10_altas = maiores_altas.head(10)
# Exibir as 10 maiores altas
print("10 Maiores Altas para Fundos com 'quant' na Denominação:")
print(top_10_altas)
# Criar DataFrame com as 10 maiores altas e a denominação social
top_10_df = pd.DataFrame({'CNPJ_FUNDO': top_10_altas.index, 'Retorno (%)': top_10_altas.values})
top_10_df['Denominação Social'] = [cadastral[cadastral['CNPJ_FUNDO'] == cnpj]['DENOM_SOCIAL'].values[0] for cnpj in top_10_df['CNPJ_FUNDO']]
# Indices de 1 a 10
top_10_df.index = range(1, 11)
# Formatar a coluna "Retorno (%)" com duas casas decimais
top_10_df['Retorno (%)'] = top_10_df['Retorno (%)'].round(2)
top_10_df = top_10_df[['Denominação Social', 'Retorno (%)']]

print(top_10_df)