# import tkinter as tk
import csv
import datetime
import os
import platform
import time
import operadora as Ati
from threading import Thread
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from bigdata import CsvFile as Csv
from gui import Application, Widgets, num_brasil, num_usa


class Bigdata:
    def __init__(self, instance):
        '''
        Classe instanciadora e manipuladora dos dados nos arquivos.

        instance - Objeto csv que será manipulado.
        '''
        self.instance = instance
        self.arquivo_csv = ''
        self.arquivo_csv_nome = ''
        self.delimiter = ''
        self.modedict = False
        self.csvfile = None

    def abrir_csv(self, delimiter=';', modedict=True, encoder='utf8'):
        if self.arquivo_csv:
            self.csvfile = Csv(self.arquivo_csv, delimiter=delimiter, modedict=modedict, encoder=encoder)
            self.delimiter = delimiter
            self.modedict = modedict
            self.encoder = encoder
            nome = self.arquivo_csv.split('/')
            self.arquivo_csv_nome = nome[-1]

    def clean(self):
        self.arquivo_csv = ''
        self.arquivo_csv_nome = ''
        self.delimiter = ''
        self.modedict = False
        self.csvfile = None
        
    def exibe_arquivo(self):
        print(self.arquivo_csv)

    def rotina1_mesclar(self):
        pass

# Funções do menu Arquivo
def arquivo_abrir():
    def param():
        def openfile():
            try:
                if len(Text1.get()) == 1:
                    orcsv.arquivo_csv = name
                    separator = Text1.get()
                    encoder = Combo1.get()
                    if separator == 't': separator = '\t'
                    orcsv.abrir_csv(separator, Check1.get(), encoder)
                    mainwindow.root.title('Manipulador de CSV - [' + orcsv.arquivo_csv_nome + ']')
                    mens = 'Foi aberto o arquivo ' + orcsv.arquivo_csv_nome + '.'
                    messagebox.showinfo(title="Arquivo CSV", message=mens)
                    form_selec.destroy()
            except Exception as e: messagebox.showerror(title="Erro ao abrir o arquivo", message=str(e))
            

        dimension = widgets.geometry(230, 320)
        form_setup = {
            'title': 'Abrir arquivo',
            'color': 'aquamarine',
            'dimension': dimension,
        }
        form_selec = mainwindow.form(form_setup)
        wg = Widgets(form_selec, 'aquamarine')
        wg.label('', 5, 0, 0)
        wg.label('', 5, 2, 0)
        wg.label('', 5, 4, 0)
        wg.label('', 5, 6, 0)
        Text1 = wg.textbox('Separador: ', 2, 1, 1, ';')
        Check1 = wg.check('Possui cabeçalho:', 3, 'Sim', 3, 1, selected=True)
        Combo1 = wg.combobox('Regra de codificação: ', 8, ['utf8', 'iso8859'], 5, 1, 'utf8')
        wg.button('Abrir', openfile, 10, 1, 7, 1, 2)

    name = askopenfilename(filetypes=[("Planilhas em CSV", "*.csv"), ("Texto", "*.txt"), ("Todos os arquivos", "*.*")])
    if name:
        param()
    else:
        pass

def arquivo_fechar():
    orcsv.clean()
    mainwindow.root.title('Manipulador de CSV')
    mens = 'O arquivo CSV foi fechado.'
    messagebox.showinfo(title="Arquivo CSV", message=mens)
    
# Funções do menu Funções
def arquivo_geral():
    def sair():
        form_selec.destroy()

    if orcsv.arquivo_csv:
        dimension = widgets.geometry(350, 760)
        form_setup = {
            'title': 'Dados gerais do arquivo csv',
            'color': 'aquamarine',
            'dimension': dimension,
        }
        form_selec = mainwindow.form(form_setup)
        wg = Widgets(form_selec, 'aquamarine')
        wg.label('', 5, 0, 0)
        wg.label('', 5, 6, 0)
        wg.label('Nome do arquivo: ' + orcsv.arquivo_csv , 80, 1, 1, 2)
        wg.label('Qtde de linhas: ' + str(orcsv.csvfile.count), 80, 2, 1, 2)
        wg.label('Qtde de colunas: ' + str(len(orcsv.csvfile.cols)), 80, 3, 1, 2)
        if orcsv.modedict: cabec = 'Sim'
        if not orcsv.modedict: cabec = 'Não'
        wg.label('Possui cabeçalho: ' + cabec, 80, 4, 1, 2)
        if orcsv.modedict:
            cols = []
            for row in orcsv.csvfile.cols: cols.append(row)
            wg.listbox('Cabeçalho: ', 25, 7, cols, 5, 1)
        wg.button('Ok', sair, 16, 1, 7, 1, 2)

