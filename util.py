import os
import json

def Cabecalho():
    os.system('cls')
    print(""" 
    ███████╗░█████╗░██╗░░██╗  ██████╗░███████╗██╗░░░██╗
    ██╔════╝██╔══██╗╚██╗██╔╝  ██╔══██╗██╔════╝██║░░░██║
    █████╗░░██║░░██║░╚███╔╝░  ██║░░██║█████╗░░╚██╗░██╔╝
    ██╔══╝░░██║░░██║░██╔██╗░  ██║░░██║██╔══╝░░░╚████╔╝░
    ██║░░░░░╚█████╔╝██╔╝╚██╗  ██████╔╝███████╗░░╚██╔╝░░
    ╚═╝░░░░░░╚════╝░╚═╝░░╚═╝  ╚═════╝░╚══════╝░░░╚═╝░░░
                ⍟  𝔖𝔦𝔰𝔱𝔢𝔪𝔞 𝔡𝔢 𝔪𝔞𝔰𝔰𝔞 𝔍𝔰𝔬𝔫 ⍟
    """)
    print("QA Online BR - EdsonSan")

def InicializaArquivo():
    dbcursos_json = 'dbcursos.json'
    diretorio_atual = os.listdir()
    if dbcursos_json in diretorio_atual:
            print("Arquivo existe")
            with open('dbcursos.json','r',encoding='utf-8') as dbcursos:
                dados = json.load(dbcursos)
                dbcursos.close()       
                return dados
    else:
        print("Arquivo não Existe")
        exit
   

# def GravaArquivo(variavel):
#     atualizaArquivo = open('dbcursos.json','w')
#     atualizaArquivo.writelines(variavel)
#     # atualizaArquivo.  (variavel)
#     atualizaArquivo.close()       
    