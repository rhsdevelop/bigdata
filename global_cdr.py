import csv


def global_converte(file, upload=False):
    f = open(file)
    data = csv.reader(f.read().splitlines(), delimiter=self.delimiter)
    f.close()
    fieldnames = ['MonthReference', 'CallDate', 'Duration', 'Phone', 'Price', 'UFSource', 'UFDestination', 'Call_id']
    wcsv = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')
    if self.delfile:
        wcsv.writeheader()
    amount = 0
    for row in data:
        amount += row[9]
        MonthReference = str(row[3])[0:4] + '_' + str(row[3])[5:7]
        CallDate = str(row[3])
        Duration = row[7]
        Phone = row[2][2:]
        Price = row[8]
        UFSource = 'MG'         # se cliente != Global NULL
        UFDestination = import_UF(Phone[0:2])  # se cliente != Global NULL
        Call_id = row[10]
        wcsv.writerow({'MonthReference': MonthReference,
                       'CallDate': CallDate,
                       'Duration': Duration,
                       'Phone': Phone,
                       'Price': Price,
                       'UFSource': UFSource,
                       'UFDestination': UFDestination,
                       'Call_id': Call_id})
    if self.upload:
        ftpfile = self.filename.split('/')
        directory = ftpfile[-3].split('-')
        directory = directory[1] + '_' + directory[0]
        session = ftplib.FTP('tamoios.tiglobalcob.com.br')
        session.connect(port=21222)
        session.login(user='otimatelecom', passwd='Ct9(201opT#@')
        try:
            session.mkd(directory)
        except:
            pass
        file = open(self.filename, 'rb')                                  # file to send
        session.storbinary('STOR ' + directory + '/' + ftpfile[-1], file) # send the file
        file.close()                                    # close file and FTP
        session.quit()
    return round(amount, 2)


def import_UF(value):
    states = {'11': 'SP',
              '12': 'SP',
              '13': 'SP',
              '14': 'SP',
              '15': 'SP',
              '16': 'SP',
              '17': 'SP',
              '18': 'SP',
              '19': 'SP',
              '21': 'RJ',
              '22': 'RJ',
              '24': 'RJ',
              '27': 'ES',
              '28': 'ES',
              '31': 'MG',
              '32': 'MG',
              '33': 'MG',
              '34': 'MG',
              '35': 'MG',
              '37': 'MG',
              '38': 'MG',
              '41': 'PR',
              '42': 'PR',
              '43': 'PR',
              '44': 'PR',
              '45': 'PR',
              '46': 'PR',
              '47': 'SC',
              '48': 'SC',
              '49': 'SC',
              '51': 'RS',
              '53': 'RS',
              '54': 'RS',
              '55': 'RS',
              '61': 'DF',
              '62': 'GO',
              '63': 'TO',
              '64': 'GO',
              '65': 'MT',
              '66': 'MT',
              '67': 'MS',
              '68': 'AC',
              '69': 'RO',
              '71': 'BA',
              '73': 'BA',
              '74': 'BA',
              '75': 'BA',
              '77': 'BA',
              '79': 'SE',
              '81': 'PE',
              '82': 'AL',
              '83': 'PB',
              '84': 'RN',
              '85': 'CE',
              '86': 'PI',
              '87': 'PE',
              '88': 'CE',
              '89': 'PI',
              '91': 'PA',
              '92': 'AM',
              '93': 'PA',
              '94': 'PA',
              '95': 'RR',
              '96': 'AP',
              '97': 'AM',
              '98': 'MA',
              '99': 'MA'
    }
    if value in states.keys():
        return states[value]
    else:
        return ''