def arquivo_modificar():
    def create():
        mantem = []
        novos = []
        _filtro = {}
        for row in combolist:
            if combolist[row][1] == 'Sim':
                if orcsv.modedict: mantem.append(combolist[row][0])
                if not orcsv.modedict: mantem.append(int(combolist[row][0]))
                novos.append(combolist[row][2])
                if combolist[row][3]:
                    _filtro[combolist[row][0]] = combolist[row][3]
        path = orcsv.arquivo_csv[0:len(orcsv.arquivo_csv) - len(orcsv.arquivo_csv_nome)] + newfile.get()
        # resp = orcsv.csvfile.manipula(path, mantem, novos)
        if os.path.exists(path):
            mens = 'O arquivo ' + newfile.get() + ' já existe na pasta selecionada. Deseja substituir o arquivo existente?'
            if messagebox.askyesno(title="Atualização de sistema", message=mens):
                os.remove(path)
                #ct_p = ct_progresso=len(pr)
                confirm.configure(state='disabled')
                #new_csv.append(Thread(target=orcsv.csvfile.manipula, args=[path, mantem, novos, _filtro, True, 0]))
                #pr.append(Thread(target=progresso, args=['Gerando: ' + newfile.get() ,'Novo arquivo gerado com sucesso!', form_selec, ct_p, confirm]))
                #new_csv[-1].start()
                #pr[-1].start()
                new_csv = Thread(target=orcsv.csvfile.manipula, args=[path, mantem, novos, _filtro, True, 0])
                pr = Thread(target=progresso, args=['Gerando: ' + newfile.get() ,'Novo arquivo gerado com sucesso!', form_selec, 0, confirm])
                new_csv.start()
                pr.start()
        else:
            '''
            ct_p = ct_progresso=len(pr)
            new_csv.append(
                Thread(
                    target=orcsv.csvfile.manipula, 
                    args=[path, mantem, novos, {}, str(form_selec), ct_p]
                )
            )
            time.sleep(1)
            pr.append(
                Thread(
                    target=progresso, 
                    args=['Gerando: ' + newfile.get() ,'Novo arquivo gerado com sucesso!', str(form_selec), ct_p]
                )
            )
            new_csv[-1].start()
            pr[-1].start()
            '''
            confirm.configure(state='disabled')
            new_csv = Thread(target=orcsv.csvfile.manipula, args=[path, mantem, novos, _filtro, True, 0])
            pr = Thread(target=progresso, args=['Gerando: ' + newfile.get() ,'Novo arquivo gerado com sucesso!', form_selec, 0, confirm])
            new_csv.start()
            pr.start()

    def selec_arq(tipo=None):
        def _init():
            if itemselect.selection():
                for i in itemselect.selection():
                    gridselected = str(itemselect.item(i, 'text'))
            return combolist[int(gridselected)]

        def confirma():
            if itemselect.selection():
                for i in itemselect.selection():
                    gridselected = str(itemselect.item(i, 'text'))
            if manter.get(): manter_r = 'Sim'
            if not manter.get(): manter_r = 'Não'
            filtro_r = ''
            if filtro.get():
                filtro_r = filtro_itens[filtro.get()] + ';' + param.get() 
            combolist[int(gridselected)] = [
                campo_atual.get(),
                manter_r,
                nome.get(),
                filtro_r,
                ''
            ]
            itemselect.delete(*itemselect.get_children())
            for rows in ordlista:
                itemselect.insert('', 'end', text=rows, values=combolist[rows])
            form_selec1.destroy()

        def filtro_cmd(value=None):
            wg1.combobox_return(filtro, opcs)

        selec = _init()
        dimension = widgets.geometry(355, 460)
        form_setup1 = {
            'title': 'Editar campo do arquivo CSV',
            'color': 'light cyan',
            'dimension': dimension,
        }
        form_selec1 = mainwindow.form(form_setup1)
        wg1 = Widgets(form_selec1, 'light cyan')
        wg1.label('', 5, 0, 0)
        wg1.label('', 5, 4, 0)
        wg1.label('', 5, 7, 0)
        wg1.label('', 5, 20, 0)
        campo_atual = wg1.textbox('Campo atual: ', 25, 1, 1, selec[0], show=False)
        if selec[1] == 'Sim': manter = wg1.check('Manter: ', 3, 'Sim', 2, 1, True)
        if selec[1] == 'Não': manter = wg1.check('Manter: ', 3, 'Sim', 2, 1, False)
        nome = wg1.textbox('Nome coluna: ', 25, 3, 1, selec[2])
        filtro_itens = {
            'Igual': '=',
            'Diferente': '!=',
            'Maior': '>',
            'Maior ou igual': '>=',
            'Menor': '<',
            'Menor ou igual': '<=',
            'Entre': '==',
            'Contém': 'in',
            'Não contém': 'not',
        }
        opcs = list(filtro_itens.keys())
        filtro = wg1.combobox('Filtro: ', 13, opcs, 5, 1, '', cmd=filtro_cmd, seek=filtro_cmd)
        param = wg1.textbox('', 20, 6, 1)
        wg1.label('Duplicar coluna', 40, 8, 1, 2)
        n_nome = wg1.textbox('Nova coluna: ', 25, 9, 1)
        n_opcs = [
            'Cadeia de caracteres',
            'Separador/Posição',
        ]
        # Se a regra for Cadeia de caracteres. Exemplos: '0-4;6-10' (Os trechos serão concatenados.)
        # Se a regra for Separador/Posição. Exemplos: ' ;1;2' (Primeiro item caractere, pode ser (;), depois itens que entram)
        n_regra = wg1.combobox('Regra: ', 18, n_opcs, 10, 1)
        n_param = wg1.textbox('Parâmetros: ', 20, 11, 1)
        ok = wg1.button('Ok', confirma, 12, 1, 21, 1, 2)
        campo_atual.configure(state='disabled')

    def resp_nao():
        resp(False)

    def resp_sim():
        resp(True)

    def resp(r):
        if r: manter_r = 'Sim'
        if not r: manter_r = 'Não'
        cl = combolist
        for row in cl:
            combolist[row] = [
                cl[row][0],
                manter_r,
                cl[row][2],
                cl[row][3],
                cl[row][4]
            ]
        itemselect.delete(*itemselect.get_children())
        for rows in ordlista:
            itemselect.insert('', 'end', text=rows, values=combolist[rows])

    if orcsv.arquivo_csv:
        #new_csv = []
        #pr = []
        dimension = widgets.geometry(495, 760)
        form_setup = {
            'title': 'Criar cópia modificada do arquivo aberto',
            'color': 'aquamarine',
            'dimension': dimension,
        }
        form_selec = mainwindow.form(form_setup)
        wg = Widgets(form_selec, 'aquamarine')
        wg.label('', 5, 0, 0)
        wg.label('', 5, 2, 0)
        wg.label('', 5, 4, 0)
        wg.label('', 5, 6, 0)
        wg.label('', 5, 8, 0)
        wg.label('Use a tabela abaixo pra configurar sua necessidade:', 60, 1, 1, 2)

        colsf = 'campo', 'manter', 'alterar', 'filtrar', 'duplicar'
        headf = {
            'campo': {'text': 'Campo', 'width': 150},
            'manter': {'text': 'Manter', 'width': 80},
            'alterar': {'text': 'Alterar', 'width': 150},
            'filtrar': {'text': 'Filtrar', 'width': 110},
            'duplicar': {'text': 'Duplicar', 'width': 110},
        }
        combolist = {}
        ordlista = []
        ordem = 0
        for row in orcsv.csvfile.cols:
            ordem += 1
            field = row
            if not orcsv.modedict:
                field = str(int(row) - 1)
            texts = [
                field,
                'Sim',
                field,
                '',
                ''
            ]
            ordlista.append(ordem)
            combolist[ordem] = tuple(texts)
        itemselect = wg.grid(colsf, headf, combolist, ordlista, 12, 3, 1, colspan=2, cmd=selec_arq)
        nome = orcsv.arquivo_csv_nome.split('.')
        if len(nome) == 1:
            nome = orcsv.arquivo_csv_nome + '_novo'
        else:
            nome = '.'.join(nome[:-1]) + '_novo.' + nome[-1]
        sim = wg.button('Sim para todos', resp_sim, 16, 1, 5, 1)
        nao = wg.button('Não para todos', resp_nao, 16, 1, 5, 2)
        newfile = wg.textbox('Novo arquivo: ', 30, 7, 1, nome)
        confirm = wg.button('Criar', create, 16, 1, 9, 1, 2)
        confirm.focus()

