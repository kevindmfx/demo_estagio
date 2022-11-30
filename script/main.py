import requests # --- Bibliotecas para o funcionamento do programa
import json
import os
import time

clear = lambda: os.system('cls')
espera = lambda: time.sleep(2)

def req(url): # --- Faz o scrap das informações do cep
    r1 = requests.get(url).text
    return r1

def add_db(dadosdb): # --- Salva no banco de dados
    try:
        db = open('db\\db.text', 'a', newline="", encoding="UTF8")  
        db.write( (f'{dadosdb}') )
        print('As informações foram salvas no banco de dados com sucesso!')
        db.close()
    except Exception as error:
        db.close()
        print('Não foi possivel salvar as informações no banco de dados!')   

def pegardds(): # --- Recolhe os dados e envia para o banco de dados
    while True:
        clear()
        print('BUSCA DE DADOS:\n')
        nome = input('Informe seu nome completo: ')
        cep = input('informe seu cep: ')
        cep.replace("-", "").replace(".", "").replace(" ", "")
        if len(cep) == 8 and cep.isdigit() == True and nome.isdigit() == False:
            reqcep = req(f'https://viacep.com.br/ws/{cep}/json')               
            dados = json.loads(reqcep)
            try:
                impdb = f"""
                        Nome: {nome.title()}
                        Cep: {dados['cep']}
                        Rua: {dados['logradouro']}
                        Bairro: {dados['bairro']}
                        Cidade: {dados['localidade']}
                        Estado: {dados['uf']}""".replace('                        ', '')
            except Exception as error:
                input('\nCEP não encontrado! Aperte ENTER para voltar ao menu.')  
                break
            else:    
                print(impdb)
                escolha1 = input('\nDeseja salvar essas informações? ( S ou N ) : ')
                if escolha1.upper() == 'S':
                    add_db(impdb)    
                    escolha2 = input('\nDeseja continuar a busca? ( S ou N ): ')
                    if escolha2.upper() != 'S':
                        print('\nVoltando para o menu!')
                        espera()
                        break
                    else:
                        print('\nVoltando para a busca!')
                        espera()
                else:    
                    print('\nVoltando para o menu!')
                    espera()
                    break     
        else:
            input('\nAlgo deu errado! Aperte ENTER para voltar ao menu.') 
            break   
        
def mostrardb(): # --- Nostra o banco de dados do programa
    clear()
    try:
        db = open('db\\db.text', 'r', encoding='UTF8')
        db1 = db.read()
    except Exception as error:
        print('\nNão existem dados salvos!')        
        db.close()    
        espera()
    else:        
        if db1 != '':
            input(f'BANCO DE DADOS: \n{db1}\n\nAperte ENTER para voltar ao menu.')
        else:    
            print('\nNão existem dados salvos!')        
            db.close()    
            espera()

def menu(): # --- Cria o menu do programa
    try:
        os.makedirs('db')    
        db = open('db\\db.text', 'a', newline="", encoding="UTF8")
        db.close()
    except OSError:
        db = open('db\\db.text', 'a', newline="", encoding="UTF8")
        db.close()
    while True:
        clear()
        escolhamenu = input('''MENU:\n1 - Buscar dados\n2 - Ver banco de dados\n3 - Sair\nSelecione a opção que deseja: ''')
        if escolhamenu == '1' or escolhamenu == '2' or escolhamenu == '3':
            if escolhamenu == '1':
                pegardds()
            if escolhamenu == '2':
                mostrardb()
            if escolhamenu == '3':
                print('Fechando aplicativo...')
                espera()
                break    
        else:
            print('Opção inválida!')  
            espera()          

menu() # --- Inicia o programa
