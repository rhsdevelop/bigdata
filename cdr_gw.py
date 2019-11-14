from bigdata import CsvFile


teste = CsvFile('20180717003123.csv')
resumo_cdr = teste.copia_cdr_gw('20180717003123_new.csv')
print('  ---  Resumo do CDR  ---')
print('Bilhetado em minutos: ' + '{:8,}'.format(int(resumo_cdr['Bilhetado'] / 60)).replace(',', '.')) 
print('   Falado em minutos: ' + '{:8,}'.format(int(resumo_cdr['Falado'] / 60)).replace(',', '.')) 
_valortot = str(round(resumo_cdr['Valor'], 2)).split('.')
valortot = '{:8,}'.format(int(_valortot[0])).replace(',', '.') + ',' + '{:0<2}'.format(_valortot[1])
print('         Valor em R$: ' + valortot) 