def arquivo_mesclar():
    def add():
        new_files = askopenfilename(filetypes=[("Planilhas em CSV", "*.csv"), ("Texto", "*.txt"), ("Todos os arquivos", "*.*")])
        if new_files:
            new_files = new_files.split('/')
            if new_files[-1] in arquivos_mesclar:
                messagebox.showerror('Aviso', 'Você já adicionou esse arquivo!')
            else:
                _files.insert('end', new_files[-1])
                arquivos_mesclar.append(new_files[-1])
                # _remove.configure(state='normal')

    def remove():
        pass

    def selec_arq(tipo=None):
        teste()
    
    def mesclar():
        #fields = ['MonthReference', 'CallDate', 'Duration', 'Phone', 'Price', 'UFSource', 'UFDestination', 'Call_id']
        #dd = '31'
        lista_mesclar = []
        path_mesclar = orcsv.arquivo_csv[:-len(orcsv.arquivo_csv_nome)]
        for row in arquivos_mesclar:
            lista_mesclar.append([path_mesclar + row, orcsv.csvfile.cols, orcsv.csvfile.delimiter])
        orcsv.csvfile.mesclar_arquivos(
            path_mesclar + _newfile.get(),
            lista_mesclar,
            _header2.get().split(';'),
            _delimiter.get()
        )
        messagebox.showinfo('Aviso', 'Arquivo mesclado foi gerado com sucesso!')

    if orcsv.arquivo_csv:
        arquivos_mesclar = []
        dimension = widgets.geometry(300, 650)
        form_setup = {
            'title': 'Mesclar arquivo',
            'color': 'aquamarine',
            'dimension': dimension,
        }
        form_selec = mainwindow.form(form_setup)
        wg = Widgets(form_selec, 'aquamarine')
        wg.label('', 5, 0, 0)
        wg.label('', 5, 2, 0)
        wg.label('', 5, 8, 0)
        wg.label('', 70, 1, 1, colspan=2)
        wg.label('\n' * 13, 5, 1, 0, rowspan=8)
        _add = wg.button('Adicionar arquivo', add, 16, 1, 1, 1)
        _remove = wg.button('Remover arquivo', remove, 16, 1, 1, 2)
        _files = wg.listbox('Arquivos', 16, 3, [], 3, 1, selec_arq)
        _header1 = wg.textbox('Cabeçalho atual: ', 45, 4, 1, ';'.join(orcsv.csvfile.cols))
        _header2 = wg.textbox('Novo cabeçalho: ', 45, 5, 1, ';'.join(orcsv.csvfile.cols))
        _delimiter = wg.textbox('Novo delimitador: ', 2, 6, 1, orcsv.csvfile.delimiter)
        newname = orcsv.arquivo_csv_nome.split('.')
        if len(newname) == 1:
            newname = orcsv.arquivo_csv_nome + '_novo'
        else:
            newname = '.'.join(newname[:-1]) + '_novo.' + newname[-1]
        _newfile = wg.textbox('Nome do novo arquivo: ', 40, 7, 1, newname)
        wg.button('Mesclar', mesclar, 16, 1, 9, 1, 2)
        _files.insert('end', orcsv.arquivo_csv_nome)
        arquivos_mesclar.append(orcsv.arquivo_csv_nome)
        _header1.configure(state='disabled')
        _remove.configure(state='disabled')
        _add.focus()

