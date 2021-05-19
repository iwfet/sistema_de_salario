from re import T
import time 
import tkinter as tk
from tkinter import Canvas, filedialog
import pandas as pd
import numpy  as np
from openpyxl import *
import Calculo_valores as calc



valor_salario_liquido = []
valor_desconto_inss = []
valor_desconto_irrf = []

root = tk.Tk()

Canvas1 = tk.Canvas(root, width= 300, height= 300, bg='lightsteelblue')
Canvas1.pack()

lb = tk.Label(root,text = "")
lb.place(x=125, y=200)
lb.config(fg="lightsteelblue")
lb["bg"] = "lightsteelblue"

ler = 0  
def mudaTxt():
    lb["text"] = "Gerado"
    lb["fg"] = "white"
    lb["bg"] = "green"
    
    
def getExcel():    
    global ler
    import_file_path = filedialog.askopenfilename()
    ler = pd.read_excel(import_file_path)
    mudaTxt()
    time.sleep(3)
    browseButtonFechar['fg'] = 'red'

    
browseButton_excel = tk.Button(
    text="importe excel file",
    command=getExcel, 
    bg='green', fg='white', font=('helvetica', 12, 'bold'))
Canvas1.create_window(150,150, window=browseButton_excel)

browseButtonFechar = tk.Button(
text="Fechar",
command=root.quit(),
bg='lightsteelblue', fg='lightsteelblue', font=('helvetica', 12, 'bold'))
Canvas1.create_window(150,250, window=browseButtonFechar)



root.mainloop()



for index, linha in ler.iterrows():
    id = linha["Matricula"]
    nome = linha["Nome"]
    Dependentes = linha["Dependentes"]
    Descontos = linha["Desconto"]
    Salario_bruto = linha["Salario"]
    
    desconto_inss = calc.DescontoINSS(Salario_bruto)
    desconto_irrf = calc.DescontoIRRF(Salario_bruto,desconto_inss,Dependentes)
    valor_final = Salario_bruto - desconto_irrf - Descontos- desconto_inss
    
    valor_salario_liquido.append(f'''{valor_final:,.2f}''')
    valor_desconto_inss.append(f'''{desconto_inss:,.2f}''')
    valor_desconto_irrf.append(f'''{desconto_irrf:,.2f}''')

ler['Desconto do inss'] = valor_desconto_inss
ler['Desconto do irrf'] =  valor_desconto_irrf
ler['Salario liquido'] = valor_salario_liquido

writer = pd.ExcelWriter('salario_com_os_descontos.xlsx')
ler.to_excel(writer,'new_sheet')
writer.save()
print(ler)
