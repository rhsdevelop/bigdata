import csv
from bigdata import CsvFile


def global_cdr():
    fields = ['MonthReference', 'CallDate', 'Duration', 'Phone', 'Price', 'UFSource', 'UFDestination', 'Call_id']
    dd = '31'
    teste = CsvFile('csv/bina/2018_07_' + dd + '.txt', '\t')
    teste.mesclar_arquivos(
        './csv/correta/2018_07_' + dd + '.txt',
        [
            ['./csv/bina/2018_07_' + dd + '.txt', fields, '\t'], 
            ['./csv/outras/2018_07_' + dd + '.txt', fields, '\t'],
        ]
        fields, 
        '\t'
    )

def cdr():
    fields = ['Central', 'Data e Hora', 'Numero', 'Descricao', 'Tipo', 'Falado', 'Bilhetado', 'Tarifa', 'Valor']
    teste = CsvFile('exemplo.csv', ';')
    teste.mesclar_arquivos(
        '2018_07_01-31_acao.csv', 
        ['2018_07_01-20_acao.csv', fields, True, ';'], 
        ['21-31-acao_cdr.csv', fields, True, ';'],
        fields, 
        ';'
    )

def invalidos(origem, destino, tratado):
    data = CsvFile(origem)
    gwids = [
        653,
        673,
        674,
        756,
        786,
        642,
        747,
        748,
        752,
        753,
        754,
        760,
        761,
        763,
        764,
        765,
        766,
        767,
        768,
        769,
        806,
        807,
        808,
        809,
        810,
        811,
        812,
        813,
        814,
        815,
        816,
        817,
        818,
        819,
        820,
        821,
        822,
        823,
        824,
        825,
        826,
        827,
        828,
        829,
        830,
    ]
    gwids = [str(x) for x in gwids]
    gwid = 'in'
    for row in gwids:
        gwid += ';' + str(row) 
    #gwid = {
    #    'gwid': gwids
    #}
    rows = data.manipula(destino, ['callee_id', 'gwid'], ['Telefone', 'GWID'], {'gwid': gwid})
    f = open(destino)
    csvreader = csv.DictReader(f.read().splitlines(), delimiter=';')
    f.close()
    with open(tratado, 'w', newline='') as csvfile:
        nomes = csvreader.fieldnames + ['DDD']
        linha = csv.DictWriter(csvfile, fieldnames=nomes, delimiter=';')
        linha.writeheader()
        count = 0
        ddds = {}
        for row in csvreader:
            ddd = row['Telefone'][2:4]
            if ddd not in ddds:
                ddds[ddd] = 0
            if ddds[ddd] < 100:
                if ddd in ['92', '97']:
                    if row['GWID'] not in ['653', '673', '674', '756', '786']:
                        continue
                else:
                    pass
                row_data = {}
                for item in csvreader.fieldnames:
                    row_data[item] = row[item]
                row_data['DDD'] = row['Telefone'][2:4]
                linha.writerow(row_data)
                count += 1
                ddds[ddd] += 1
    print(rows)

# invalidos('14-08-2018-invalids.csv', '14-08-2018-onlycol.csv', '14-08-2018-tratado.csv')
global_cdr()