def resumo_dinamico():
    def buscar():
        _fields = [
            (_field1.get(), _group1.get()),
            (_field2.get(), _group2.get()),
            (_field3.get(), _group3.get()),
        ]
        inicio = datetime.datetime.now()
        if platform.system() == 'Windows':
            f = open(orcsv.arquivo_csv, newline='', encoding=orcsv.encoder)
        else:
            f = open(orcsv.arquivo_csv)
        datacsv = csv.DictReader(f, delimiter=orcsv.delimiter)
        _field_data = {'soma': 0.0, 'media': 0.0, 'minimo': 0.0, 'maximo': 0.0, 'contagem': 0}
        _field_dict = {}
        count = 0
        for row in datacsv:
            for i in _fields:
                if i[0]:
                    if i[0] not in _field_dict.keys():
                        _field_dict[i[0]] = {}
                    if i[1]:
                        agroup = row[i[1]]
                        if agroup not in _field_dict[i[0]].keys():
                            _field_dict[i[0]][agroup] = _field_data.copy()
                    else:
                        agroup = 'Tudo'
                        if agroup not in _field_dict[i[0]].keys():
                            _field_dict[i[0]][agroup] = _field_data.copy()
                    try:
                        _value = float(row[i[0]])
                    except:
                        try:
                            _value = float(num_usa(row[i[0]]))
                        except:
                            _value = 0.0
                    _field_dict[i[0]][agroup]['soma'] += _value
                    if _field_dict[i[0]][agroup]['maximo'] < _value:
                        _field_dict[i[0]][agroup]['maximo'] = _value
                    if _field_dict[i[0]][agroup]['contagem'] == 0:
                        _field_dict[i[0]][agroup]['minimo'] = _value
                    else:
                        if _field_dict[i[0]][agroup]['minimo'] > _value:
                            _field_dict[i[0]][agroup]['minimo'] = _value
                    _field_dict[i[0]][agroup]['contagem'] += 1
                    _field_dict[i[0]][agroup]['media'] = _field_dict[i[0]][agroup]['soma'] / _field_dict[i[0]][agroup]['contagem']
            count += 1
        _list.delete(*_list.get_children())
        combolist.clear()
        ordlist.clear()
        indice = 1
        _f_d_sort = list(_field_dict.keys())
        _f_d_sort.sort()
        for row in _f_d_sort:
            _f_r_sort = list(_field_dict[row].keys())
            _f_r_sort.sort()
            for i in _f_r_sort:
                ordlist.append(str(indice))
                combolist[str(indice)] = (row,
                                    i,
                                    num_brasil(str(round(_field_dict[row][i]['soma'], 2))),
                                    num_brasil(str(round(_field_dict[row][i]['media'], 2))),
                                    num_brasil(str(round(_field_dict[row][i]['maximo'], 2))),
                                    num_brasil(str(round(_field_dict[row][i]['minimo'], 2))),
                                    str(_field_dict[row][i]['contagem']))
                indice += 1
        for rows in ordlist:
            _list.insert('', 'end', text=rows, values=combolist[rows])
        fim = datetime.datetime.now()
        tempo_exec = (fim - inicio).seconds
        messagebox.showinfo('Informação', 'Resumo gerado em ' + str(tempo_exec) + ' segundos.')

    def csv_resumo():
        nome = datetime.datetime.now().strftime('%Y%m%d-%H%M')
        f = open('../' + nome + '.csv', 'w')
        datacsv = csv.DictWriter(f, fieldnames=columns, delimiter=';')
        datacsv.writeheader()
        for row in ordlist:
            ordem = 0
            lista = {}
            for i in columns:
                lista[i] = combolist[row][ordem]
                ordem += 1
            datacsv.writerow(lista)
        messagebox.showinfo('Informação', 'O resumo está gerado!')

    if orcsv.arquivo_csv:
        dimension = widgets.geometry(450, 850)
        form_setup = {
            'title': 'Tabela dinâmica para CSV',
            'color': 'aquamarine',
            'dimension': dimension,
        }
        form_selec = mainwindow.form(form_setup)
        wg = Widgets(form_selec, 'aquamarine')
        wg.label('', 5, 0, 0)
        wg.label('', 5, 2, 0)
        wg.label('', 5, 8, 0)
        wg.label('', 5, 10, 0)
        wg.label('', 20, 1, 1, colspan=2)
        wg.label('\n' * 7, 5, 1, 0, rowspan=4)
        wg.label('Campos', 10, 1, 1, 2)
        wg.label('Agrupador', 10, 1, 3, 2)
        _field1 = wg.combobox('1o campo: ', 10, orcsv.csvfile.cols, 2, 1)
        _field2 = wg.combobox('2o campo: ', 10, orcsv.csvfile.cols, 3, 1)
        _field3 = wg.combobox('3o campo: ', 10, orcsv.csvfile.cols, 4, 1)
        _group1 = wg.combobox('', 10, orcsv.csvfile.cols, 2, 3)
        _group2 = wg.combobox('', 10, orcsv.csvfile.cols, 3, 3)
        _group3 = wg.combobox('', 10, orcsv.csvfile.cols, 4, 3)
        _soma1 = wg.check('', 10, 'Somar', 2, 5)
        _soma2 = wg.check('', 10, 'Somar', 3, 5)
        _soma3 = wg.check('', 10, 'Somar', 4, 5)
        wg.button('Buscar dados', buscar, 16, 1, 9, 1, 3)
        wg.button('CSV do resumo', csv_resumo, 16, 1, 9, 4, 3)

        columns = 'item', 'grupo', 'soma', 'media', 'maximo', 'minimo', 'contagem'
        headers = {
            'item': {'text': 'Item', 'width': 120},
            'grupo': {'text': 'Grupo', 'width': 120},
            'soma': {'text': 'Soma', 'anchor': 'e', 'format': 'float', 'width': 100},
            'media': {'text': 'Média', 'anchor': 'e', 'format': 'float', 'width': 90},
            'maximo': {'text': 'Máximo', 'anchor': 'e', 'format': 'float', 'width': 80},
            'minimo': {'text': 'Mínimo', 'anchor': 'e', 'format': 'float', 'width': 80},
            'contagem': {'text': 'Contagem', 'anchor': 'e', 'format': 'float', 'width': 85},
        }
        combolist = {}
        ordlist = []

        _list = wg.grid(columns, headers, combolist, ordlist, 8, 11, 1, colspan=6)
        #_soma1 = wg.label('Item 1\nSoma: 0,00 - Méd: 0,00 - Mín: 0,00 - Máx: 0,00 - Cont: 0,00', 80, 11, 1, 6)
        #_soma2 = wg.label('Item 2\nSoma: 0,00 - Méd: 0,00 - Mín: 0,00 - Máx: 0,00 - Cont: 0,00', 80, 12, 1, 6)
        #_soma3 = wg.label('Item 3\nSoma: 0,00 - Méd: 0,00 - Mín: 0,00 - Máx: 0,00 - Cont: 0,00', 80, 13, 1, 6)
        _field1.focus()

