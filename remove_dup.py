import csv
import platform

filename = "ot_04-10-02-2019.csv"
if platform.system() == 'Windows':
    f = open(filename, newline='', encoding='utf8')
else:
    f = open(filename)
datacsv = csv.DictReader(f, delimiter=';') # trocar o separador se necessário.
number = {}
for row in datacsv:
    if row['Telefone'] not in number.keys():
        number[row['Telefone']] = [0, 0.0]
    number[row['Telefone']][0] += 1
    number[row['Telefone']][1] += float(row['Custo'].replace(',', '.'))
f.close()
#datacsv = []
order_number = list(number.keys())
order_number.sort()
f = open('analisado.csv', 'w', newline='')
new_data = csv.DictWriter(f, ['Telefone', 'Eventos', 'Bilhetado'], delimiter=';')
new_data.writeheader()
for row in order_number:
    new_data.writerow(
        {
            'Telefone': row,
            'Eventos': number[row][0],
            'Bilhetado': number[row][1],
        }
    )
print("Oba!!! Estou muito feliz. Foi um sucesso!")