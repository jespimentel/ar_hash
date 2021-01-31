import os
import glob
import hashlib
from tkinter import filedialog, Tk
from datetime import datetime
from fpdf import FPDF

# Hash MD5
def calcula_md5 (volume_digitalizado):
    md5 = hashlib.md5()
    with open(volume_digitalizado, 'rb') as f:
        while True:
            data = f.read()
            if not data:
                return 0
            md5.update(data)
            return 'MD5:{0}'.format(md5.hexdigest())

# Lista os PDFs da pasta
def lista_pdf(pasta):
    volumes_pdf =[]
    path = pasta + '//*.pdf'
    for pdf in glob.glob(path):
        volumes_pdf.append (pdf)
    return volumes_pdf

# Identifica o nome do arquivo no path
def identifica_nome_arquivo(doc):
    arquivo = doc.split('\\')
    return arquivo[-1]

# Gera o PDF
def gera_pdf (doc_txt, pasta):
    pdf = FPDF()
    pdf.add_page() # adiciona página
    pdf.set_font("Arial", size=12) # configura a fonte
    f = open(doc_txt, 'r')
    for x in f: # insere o texto
        pdf.cell(200, 10, txt = x, ln = 1, align = 'L')
    nome_do_pdf = pasta+'.pdf'
    pdf.output(nome_do_pdf)
    return

# Início do programa
bloco_texto = 'ÁREA REGIONAL DE PIRACICABA\n'
bloco_texto += 'Digitalização de autos - Conferido em: ' + datetime.now().strftime('%d/%m/%Y %H:%M')
bloco_texto += '\n-------------------------------------------------\n\n'

print()
print(bloco_texto)

# Seleciona a pasta
root = Tk()
root.withdraw()
pasta = filedialog.askdirectory()

pdf = lista_pdf (pasta)
linhas = []
for doc in pdf:
    linhas.append (identifica_nome_arquivo(doc) + ' \t\t' + calcula_md5(doc) + '\n')

# Gera o arquivo txt para gravar os hashs
nome_arquivo = pasta + '.txt'
arquivo = open (nome_arquivo, 'w')
arquivo.write(bloco_texto)
for linha in linhas:
    arquivo.writelines(linha)
arquivo.close()

# Gera o PDF com os hashs a partir do arquivo txt
gera_pdf (nome_arquivo, pasta)

print ('Concluído!')