# Relatórios específicos da Ótima Telecom
def otima_invalidos():
    def sair():
        form_selec.destroy()

    def create():
        def generate():
            file_source = 'temp2.csv'
            file_output = path
            if file_output[-4:] != '.csv':
                file_output += '.csv'
            f = open(file_source)
            counts = len(f.readlines())
            f.close()
            if platform.system() == 'Windows':
                data_source = open(file_source, newline='', encoding='utf8')
            else:
                data_source = open(file_source)
            importarcomp = csv.DictReader(data_source.read().splitlines(), delimiter=';')
            with open(file_output, 'w', newline='') as csvfile:
                fieldnames = ['Telefone', 'RN1', 'Operadora']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                count = 0
                lista_fill = []
                orcsv.csvfile.progresso = 0.0
                for row in importarcomp:
                    orcsv.csvfile.progresso = (count / counts) * 100
                    ati_return = Ati.consult_ati(row['Telefone'])
                    if ati_return:
                        if ati_return != ['55000', 'UNKNOWN']:
                            lista_fill.append(
                                {
                                    'Telefone': row['Telefone'],
                                    'RN1': ati_return[0],
                                    'Operadora': ati_return[1],
                                }
                            )
                            count += 1
                writer.writerows(lista_fill)
            data_source.close()
            messagebox.showinfo(title='Aviso', message='Arquivo gerado com sucesso.\nForam analisados ' + str(count) + ' telefones.')
            orcsv.csvfile.progresso = 100.0
            os.remove('temp.csv')
            os.remove('temp2.csv')
            sair()

        if not _fileati.get():
            messagebox.showwarning('Atenção', 'Não foi digitado nenhum nome destino. Será usado relatorio_ati.csv.')
            _fileati.insert(0, 'relatorio_ati.csv')
        gwids = [
            5,
            187,
            273,
        ]
        gwids = [str(x) for x in gwids]
        gwid = 'in'
        for row in gwids:
            gwid += ';' + str(row)
        try:
            # Abrir primeiro temporário - Alterar cabeçalho e selecionar gwids exclusivos
            rows = orcsv.csvfile.manipula('temp.csv', ['callee_id', 'gwid'], ['Telefone', 'GWID'], {'gwid': gwid})
            messagebox.showinfo('Etapa 1', 'Clique ok para iniciar consulta ATI.')
            f = open('temp.csv')
            csvreader = csv.DictReader(f.read().splitlines(), delimiter=';')
            f.close()
            # Etapa 1 - Confirmar existência de arquivo com o mesmo nome.
            path = orcsv.arquivo_csv[0:len(orcsv.arquivo_csv) - len(orcsv.arquivo_csv_nome)] + _fileati.get()
            run = True
            if os.path.exists(path):
                mens = 'O arquivo ' + _fileati.get() + ' já existe na pasta selecionada. Deseja substituir o arquivo existente?'
                if messagebox.askyesno(title="Atualização de sistema", message=mens):
                    os.remove(path)
                else:
                    run = False
            if run:
                # Etapa 2 - Limitar os números a serem consultados.
                # Abrir segundo temporário - adiciona coluna DDD
                with open('temp2.csv', 'w', newline='') as csvfile:
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
                                if len(row['Telefone']) <= 12:
                                    continue
                            row_data = {}
                            for item in csvreader.fieldnames:
                                row_data[item] = row[item]
                            row_data['DDD'] = row['Telefone'][2:4]
                            linha.writerow(row_data)
                            count += 1
                            ddds[ddd] += 1
                # Etapa 3 - Realizar a consulta ATI
                new_csv = Thread(target=generate, args=[])
                pr = Thread(target=progresso, args=['Gerando: ' + _fileati.get() ,'Novo arquivo gerado com sucesso!', form_selec, 0])
                new_csv.start()
                pr.start()
        except:
            messagebox.showerror('Atenção', 'A atividade foi interrompida. Verifique se os dados configurados estão corretos.')

    if orcsv.arquivo_csv:
        dimension = widgets.geometry(210, 760)
        form_setup = {
            'title': 'Selecionar amostras para ATI',
            'color': 'aquamarine',
            'dimension': dimension,
        }
        form_selec = mainwindow.form(form_setup)
        wg = Widgets(form_selec, 'aquamarine')
        wg.label('', 5, 0, 0)
        wg.label('', 5, 6, 0)
        wg.label('Nome do arquivo atual: ' + orcsv.arquivo_csv_nome, 80, 1, 1, 2)
        wg.label('Qtde de linhas: ' + str(orcsv.csvfile.count), 80, 2, 1, 2)
        nome = orcsv.arquivo_csv_nome.split('.')
        if len(nome) == 1:
            nome = orcsv.arquivo_csv_nome + '_ati'
        else:
            nome = '.'.join(nome[:-1]) + '_ati.' + nome[-1]
        nome = nome.replace('-invalids', '')
        _fileati = wg.textbox('Nome do arquivo para ATI: ', 40, 3, 1, nome)
        confirm = wg.button('Gerar', create, 16, 1, 7, 1)
        wg.button('Sair', sair, 16, 1, 7, 2)

