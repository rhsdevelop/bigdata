# Executável multiplataforma para extrair informações sobre validade de números.
import csv
import os
import requests
import tkinter as tk
import platform
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

ATI = {
    'host': '186.250.124.72',
    'port': 8007,
    'token': 'uarv5mkoiCHkKMAfYJ3949'
}


def consult_ati(n):
    try:
        headers = {'Authorization': ATI['token']}
        r = requests.get('http://%s:%s/ati/?n=%s' % (ATI['host'], ATI['port'], n), headers=headers)
        if r.status_code == 200:
            res = r.text.split(';')
            if len(res) == 2:
                return res
        return False
    except Exception as e:
        return False

def executa():
    file_source = resp['text']
    file_output = entry1.get()
    if file_source == '<Arquivo>':
        messagebox.showerror(title='Aviso', message='Não foi selecionado um arquivo válido.')
    else:
        if not file_output:
            file_output = 'output.csv'
        if file_output[-4:] != '.csv':
            file_output += '.csv'
        row = file_source.split('/')
        file_output = ('/'.join(row[:-1])) + '/' + file_output
        if platform.system() == 'Windows':
            data_source = open(file_source, newline='')
        else:
            data_source = open(file_source)
        importarcomp = csv.DictReader(data_source.read().splitlines(), delimiter=';')
        with open(file_output, 'w', newline='') as csvfile:
            fieldnames = ['Telefone', 'RN1', 'Operadora']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            ddd = {}
            count = 0
            lista_fill = []
            for row in importarcomp:
                ati_return = consult_ati(row['Telefone'])
                if ati_return:
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
        messagebox.showinfo(title='Aviso', message='Arquivo convertido com sucesso.\nForam analisados ' + str(count) + ' telefones.')

def busca_csv():
    name = askopenfilename(filetypes=[("Planilhas em CSV", "*.csv")])
    if name:
        if os.path.exists(name):
            resp['text'] = name
        else:
            messagebox('Não foi selecionado um arquivo válido.')

if __name__ == '__main__':
    janela = tk.Tk()
    janela.title("Verificar números válidos")
    label = tk.Label(janela, text='', bg='white')
    label1 = tk.Label(janela, text='Clique no botão abaixo e anexe o arquivo CSV')
    label1['bg'] = 'white'
    label1['font'] = 'Arial 14 bold'
    label2 = tk.Label(janela, text='', bg='white')
    busca = tk.Button(janela, text="Buscar arquivo", width=30, command=busca_csv)
    label3 = tk.Label(janela, text='', bg='white')
    resp = tk.Label(janela, text='<Arquivo>', bg='white')
    label4 = tk.Label(janela, text='', bg='white')
    label5 = tk.Label(janela, text='Digite o nome do arquivo de resposta (em branco "output.csv")')
    label5['bg'] = 'white'
    label5['font'] = 'Arial 14 bold'
    label6 = tk.Label(janela, text='', bg='white')
    entry1 = tk.Entry(janela, width=30)
    label7 = tk.Label(janela, text='', bg='white')
    execute = tk.Button(janela, text="Gerar relatório", width=30, command=executa)
    label.pack()
    label1.pack()
    label2.pack()
    busca.pack()
    label3.pack()
    resp.pack()
    label4.pack()
    label5.pack()
    label6.pack()
    entry1.pack()
    label7.pack()
    execute.pack()

    janela["bg"] = "white"
    janela.geometry("660x400+60+60")
    janela.mainloop()
