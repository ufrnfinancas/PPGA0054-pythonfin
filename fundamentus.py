import fundamentus

dfraw = fundamentus.get_resultado_raw()
dfraw
print(dfraw.columns)

df = fundamentus.get_resultado()
df
print(df.columns)


# 'Cotação', 'P/L', 'P/VP', 'PSR', 'Div.Yield', 'P/Ativo', 'P/Cap.Giro',
#       'P/EBIT', 'P/Ativ Circ.Liq', 'EV/EBIT', 'EV/EBITDA', 'Mrg Ebit',
#       'Mrg. Líq.', 'Liq. Corr.', 'ROIC', 'ROE', 'Liq.2meses', 'Patrim. Líq',
#       'Dív.Brut/ Patrim.', 'Cresc. Rec.5a'],
# 'cotacao', 'pl', 'pvp', 'psr', 'dy', 'pa', 'pcg', 'pebit', 'pacl',
#       'evebit', 'evebitda', 'mrgebit', 'mrgliq', 'roic', 'roe', 'liqc',
#       'liq2m', 'patrliq', 'divbpatr', 'c5y'
