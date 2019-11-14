import csv

file1 = 'csv/2018_08_20-23_improd.csv'
file2 = 'csv/2018_08_20.csv'
file3 = 'csv/2018_08_20_verificado.csv'
f1 = open(file1)
datacsv1 = csv.DictReader(f1, delimiter=';')
numeros = []
for row in datacsv1:
    numeros.append(
        row['TELEFONE'],
    )
num = set(numeros)
f1.close()

f2 = open(file2)
datacsv2 = csv.DictReader(f2, delimiter=';')
f3 = open(file3, 'w')
fieldnames = ['Data', 'Telefone', 'GWID', 'Falado']
datacsv3 = csv.DictWriter(f3, fieldnames=fieldnames, delimiter=';')
datacsv3.writeheader()
for row in datacsv2:
    if row['Numero'] in num:
        if int(row['Falado']) > 3:
            datacsv3.writerow(
                {
                    'Data': row['Data e Hora'],
                    'Telefone': row['Numero'],
                    'GWID': row['GWID'],
                    'Falado': row['Falado'],
                }
            )
f2.close()
f3.close()