def otima_comparacdr():
    def add():
        new_files = askopenfilename(filetypes=[("Planilhas em CSV", "*.csv"), ("Texto", "*.txt"), ("Todos os arquivos", "*.*")])
        if new_files:
            _files.delete(0, 'end')
            _files.insert('end', new_files)

    def csv_resumo():
        nome = datetime.datetime.now().strftime('%Y%m%d-%H%M')
        f = open('../' + nome + '.csv', 'w')
        try:
            fuso = int(_fuso.get())
            orcsv.csvfile.confere_cdr(compara=_files.get(), destino=_newfile.get(), delimiter=_delimiter.get(), fuso_horario=fuso)
            messagebox.showinfo('Informação', 'Arquivo gerado com sucesso!')
        except:
            messagebox.showerror('Aviso', 'Fuso horário não é número!')

    if orcsv.arquivo_csv:
        dimension = widgets.geometry(450, 850)
        form_setup = {
            'title': 'Unir CDR Ótima x CDR Parceiros',
            'color': 'aquamarine',
            'dimension': dimension,
        }
        form_selec = mainwindow.form(form_setup)
        wg = Widgets(form_selec, 'aquamarine')
        wg.label('', 5, 0, 0)
        wg.label('', 5, 2, 0)
        wg.label('', 5, 8, 0)
        wg.label('', 70, 1, 1, colspan=2)
        wg.label('\n' * 13, 5, 1, 0, rowspan=8)
        _add = wg.button('Adicionar CDR parceiro', add, 16, 1, 1, 2)
        _files = wg.textbox('Caminho/arquivo: ', 60, 3, 1, '')
        _delimiter = wg.textbox('Delimitador: ', 2, 4, 1, orcsv.csvfile.delimiter)
        _fuso = wg.textbox('Fuso Horário: ', 2, 5, 1, '0')
        newname = orcsv.arquivo_csv_nome.split('.')
        if len(newname) == 1:
            newname = orcsv.arquivo_csv_nome + '_novo'
        else:
            newname = '.'.join(newname[:-1]) + '_novo.' + newname[-1]
        _newfile = wg.textbox('Nome do novo arquivo: ', 40, 7, 1, newname)
        _generate = wg.button('Gerar CDR mesclado', csv_resumo, 16, 1, 9, 2)
        #wg.button('Mesclar', mesclar, 16, 1, 9, 1, 2)
        #arquivos_mesclar.append(orcsv.arquivo_csv_nome)
        _add.focus()

