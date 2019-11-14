import argparse
import datetime
import platform
import csv
import os


class CsvFile:
    def __init__(self, origem, delimiter=';', modedict=True, encoder='utf8'):
        self.origem = origem
        self.delimiter = delimiter
        self.modedict = modedict
        self.progresso = 0.0 # {}
        if not self.origem:
            print('Erro: Não foi inserido arquivo de origem!')
        if platform.system() == 'Windows':
            f = open(self.origem, newline='', encoding=encoder)
        else:
            f = open(self.origem)
        if self.modedict:
            self.csvreader = csv.DictReader(f.read().splitlines(), delimiter=self.delimiter)
            self.cols = self.csvreader.fieldnames
        else:
            self.csvreader = csv.reader(f.read().splitlines(), delimiter=self.delimiter)
            for row in self.csvreader:
                cols = row
                break
            col = 1
            newcols = []
            for row in range(len(cols)):
                newcols.append(str(col))
                col += 1
            self.cols = newcols
        f.close()
        if platform.system() == 'Windows':
            f = open(self.origem, newline='', encoding=encoder)
        else:
            f = open(self.origem)
        self.count = len(f.readlines())
        f.close()


    def metodo1(self):
        print('Oba! Dá certo')


    def mesclar_arquivos(self, arquivo='', arquivos=[], novos_campos=[], delimiter=';'):
        '''Une 2 arquivos formato csv.

        arquivo1 e arquivo2 são listas. primeiro item nome do arquivo, segundo item lista de itens
                            e no terceiro item dicionario True ou False.
        novos_campos o usuário deve preencher os campos que ficam no arquivo definitivo.

        Obs: a quantidade e ordem dos fields de arquivos existentes deve ser informada na mesma da
        lista novos_campos para que o preenchimento seja correto.
        '''
        if not arquivo:
            arquivo = 'output.csv'
        csvreader = []
        if arquivos:
            for row in arquivos:
                if platform.system() == 'Windows':
                    f = open(row[0], newline='', encoding='utf8')
                else:
                    f = open(row[0])
                if row[1]:
                    csvreader.append(csv.DictReader(f.read().splitlines(), delimiter=row[2]))
                else:
                    csvreader.append(csv.reader(f.read().splitlines(), delimiter=row[2]))
                f.close()
        with open(arquivo, 'w', newline='') as csvfile:
            fieldnames = novos_campos
            linha = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=delimiter)
            linha.writeheader()
            for row in csvreader:
                for i in row:
                    row_data = {}
                    counter = 0
                    for item in novos_campos:
                        row_data[item] = i[item]
                        counter += 1
                    linha.writerow(row_data)
        return str(counter) + ' registros adicionados ao novo arquivo.'


    def manipula(self, arquivo, mantem=[], nomes=[], filtro={}, inst_progresso=None, ct_progresso=0):
        ''' Constroi um novo arquivo, eliminando colunas e modificando cabeçalhos.
        arquivo = nome do arquivo que será gerado à partir do arquivo original instanciado.
        mantem = colunas da planilha original que são mantidas.
        nomes = nomes que devem ser atribuidos no novo arquivo para as colunas que foram mantidas.
        filtro = filtro que deve ser aplicado no novo arquivo.
            Exemplos de filtro: {'campo': '>;2018-01-01'}
        '''
        if not arquivo:
            arquivo = 'output.csv'
        if os.path.exists(arquivo):
            return False
        else:
            if platform.system() == 'Windows':
                f = open(self.origem, newline='', encoding='utf8')
            else:
                f = open(self.origem)
            if self.modedict:
                csvreader = csv.DictReader(f.read().splitlines(), delimiter=self.delimiter)
            else:
                csvreader = csv.reader(f.read().splitlines(), delimiter=self.delimiter)
            f.close()
            with open(arquivo, 'w', newline='') as csvfile:
                linha = csv.DictWriter(csvfile, fieldnames=nomes, delimiter=self.delimiter)
                linha.writeheader()
                count = 0
                for row in csvreader:
                    if filtro:
                        continua = True
                        for f in filtro:
                            ff = filtro[f].split(';')
                            if ff[0] == '=':
                                if row[f].lower() != ff[1].lower():
                                    continua = False
                            if ff[0] == '!=':
                                if row[f].lower() == ff[1].lower():
                                    continua = False
                            if ff[0] == '>':
                                if row[f].lower() <= ff[1].lower():
                                    continua = False
                            if ff[0] == '>=':
                                if row[f].lower() < ff[1].lower():
                                    continua = False
                            if ff[0] == '<':
                                if row[f].lower() >= ff[1].lower():
                                    continua = False
                            if ff[0] == '<=':
                                if row[f].lower() > ff[1].lower():
                                    continua = False
                            if ff[0] == '==':
                                if row[f].lower() == ff[1].lower():
                                    continua = False
                            if ff[0] == 'in':
                                partial_ff = ff[1:]
                                if len(partial_ff) == 1:
                                    if ff[1].lower() not in row[f].lower():
                                        continua = False
                                else:
                                    if row[f] not in partial_ff:
                                        continua = False
                            if ff[0] == 'not':
                                partial_ff = ff[1:]
                                if len(partial_ff) == 1:
                                    if ff[1].lower() in row[f].lower():
                                        continua = False
                                else:
                                    if row[f] in partial_ff:
                                        continua = False
                        if not continua: continue 
                    row_data = {}
                    counter = 0
                    for item in mantem:
                        row_data[nomes[counter]] = row[item]
                        counter += 1
                    linha.writerow(row_data)
                    count += 1
                    if inst_progresso:
                        '''
                        if inst_progresso not in self.progresso:
                            self.progresso[inst_progresso] = []
                        if len(self.progresso[inst_progresso]) <= ct_progresso:
                            self.progresso[inst_progresso].append(0.0)
                        self.progresso[inst_progresso][ct_progresso] = (count / self.count) * 100
                        '''
                        self.progresso = (count / self.count) * 100
                self.progresso = 100.0
            return str(count) + ' registros adicionados ao novo arquivo.'
     

    def resumo(self, cols_calc={}, cols_criterio=[], cols_exibe=''):
        '''Exibe uma tabela dinâmica do arquivo csv.
        
        cols_calc     : dicionário. usar item de cabeçalho + tipo de cálculo
        cols_critério : se for apresentado somente 1 critério, não precisa colocar em lista.

        retorna lista de dicionários com cada registro consolidado.
        '''
        if type(cols_criterio) is str: cols_criterio = [cols_criterio]
        if not cols_exibe:
            cols_exibe = self.cols
        f = open(self.origem)
        if self.modedict:
            self.csvreader = csv.DictReader(f.read().splitlines(), delimiter=self.delimiter)
            self.cols = self.csvreader.fieldnames
        else:
            self.csvreader = csv.reader(f.read().splitlines(), delimiter=self.delimiter)
        resumo_csv = []
        calculo = []
        groups = []
        group_id = 0
        for row in self.csvreader:
            group = []
            for field in cols_criterio:
                group.append(row[field])
            if group not in groups:
                groups.append(group)
                if cols_calc:
                    calculo.append({})
                    for col in cols_calc:
                        if cols_calc[col] == 'soma':
                            calculo[group_id][col] = 0.0
                        elif cols_calc[col] == 'contador':
                            calculo[group_id][col] = 0
                        group_id += 1
            if cols_calc:
                for field in cols_calc:
                    ind = groups.index(group)
                    try:
                        if cols_calc[field] == 'soma':
                            calculo[ind][field] += float(row[field])
                        elif cols_calc[field] == 'contador':
                            calculo[ind][field] += 1
                    except:
                        # Os números estão em formato br ou coluna informada errada
                        valor_usa = row[field].split(',')
                        valor_usa[0] = valor_usa[0].replace('.', '')
                        valor_usa = '.'.join(valor_usa)
                        if cols_calc[field] == 'soma':
                            calculo[ind][field] += float(valor_usa)
                        elif cols_calc[field] == 'contador':
                            calculo[ind][field] += 1
        new_groups = []
        for row in groups:
            if cols_calc:
                ind = groups.index(row)
                new_calc = []
                for row2 in cols_calc:
                    new_calc.append(calculo[ind][row2])
                new_groups.append(row + new_calc)
            else:
                new_groups.append(row)
        new_groups.sort()
        for row in new_groups:
            new_dict = {}
            counter = 0
            for row2 in cols_criterio:
                new_dict[row2] = row[counter]
                counter += 1
            for row2 in cols_calc:
                new_dict[row2] = row[counter]
                counter += 1
            resumo_csv.append(new_dict)
        f.close()
        return resumo_csv


    '''
    Próximos métodos são específicos à Ótima Telecom.
    '''
    def confere_cdr(self, compara='', destino='', delimiter=';', fuso_horario=0):
        print('Começou a rotina...')
        hour_initial = datetime.datetime.now()
        print(hour_initial.strftime('%d/%m/%Y %H:%M:%S'))
        if not destino:
            destino = 'output.csv'
        f = open(self.origem)
        datacsv = csv.DictReader(f, delimiter=self.delimiter)
        print('Fieldnames: ' + ', '.join(datacsv.fieldnames))
        if 'Numero' in datacsv.fieldnames and compara:
            fones = []
            dict_fones = {}
            count = 0
            counter_perc = {}
            for i in range(10):
                counter_perc[i / 10] = True
            for i in datacsv:
                fones.append(i['Numero'])
            counter = len(fones)
            set_fones = set(fones)
            f.close()
            print('Etapa 1 - Listar números exclusivos: Ok')
            f = open(self.origem)
            datacsv = csv.DictReader(f, delimiter=self.delimiter)
            for i in datacsv:
                if round(count / counter, 1) in counter_perc and counter_perc[round(count / counter, 1)]:
                    print(str(int(round(count / counter, 1) * 100)) + '%')
                    counter_perc[round(count / counter, 1)] = False
                if i['Numero'] not in dict_fones.keys():
                    dict_fones[i['Numero']] = []
                initial_date = datetime.datetime.strptime(i['Data e Hora'], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=fuso_horario * 60 - 10)
                final_date = datetime.datetime.strptime(i['Data e Hora'], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=fuso_horario * 60 + 10)
                dict_fones[i['Numero']].append([
                    initial_date,
                    final_date,
                    i['Bilhetado'],
                    i['Valor']
                ])
                count += 1
            f.close()
            print('100%')
            print('Etapa 2 - Criar dicionário com todos os eventos: Ok')
            for i in range(10):
                counter_perc[i / 10] = True
            f = open(compara)
            fn = open(destino, 'w')
            datacsv = csv.DictReader(f, delimiter=delimiter)
            newcsv = csv.DictWriter(fn, fieldnames=[
                'Numero',
                'Hora_Parc',
                'Volume_Parc',
                'Valor_Parc',
                'Hora_Otima',
                'Volume_Otima',
                'Valor_Otima'
            ], delimiter=self.delimiter)
            newcsv.writeheader()
            for i in datacsv:
                if round(count / counter, 1) in counter_perc and counter_perc[round(count / counter, 1)]:
                    print(str(int(round(count / counter, 1) * 100)) + '%')
                    counter_perc[round(count / counter, 1)] = False
                newline = {}
                newline['Numero'] = i['Numero']
                newline['Hora_Parc'] = i['Data e Hora']
                newline['Volume_Parc'] = i['Bilhetado']
                newline['Valor_Parc'] = i['Valor']
                newline['Hora_Otima'] = ''
                newline['Volume_Otima'] = '0'
                newline['Valor_Otima'] = '0.0'
                if i['Numero'] in set_fones:
                    for row in dict_fones[i['Numero']]:
                        if datetime.datetime.strptime(i['Data e Hora'][0:19], '%Y-%m-%d %H:%M:%S') >= row[0] and datetime.datetime.strptime(i['Data e Hora'][0:19], '%Y-%m-%d %H:%M:%S') <= row[1]:
                            newline['Hora_Otima'] = row[0] + datetime.timedelta(minutes=10)
                            newline['Volume_Otima'] = row[2]
                            newline['Valor_Otima'] = row[3]
                newcsv.writerow(newline)
                count += 1
            f.close()
            fn.close()    
            print('100%')
            print('Etapa 3 - Gerar CDR comparativo: Ok')
            print('Rotina realizada com sucesso.')
            hour_final = datetime.datetime.now()
            print(hour_final.strftime('%d/%m/%Y %H:%M:%S'))
            print((hour_final - hour_initial).seconds)
            return set_fones, dict_fones
        else:
            print(' Algo deu errado! Verifique o cabeçalho do arquivo origem.')


    def copia_cdr_gw(self, destino=''):
        if not destino:
            destino = 'output'
            extension = self.origem.split('.')
            if len(extension) > 1:
                destino += '.' + extension[-1:][0]
        fo = open(self.origem)
        fd = destino
        foi = csv.reader(fo.read().splitlines(), delimiter=self.delimiter)
        fieldnames = [
            'Telefone',
            'Data / Hora',
            'Bilhetado',
            'Falado',
            'Tarifa',
            'Valor Total',
        ]
        bilhetado_acum = 0.0
        falado_acum = 0.0
        valor_acum = 0.0
        linha = []
        for row in foi:
            try:
                falado_acum += float(row[4])
                #if float(row[12]) != 0.0:
                bilhetado_acum += float(row[12])
                #    tarifa = '0.084'
                #    valor = str((float(row[12]) / 60) * 0.084)
                tarifa = row[8] # se tiver if comente essa linha
                valor = row[9] # se tiver if comente essa linha
                valor_acum += float(valor)
                #else:
                #    tarifa = '0.0'
                #    valor = '0.0'
                linha.append(
                    {
                        'Telefone': row[2], 
                        'Data / Hora': row[3],
                        'Bilhetado': row[12],
                        'Falado': row[4],
                        'Tarifa': tarifa,
                        'Valor Total': valor,
                    }
                )
            except:
                pass
        grava_dictcsv(fd, linha)
        resumo = {
            'Bilhetado': bilhetado_acum,
            'Falado': falado_acum,
            'Valor': valor_acum
        }
        return resumo


    def global_converte(self, destino, upload=False):
        f = open(self.origem)
        data = csv.reader(f.read().splitlines(), delimiter=self.delimiter)
        f.close()
        csvfile = open(destino, 'w')
        fieldnames = ['MonthReference', 'CallDate', 'Duration', 'Phone', 'Price', 'UFSource', 'UFDestination', 'Call_id']
        wcsv = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')
        wcsv.writeheader()
        amount = 0.0
        for row in data:
            amount += round(float(row[9]), 3)
            MonthReference = str(row[3])[0:4] + '_' + str(row[3])[5:7]
            CallDate = str(row[3])
            Duration = row[7]
            Phone = row[2][2:]
            Price = round(float(row[9]), 3)
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
        if upload:
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


    def cdr_converte(self, destino):
        '''
        Converte csv gerado na Pulse nova para o formato ADM.

        Profile, Info Gateway
        '''
        f = open(self.origem)
        data = csv.reader(f.read().splitlines(), delimiter=self.delimiter)
        f.close()
        csvfile = open(destino, 'w')
        fieldnames = ['Central', 'Data e Hora', 'Numero', 'Descricao', 'Tipo', 'Falado', 'Bilhetado', 'Tarifa', 'Valor']
        wcsv = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        wcsv.writeheader()
        amount = 0
        for row in data:
            amount += round(float(row[9]), 3)
            Central = row[10] # Profile no cdr saintes
            MonthReference = str(row[3])[0:4] + '_' + str(row[3])[5:7]
            CallDate = str(row[3])
            Description = row[12] # Info gateway no cdr saintes
            if Description == '\\N':
                Description = ''
            if Description:
                if 'movel' in Description.lower():
                    Tipo = 'MOVEL'
                else:
                    Description = 'FIXO BRASIL'
                    Tipo = 'FIXO'
            else:
                Tipo = ''
            Phone = row[2][2:]
            Falado = row[4]
            Bilhetado = row[7]
            Tarifa = row[8]
            Valor = round(float(row[9]), 3)
            wcsv.writerow({'Central': Central,
                           'Data e Hora': CallDate,
                           'Numero': Phone,
                           'Descricao': Description,
                           'Tipo': Tipo,
                           'Falado': Falado,
                           'Bilhetado': Bilhetado,
                           'Tarifa': Tarifa,
                           'Valor': Valor})
        return round(amount, 2)


    def cdr_alterarcoluna(self, destino):
        '''
        def provisória. Ajustar descrição do CDR.

        Profile, Info Gateway
        '''
        f = open(self.origem)
        data = csv.reader(f.read().splitlines(), delimiter=self.delimiter)
        f.close()
        csvfile = open(destino, 'w')
        fieldnames = ['Central', 'Data e Hora', 'Numero', 'Descricao', 'Tipo', 'Falado', 'Bilhetado', 'Tarifa', 'Valor']
        wcsv = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        wcsv.writeheader()
        for row in data:
            if 'movel' not in row[3].lower() and row[3] != '':
                descricao = 'FIXO BRASIL'
            wcsv.writerow({'Central': row[0],
                           'Data e Hora': row[1],
                           'Numero': row[2],
                           'Descricao': descricao,
                           'Tipo': row[4],
                           'Falado': row[5],
                           'Bilhetado': row[6],
                           'Tarifa': row[7],
                           'Valor': row[8]})
        return round(amount, 2)


def grava_dictcsv(arquivo='', dictcsv=[], delimiter=';'):
    if not arquivo:
        arquivo = 'output.csv'
    with open(arquivo, 'w', newline='') as csvfile:
        fieldnames = list(dictcsv[0].keys())
        linha = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=delimiter)
        linha.writeheader()
        linha.writerows(dictcsv)


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Processar arquivos csv.')
    parser.add_argument('origem', metavar='<Origem>', type=str, nargs='+',
                    help='Nome do arquivo original')
    parser.add_argument('destino', metavar='<Destino>', type=str, nargs='+',
                    help='Nome do arquivo que será salvo, ou digite tela, para exibição')
    parser.add_argument('-c', metavar='<Colunas>', type=str, nargs='+',
                    help='Colunas que serão mantidas')
    parser.add_argument('-a', metavar='<Colunas>', type=str, nargs='+',
                    help='Colunas que serão agrupadas para soma')
    #parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                   const=sum, default=max,
    #                   help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args)
    # print(args.accumulate(args.integers))
