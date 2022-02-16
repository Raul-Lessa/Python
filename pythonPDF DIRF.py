import csv
from doctest import OutputChecker
from posixpath import split
from tokenize import String
from tracemalloc import start
from typing import ChainMap, Counter
import PyPDF2
import pandas as pd
from tika import parser
import os
import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

os.system('cls' if os.name == 'nt' else 'clear')

# Variaveis globais
folder = "C:\\"

# (0) select file


def select_file():
    filetypes = (
        ('Pdf files', '*.pdf'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    if filename != "":
        showinfo(
            title='Selected File',
            message=filename
        )
        return filename
    return ""


# (1) get name


def PDFextactText(pdf):
    print("Extração texto")
    rawText = parser.from_file(pdf)
    rawList = rawText['content'].splitlines()

    split_list = [i.split() for i in rawList]
    hit = 0
    text_list = []
    pag_list = []
    counter = 0
    for word in split_list:
        counter = counter + 1

        # print(word)
        if hit == 1:
            text_list.append(word[0])
            hit = 0

        if hit == 2:
            hit = 1

        if word == ['CPF', 'Nome', 'Completo']:
            hit = 2

        if word == ['Pág.', '1'] or word == ['Pág.', '2']:
            if word == ['Pág.', '1']:
                pagina = 1
            else:
                pag_list.pop()
                pagina = 2
            pag_list.append(pagina)
    # print(pag_list)
    return text_list, pag_list

# (2) split pdf


def PDFsplit(pdf, start, end, password, id):
    pdf_document = pdf
    pdf = PyPDF2.PdfFileReader(pdf_document)
    pdf_writer = PyPDF2.PdfFileWriter()
    for page in range(start-1, end):
        current_page = pdf.getPage(page)
        pdf_writer.addPage(current_page)

    pdf_writer.encrypt(password)
    with open(f'{folder}\\{id}.pdf', "wb") as out:

        # print(out)
        pdf_writer.write(out)


# (2.1) get password
def getPassword(id):
    # read csv, and split on ";" the line
    csv_file = csv.reader(open(
        'D:\\Temp\\DIRF\\SAVIS\\Senha PDF.csv', "r"), delimiter=";")

    # loop through the csv list
    for row in csv_file:
        # if current rows 2nd value is equal to input, print that row
        if id == row[0]:
            return row[1]
    return ""


# String operations
def left(s, amount):
    return s[:amount]


def right(s, amount):
    return s[-amount:]


def mid(s, offset, amount):
    return s[offset:offset+amount]


def main():
    # Extract Text from PDF
    # pdf file to split
    pdf = "D:\\Temp\\DIRF\\SAVIS\\INFORME RENDIMENTOS PROGRAMA DIRF.pdf"
    global folder
    folder = os.path.dirname(os.path.abspath(pdf))
    print("Realizando leitura do PDF.")
    list_CPF, list_Pags = PDFextactText(pdf)

    id_lista = list_CPF
    pages_lista = list_Pags

    # print(id_lista)
    # print(pages_lista)

    # print(len(id_lista))
    # print(len(pages_lista))

    start = 0
    end = 0
    print("Separando PDF")
    for i in range(len(id_lista)):
        start = end + 1
        end = (start + pages_lista[i]) - 1

        # calling PDFsplit funciton to split PDF
        print(str(id_lista[i]) + ' - ' + str(start) + ' - ' + str(end))
        PDFsplit(pdf, start, end, getPassword(id_lista[i]), id_lista[i])


if __name__ == "__main__":
    # calling the main fucntion
    main()
