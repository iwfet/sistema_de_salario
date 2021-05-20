import tkinter as tk
from tkinter import Canvas, DoubleVar, Message, filedialog, ttk
from tkinter.constants import X
import pandas as pd
from openpyxl import *
import Calculo_valores as calc

#Criando as listas
valor_salario_liquido = []
valor_desconto_inss = []
valor_desconto_irrf = []

#Gerando parte visual
root = tk.Tk()
root.title('Selecionar arquivo')
varBarra = DoubleVar()
varBarra.set(0)

Canvas1 = tk.Canvas(root, width= 300, height= 300, bg='white')
Canvas1.pack()
pb = ttk.Progressbar(root, variable=varBarra, maximum=100)
pb.place(x=78, y=200, width=144, height= 20)   
valor_salario_liquido = []

ler = 0
import_file_path = filedialog.askopenfilename()
ler = pd.read_excel(import_file_path)

def getExcel():
    global ler
    count = 0
    etapas= 100
    while count < etapas:
        count= count + 1
        i = 0
        while i <1000000:
            i = i + 2
        varBarra.set(count)
        root.update()
    root.quit()
    
browseButton_excel = tk.Button(
    text="Executar",
    command=getExcel,
    bg='green', fg='black', font=('helvetica', 12, 'bold'))
Canvas1.create_window(150,150, window=browseButton_excel)


root.mainloop()

#Iniciando o for junto com os calculos
for index, linha in ler.iterrows():
    id = linha["Matricula"]
    nome = linha["Nome"]
    Dependentes = linha["Dependentes"]
    Descontos = linha["Desconto"]
    Salario_bruto = linha["Salario"]
    
    #Chamando as fuctions
    desconto_inss = calc.DescontoINSS(Salario_bruto)
    desconto_irrf = calc.DescontoIRRF(Salario_bruto,desconto_inss,Dependentes)
    valor_final = Salario_bruto - desconto_irrf - Descontos- desconto_inss
    
    #Colocando os valores nas variaveis 
    valor_salario_liquido.append(f'''{valor_final:,.2f}''')
    valor_desconto_inss.append(f'''{desconto_inss:,.2f}''')
    valor_desconto_irrf.append(f'''{desconto_irrf:,.2f}''')

#Adicionando as listas no excel
ler['Desconto do inss'] = valor_desconto_inss
ler['Desconto do irrf'] =  valor_desconto_irrf
ler['Salario liquido'] = valor_salario_liquido

#Gerando o excel
writer = pd.ExcelWriter('Folha Descontada.xlsx')
ler.to_excel(writer,'new_sheet')
writer.save()
print(ler)