# Funções diversas
def teste():
    print('Testado!')

def progresso(titulo, mensagem, inst, qt, wgd=None):
    dimension = widgets.geometry(80, 300)
    form_setup = {
        'title': titulo,
        'color': 'aquamarine',
        'dimension': dimension,
    }
    form_progr = mainwindow.form(form_setup)
    wg = Widgets(form_progr, 'aquamarine')
    wg.label('', 5, 0, 0)
    wg.label('Progresso: ', 15, 1, 1)
    Progresso = wg.progressbar(200, 2, 1)
    '''
    print(orcsv.csvfile.progresso)
    print(Progresso['value'])
    while Progresso['value'] < 99.0:
        Progresso['value'] = orcsv.csvfile.progresso[inst][qt]
    '''
    orcsv.csvfile.progresso = 0.0
    while not orcsv.csvfile.progresso == 100.0:
        Progresso['value'] = orcsv.csvfile.progresso
    Progresso['value'] = 100.0
    messagebox.showinfo('Processo concluído', mensagem)
    orcsv.csvfile.progresso == 0.0
    form_progr.destroy()
    if wgd:
        wgd.configure(state='active')
        wgd.focus()
    

if __name__ == '__main__':
    items = {
        'title': 'Manipulador de CSV',
        'backcolor': 'medium aquamarine',
        'geometry': '960x600+30+30'
    }
    menus = [
        # menus
        {'title': 'Arquivo'},
        {'title': 'Funções'},
        {'title': 'Ótima'},
        {'title': 'Ajuda'},
        # submenus
        # não há
    ]

    opcs = [
        {'title': 'Cadastros', 'menu': 0},
        {'root': 0, 'title': 'Abrir arquivo CSV ...', 'command': arquivo_abrir},
        {'root': 0, 'title': 'Fechar arquivo atual', 'command': arquivo_fechar},
        {'title': 'Funções', 'menu': 1},
        {'root': 1, 'title': 'Dados gerais ...', 'command': arquivo_geral},
        {'root': 1, 'title': 'Modificar estrutura ...', 'command': arquivo_modificar},
        {'root': 1, 'title': 'Mesclar arquivos ...', 'command': arquivo_mesclar},
        {'root': 1, 'title': 'Resumo dinâmico ...', 'command': resumo_dinamico},
        {'title': 'Ótima', 'menu': 2},
        {'root': 2, 'title': 'Inválidos para ATI ...', 'command': otima_invalidos},
        {'root': 2, 'title': 'Unir CDRs ...', 'command': otima_comparacdr},
        {'title': 'Ajuda', 'menu': 3},
        {'root': 3, 'title': 'Sobre ...', 'command': teste},
    ]

    mainwindow = Application(items)
    mainwindow.menu(menus, opcs)
    widgets = Widgets(mainwindow.root)
    orcsv = Bigdata(mainwindow)
    mainwindow.mainwindow()
