import psycopg2
import datetime
import os
import time
import sys
import msvcrt
from passlib.hash import sha256_crypt
conn = psycopg2.connect("host=localhost dbname=CoimbraBus user=postgres password=dani2002")
cur = conn.cursor()

#=================================================================================================================
# Função getpass
#=================================================================================================================
def getpass(prompt='Password: '):
    password = ''
    while True:
        sys.stdout.write(prompt)
        sys.stdout.flush()
        key = msvcrt.getch()
        if key == b'\r' or key == b'\n':
            sys.stdout.write('\n')
            return password
        elif key == b'\b' or ord(key) == 127:
            password = password[:-1]
            sys.stdout.write('\b \b')
        else:
            password += key.decode()
            sys.stdout.write('*')

#=================================================================================================================
#=================================================================================================================
#=============================================PÁGINA DE REGISTO/LOGIN=============================================
#=================================================================================================================
#=================================================================================================================
def menu0():
    while(1):
        os.system('cls')
        print('Coimbra Bus')
        print('[1] Efetuar Login como Cliente')
        print('[2] Efetuar Login como Administrador')
        print('[3] Registar uma nova conta Cliente')
        print('[4] Sair')

        opcao = input('Escolha a opção pretendida: ')
        if(opcao == '1'):
            return 1,0
        elif(opcao == '2'):
            return 2,0
        elif(opcao == '3'):
            return 3,0
        elif(opcao == '4'):
            return -1,0
        else:
            print('Opção inválida. Tente novamente!')
            time.sleep(1)

#=================================================================================================================
# Página Login do Cliente
#=================================================================================================================
def menu1():
    os.system('cls')
    print('Login Cliente')
    mail_cliente = input('Insira o Email (prima S para sair): ')
    if(mail_cliente == 's' or mail_cliente == 'S'):
        return 0,0,0
    
    count = 0
    cur.execute('SELECT email FROM cliente')
    for linha in cur.fetchall():
        mail, = linha
        if(mail == mail_cliente):
            count = 1
    if(count != 1):
        print('Email não encontrado')
        time.sleep(1)
        nome = 0
        id_cliente = 0
        return 1, nome, id_cliente
    
    cur.execute("SELECT nome FROM cliente WHERE email = '%s';" % (mail_cliente))
    nome, = cur.fetchone()

    cur.execute("SELECT id_cliente FROM cliente WHERE email = '%s';" % (mail_cliente))
    id_cliente, = cur.fetchone()

    print('Insira a password: ', end = "")
    password = getpass("")
    
    cur.execute("SELECT password FROM cliente WHERE email = '%s' ;" % (mail_cliente))
    password_encriptada, = cur.fetchone()

    if (sha256_crypt.verify(password, password_encriptada) == 1):
        print("\nLogin bem sucedido!")
        time.sleep(1)
        return 4, nome, id_cliente
    else:
        print("\nPalavra-passe errada.")
        time.sleep(1)
        return 1, nome, id_cliente

#=================================================================================================================
# Página Login do Administrador
#=================================================================================================================
def menu2():
    os.system('cls')
    print('Login Administrador')
    mail_admin = input('Insira o Email (prima S para sair): ')
    if(mail_admin == 's' or mail_admin == 'S'):
        return 0,0,0
    
    count = 0
    cur.execute('SELECT email FROM administrador')
    for linha in cur.fetchall():
        mail, = linha
        if(mail == mail_admin):
            count = 1
    if(count != 1):
        print('Email não encontrado')
        time.sleep(1)
        nome = 0
        id_admin = 0
        return 2, nome, id_admin
   
    cur.execute("SELECT nome FROM administrador WHERE email = '%s';" % (mail_admin))
    nome, = cur.fetchone()

    cur.execute("SELECT id_administrador FROM administrador WHERE email ='%s';" % (mail_admin))
    id_admin, = cur.fetchone()

    print('Insira a password: ', end="")
    password = getpass("")

    cur.execute("SELECT password FROM administrador WHERE email = '%s' ;" % (mail_admin))
    password_encriptada, = cur.fetchone()
    log = (sha256_crypt.verify(password, password_encriptada))
    if (log == True):
        print("\nLogin bem sucedido!")
        time.sleep(1)
        return 12, nome, id_admin
    else:
        print("\nPalavra-passe errada.")
        time.sleep(1)
        return 2, nome, id_admin

#=================================================================================================================
# Página Registo Cliente
#=================================================================================================================
def menu3():
    os.system('cls')
    print('Registo')
    nome_utilizador = input("Digite o seu nome (prima V para voltar): ")
    if (nome_utilizador == 'v' or nome_utilizador == 'V'):
        return 0,0
    while(1):
        confirmar = input("Tem a certeza que '%s' é o seu nome? (S/N): " % (nome_utilizador))
        if(confirmar == 'N' or confirmar == 'n'):
            return 3,0
        elif(confirmar == 'S' or confirmar == 's'):
                while (1):
                    count = 0
                    mail_dado = input("Insira o seu Email: ")
                    cur.execute("SELECT email FROM cliente;")
                    for linha in cur.fetchall():
                        mail, = linha
                        if(mail_dado == mail):
                            count += 1
                            print("\nEsse mail já está em uso!\n")
                    if (count == 0):
                        break
                
                print("Escolha a sua palavra-passe (Prima V para voltar): ", end="")
                password = getpass("")
                if (password == 'v' or password == 'V'):
                    return 0,0
                password_enc = sha256_crypt.hash(password)
                while(1):
                    print('Confirme a password (Prima V para voltar): ', end="")
                    confirmar_pass = getpass("")
                    if (confirmar_pass == 'v' or confirmar_pass == 'V'):
                        return 0,0
                    elif(sha256_crypt.verify(confirmar_pass,password_enc) == 1):
                        break
                    else:
                        print('Digite a mesma password!')
                    

                while(1):
                    nif = input('Insira o seu NIF (Prima V para voltar): ')
                    if (nif == 'v' or nif == 'V'):
                        return 0,0                    
                    elif(len(nif) != 9):
                        print('Insira um NIF válido')
                    elif(nif.isnumeric() != True):
                        print('Insira um NIF válido')
                    else:
                        nif = int(nif)
                        count = 0
                        cur.execute("SELECT nif FROM cliente;")
                        for linha in cur.fetchall():
                            nif_conf, = linha
                            if(nif == nif_conf):
                                count = 1
                        if (count == 0):
                            break
                        else:
                            print("\nEsse NIF já está em uso!\n")

                while(1):
                    telnum = input('Insira o seu número de telemóvel (Prima V para voltar): ')
                    if (telnum == 'v' or telnum == 'V'):
                        return 0,0                      
                    if(len(telnum) != 9):
                        print('Insira um número válido')
                    elif(telnum.isnumeric() != True):
                        print('Insira um número válido')
                    else:
                        telnum = int(telnum)
                        break
                
                print("\nRegisto concluido!")
                cur.execute("INSERT INTO public.cliente(nome, nif, telefone, email, password) VALUES ('%s', %d, %d, '%s', '%s');" % (nome_utilizador, nif, telnum, mail_dado, password_enc))
                conn.commit()
                time.sleep(2)
                return 0,0                    
        else:
            print('Digite algo válido!')
            time.sleep(1)  


#=================================================================================================================      
#=================================================================================================================
#=============================================PÁGINA DO CLIENTE===================================================
#=================================================================================================================        
#============================================
def menu4(nome):
    while(1):
        os.system('cls')
        print('Página Inicial de', nome)
        print('[1] Viagens')
        print('[2] Meus Bilhetes')
        print('[3] Mensagens')
        print('[4] Terminar Sessão')

        opcao = input('Escolha a opção pretendida: ')

        if(opcao == '1'):
            return 5,0
        elif(opcao == '2'):
            return 10,0
        elif(opcao == '3'):
            return 11,0
        elif(opcao == '4'):
            return 0,0
        else:
            print('Opção inválida. Tente novamente!')
            time.sleep(1)

#=================================================================================================================
# Página das Viagens
#=================================================================================================================
def menu5(nome,order):
    if(order == 0):
        os.system('cls')
        print('Página de', nome)
        print('Viagens')
        data_hoje = datetime.date.today()     
        cur.execute("SELECT distancia, destino, duracao FROM percurso WHERE origem='Coimbra' AND data >= '%s'" % (str(data_hoje)))
        print('===============Viagens com Origem em Coimbra===============')
        for k,linha in enumerate(cur.fetchall(),1):
            print("[%d] " % (k) + "Destino:", linha[1] + " -> Distância (km):", str(linha[0]) + " -> Duração:", linha[2])
        
        cur.execute("SELECT distancia, origem, duracao FROM percurso WHERE destino='Coimbra' AND data >= '%s'" % (str(data_hoje)))
        print('===============Viagens com Destino em Coimbra===============')
        for k,linha in enumerate(cur.fetchall(),1):
            print("[%d] " % (k) + "Origem:", linha[1] + " -> Distância (km):", str(linha[0]) + " -> Duração:", linha[2])

    elif(order == 1): #FILTRA POR NOME
        os.system('cls')
        print('Página de', nome)
        print('Viagens')
        data_hoje = datetime.date.today()         
        var_viagem = input('Insira o nome da cidade ou parte dela: ')
        cur.execute("SELECT distancia, origem, destino, duracao FROM percurso WHERE destino LIKE '" + var_viagem +"%' AND data >= '" + str(data_hoje) +"';" )
        print('===============Viagens com Origem em Coimbra===============')
        for k,linha in enumerate(cur.fetchall(),1):
            print("[%d] " % (k) + "Origem:", linha[1] + " -> Destino:", linha[2] + " -> Distância (km):", str(linha[0]) + " -> Duração:", linha[3])
        
        print('===============Viagens com Destino em Coimbra===============')
        cur.execute("SELECT distancia, origem, destino, duracao FROM percurso WHERE origem LIKE '" + var_viagem +"%' AND data >= '" + str(data_hoje) +"';" )
        for k,linha in enumerate(cur.fetchall(),1):
            print("[%d] " % (k) + "Origem:", linha[1] + " -> Destino:", linha[2] + " -> Distância (km):", str(linha[0]) + " -> Duração:", linha[3])
             
    elif(order == 2): #FILTRA POR DISTANCIA
        os.system('cls')
        print('Página de', nome)
        print('Viagens')    
        data_hoje = datetime.date.today()     
        while(1):
            var_distancia = input('Insira a distância (km): ')
            if(var_distancia.isnumeric() == 1):
                var_distancia = int(var_distancia)
                cur.execute("SELECT distancia, origem, destino, duracao FROM percurso WHERE distancia = %d AND data >= '%s';" % (var_distancia, str(data_hoje)))
                for k,linha in enumerate(cur.fetchall(),1):
                    print("[%d] " % (k) + "Origem:", linha[1] + " -> Destino:", linha[2] + " -> Distância (km):", str(linha[0]) + " -> Duração:", linha[3]) 
                break
            else:
                print('Digite algo válido')
                time.sleep(1)

    elif(order == 3): #FILTRA POR DURAÇAO
        os.system('cls')
        print('Página de', nome)
        print('Viagens')
        data_hoje = datetime.date.today()         
        var_duracao = input('Insira a duração (00h:00min): ')
        cur.execute("SELECT distancia, origem, destino, duracao FROM percurso WHERE duracao LIKE '%" + var_duracao + "%' AND data >= '" + str(data_hoje) + "' ORDER BY duracao;")
        for k,linha in enumerate(cur.fetchall(),1):
            print("[%d] " % (k) + "Origem:", linha[1] + " -> Destino:", linha[2] + " -> Distância (km):", str(linha[0]) + " -> Duração:", linha[3]) 
    while(1):
        print("=======================================================================================")
        print("========================================Viagens========================================")
        print("=======================================================================================")
        print('[1] Pesquisar Viagem')
        print('[2] Filtrar por nome')
        print('[3] Filtrar por distância')
        print('[4] Filtrar por duração')
        print('[5] Voltar')

        opcao = input('Escolha a opção pretendida: ')
        
        if(opcao == '1'):
            return 6, 0
        elif(opcao == '2'):
            return 5,1
        elif(opcao == '3'):
            return 5,2
        elif(opcao == '4'):
            return 5,3
        elif(opcao == '5'):
            return 4,0
        else:
            print('Opção inválida. Tente novamente!')
            time.sleep(1)

#=================================================================================================================
# Página de Viagens - Pesquisar
#=================================================================================================================
def menu6(nome):
    os.system('cls')
    print('Página de', nome)
    while(1):
        print('[1] Pesquisar por Destino')
        print('[2] Pesquisar por Data')
        print('[3] Pesquisar por Distância')
        print('[4] Voltar')

        opcao = input('Escolha a opção pretendida: ')
        
        if(opcao == '1'):
            return 7, 1
        elif(opcao == '2'):
            return 7, 2
        elif(opcao == '3'):
            return 7, 3
        elif(opcao == '4'):
            return 5,0
        else:
            print('Opção inválida. Tente novamente!')
            time.sleep(1)

#=================================================================================================================
# Página de Viagens - Pesquisar - Pesquisa Escolhida
#=================================================================================================================  
def menu7(nome,order,id_cliente):
    os.system('cls')
    print('Página de', nome)
    data_hoje = datetime.date.today()
    if(order == 1): # CÓDIGO PARA PESQUISAR PELO DESTINO
        var_destino = input('Insira o nome do destino da viagem que pretende pesquisar (prima R para retroceder): ')
        if (var_destino == 'r' or var_destino == 'R'):
            return 6,0,0  # Volta para o menu 6    
        count = 1
        cur.execute("SELECT destino FROM percurso WHERE destino LIKE '{}%';" .format(var_destino))
        for linha in cur.fetchall():
            destino, = linha
            if (var_destino == destino):
                count = 0
        if (count != 0):
            print("Erro! Destino não encontrado.")
            time.sleep(1)
            return 7, 1, 0 # Pede para inserir novamente
        
        cur.execute("SELECT id_percurso, distancia, origem, destino, duracao, data FROM percurso WHERE destino LIKE '{}%' AND data >= '{}' ORDER BY data;".format(var_destino,str(data_hoje)))
        aux = []
        for k,linha in enumerate(cur.fetchall(),1):
            aux.append(linha[0])
            print("[%d] " % (k) + "Origem:", linha[2] + " -> Destino:", linha[3] + " -> Distância (km):", str(linha[1]) + " -> Duração:", linha[4] + " -> Data:", str(linha[5]))

        while(1):
            opcao = input('Escolha a viagem que deseja ver os detalhes (Clique 0 para retroceder): ')
            if(opcao.isnumeric() == 1):
                opcao = int(opcao)
                if(opcao == 0):
                    return 6,0,0
                elif(opcao <= k and opcao > 0):
                    break
                else:
                    opcao = str(opcao)
                    print('Digite algo válido')
                    time.sleep(1)

        id_percurso = aux[opcao-1] #PERCURSO QUE SE VAI VER OS DETALHES
         
        
        return 8,0,id_percurso
        
    elif(order == 2): # CÓDIGO PARA PESQUISAR PELA DATA
        cur.execute("SELECT DISTINCT data FROM percurso WHERE data >= '%s';" % (str(data_hoje)))
        print("Datas Disponíveis:")
        for linha in cur.fetchall():
            data, = linha
            print("--> " + str(data))
        print("")
        
        var_data = input('Insira a data da viagem que pretende pesquisar (AAAA-MM-DD) (prima R para retroceder): ')
        if (var_data == 'r' or var_data == 'R'):
            return 6,0,0  # Volta para o menu 6    
        count = 1
        cur.execute("SELECT data FROM percurso WHERE data = '" + var_data +"';")
        for linha in cur.fetchall():
            data, = linha
            if (var_data == str(data)):
                count = 0
        if (count != 0):
            print("Erro! Data não encontrada.")
            time.sleep(1)
            return 7, 2, 0 # Pede para inserir novamente
        
        cur.execute("SELECT id_percurso, distancia, origem, destino, duracao, data FROM percurso WHERE data = '" + var_data +"';")
        aux = []
        for k,linha in enumerate(cur.fetchall(),1):
            aux.append(linha[0])
            print("[%d] " % (k) + "Origem:", linha[2] + " -> Destino:", linha[3] + " -> Distância (km):", str(linha[1]) + " -> Duração:", linha[4] + " -> Data:", str(linha[5]))

        while(1):
            opcao = input('Escolha a viagem que deseja ver os detalhes (Clique 0 para retroceder): ')
            if(opcao.isnumeric() == 1):
                opcao = int(opcao)
                if(opcao == 0):
                    return 6,0,0
                elif(opcao <= k and opcao > 0):
                    break
                else:
                    opcao = str(opcao)
                    print('Digite algo válido')
                    time.sleep(1)

        id_percurso = aux[opcao-1] #PERCURSO QUE SE VAI VER OS DETALHES

        return 8,0,id_percurso

    elif(order == 3): # CÓDIGO PARA PESQUISAR PELA DISTÂNCIA
        while(1):
            var_distancia = input('Insira a distância (Km) que pretende pesquisar (prima R para retroceder): ')
            if (var_distancia == 'r' or var_distancia == 'R'):
                return 6,0,0 # Volta para o menu 6
            elif(var_distancia.isnumeric() == 1):
                var_distancia = int(var_distancia)
                break
            else:
                print('Digite algo válido')
                time.sleep(1)

        count = 1
        cur.execute("SELECT distancia FROM percurso WHERE distancia = %d AND data >= '%s'" % (var_distancia, str(data_hoje)))
        for linha in cur.fetchall():
            distancia, = linha
            if (var_distancia == distancia):
                count = 0
        if (count != 0):
            print("Erro! Distância não encontrada.")
            time.sleep(1)
            return 7, 3, 0 # Pede para inserir novamente
        
        cur.execute("SELECT id_percurso, distancia, origem, destino, duracao, data FROM percurso WHERE distancia = %d AND data >= '%s';" % (var_distancia, str(data_hoje)))
        aux = []
        for k,linha in enumerate(cur.fetchall(),1):
            aux.append(linha[0])
            print("[%d] " % (k) + "Origem:", linha[2] + " -> Destino:", linha[3] + " -> Distância (km):", str(linha[1]) + " -> Duração:", linha[4] + " -> Data:", str(linha[5]))

        while(1):
            opcao = input('Escolha a viagem que deseja ver os detalhes (Clique 0 para retroceder): ')
            if(opcao.isnumeric() == 1):
                opcao = int(opcao)
                if(opcao == 0):
                    return 6,0,0
                elif(opcao <= k and opcao > 0):
                    break
                else:
                    opcao = str(opcao)
                    print('Digite algo válido')
                    time.sleep(1)

        id_percurso = aux[opcao-1] #PERCURSO QUE SE VAI VER OS DETALHES

        return 8,0,id_percurso
    
    elif(order == 4): # CÓDIGO PARA PESQUISAR PELO DESTINO -> BILHETES PASSADOS
        var_destino = input('Insira o nome do destino da viagem que pretende pesquisar (prima R para retroceder): ')
        if (var_destino == 'r' or var_destino == 'R'):
            return 10,0,0  # Volta para o menu 10    
        count = 1
        cur.execute("SELECT destino FROM bilhete, viagem, percurso WHERE cliente_id_cliente = {} AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data < '{}' AND destino LIKE '{}%' ORDER BY data" .format(id_cliente, data_hoje, var_destino))
        for linha in cur.fetchall():
            destino, = linha
            if (var_destino == destino):
                count = 0
        if (count != 0):
            print("Erro! Destino não encontrado.")
            time.sleep(1)
            return 7, 4, 0 # Pede para inserir novamente
        
        cur.execute("SELECT lugar_escolhido, hora_partida, preco, autocarro_id_autocarro, distancia, origem, destino, duracao, data FROM bilhete, viagem, percurso WHERE cliente_id_cliente = {} AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data < '{}' AND destino LIKE '{}%' ORDER BY data" .format(id_cliente, data_hoje, var_destino))
        print("=========================================")

        for linha in cur.fetchall():
            print("Origem:", linha[5] + " -> Destino:", linha[6] + "\nData:", str(linha[8]) + " -> Hora:", linha[1] + "\nDistância (Km):", str(linha[4]) + " -> Duração:", linha[7] + "\nAutocarro Nº:", str(linha[3]) + " -> Lugar:", str(linha[0]) + "\nPreço (€):", str(linha[2]))
            print("=========================================")

        while(1):
            opcao = input("Clique V para voltar: ")
            if(opcao == 'v' or opcao == 'V'):
                return 10,0,0
        
    elif(order == 5): # CÓDIGO PARA PESQUISAR PELA DATA -> BILHETES PASSADOS
        cur.execute("SELECT DISTINCT data FROM bilhete, viagem, percurso WHERE cliente_id_cliente = {} AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data < '{}' ORDER BY data" .format(id_cliente, data_hoje))
        print("Datas Disponíveis:")
        for linha in cur.fetchall():
            data, = linha
            print("--> " + str(data))
        print("")

        var_data = input('Insira a data da viagem que pretende pesquisar (AAAA-MM-DD) (prima R para retroceder): ')
        if (var_data == 'r' or var_data == 'R'):
            return 10,0,0  # Volta para o menu 10   
        count = 1
        cur.execute("SELECT data FROM bilhete, viagem, percurso WHERE cliente_id_cliente = {} AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data = '{}' ORDER BY data" .format(id_cliente, var_data))
        for linha in cur.fetchall():
            data, = linha
            if (var_data == str(data)):
                count = 0
        if (count != 0):
            print("Erro! Data não encontrada.")
            time.sleep(1)
            return 7, 5, 0 # Pede para inserir novamente
        
        cur.execute("SELECT lugar_escolhido, hora_partida, preco, autocarro_id_autocarro, distancia, origem, destino, duracao, data FROM bilhete, viagem, percurso WHERE cliente_id_cliente = {} AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data = '{}' ORDER BY data" .format(id_cliente,var_data))
        print("=========================================")

        for linha in cur.fetchall():
            print("Origem:", linha[5] + " -> Destino:", linha[6] + "\nData:", str(linha[8]) + " -> Hora:", linha[1] + "\nDistância (Km):", str(linha[4]) + " -> Duração:", linha[7] + "\nAutocarro Nº:", str(linha[3]) + " -> Lugar:", str(linha[0]) + "\nPreço (€):", str(linha[2]))
            print("=========================================")

        while(1):
            opcao = input("Clique V para voltar: ")
            if(opcao == 'v' or opcao == 'V'):
                return 10,0,0
            
    elif(order == 6): # CÓDIGO PARA PESQUISAR PELA DISTÂNCIA -> BILHETES PASSADOS
        while(1):
            var_distancia = input('Insira a distância (Km) que pretende pesquisar (prima R para retroceder): ')
            if (var_distancia == 'r' or var_distancia == 'R'):
                return 10,0,0 # Volta para o menu 6
            elif(var_distancia.isnumeric() == 1):
                var_distancia = int(var_distancia)
                break
            else:
                print('Digite algo válido')
                time.sleep(1)

        count = 1
        cur.execute("SELECT distancia FROM bilhete, viagem, percurso WHERE cliente_id_cliente = {} AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data < '{}' AND distancia = {} ORDER BY data" .format(id_cliente, data_hoje, var_distancia))
        for linha in cur.fetchall():
            distancia, = linha
            if (var_distancia == distancia):
                count = 0
        if (count != 0):
            print("Erro! Distância não encontrada.")
            time.sleep(1)
            return 7, 6, 0 # Pede para inserir novamente
        
        cur.execute("SELECT lugar_escolhido, hora_partida, preco, autocarro_id_autocarro, distancia, origem, destino, duracao, data FROM bilhete, viagem, percurso WHERE cliente_id_cliente = {} AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data < '{}' AND distancia = {} ORDER BY data" .format(id_cliente, data_hoje, var_distancia))
        print("=========================================")

        for linha in cur.fetchall():
            print("Origem:", linha[5] + " -> Destino:", linha[6] + "\nData:", str(linha[8]) + " -> Hora:", linha[1] + "\nDistância (Km):", str(linha[4]) + " -> Duração:", linha[7] + "\nAutocarro Nº:", str(linha[3]) + " -> Lugar:", str(linha[0]) + "\nPreço (€):", str(linha[2]))
            print("=========================================")

        while(1):
            opcao = input("Clique V para voltar: ")
            if(opcao == 'v' or opcao == 'V'):
                return 10,0,0

    elif(order == 7): # CÓDIGO PARA PESQUISAR PELO DESTINO -> BILHETES FUTUROS
        var_destino = input('Insira o nome do destino da viagem que pretende pesquisar (prima R para retroceder): ')
        if (var_destino == 'r' or var_destino == 'R'):
            return 10,0,0  # Volta para o menu 10    
        count = 1
        cur.execute("SELECT destino FROM bilhete, viagem, percurso WHERE cliente_id_cliente = {} AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data >= '{}' AND destino LIKE '{}%' ORDER BY data" .format(id_cliente, data_hoje, var_destino))
        for linha in cur.fetchall():
            destino, = linha
            if (var_destino == destino):
                count = 0
        if (count != 0):
            print("Erro! Destino não encontrado.")
            time.sleep(1)
            return 7, 7, 0 # Pede para inserir novamente
        
        cur.execute("SELECT lugar_escolhido, hora_partida, preco, autocarro_id_autocarro, distancia, origem, destino, duracao, data FROM bilhete, viagem, percurso WHERE cliente_id_cliente = {} AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data >= '{}' AND destino LIKE '{}%' ORDER BY data" .format(id_cliente, data_hoje, var_destino))
        print("=========================================")

        for linha in cur.fetchall():
            print("Origem:", linha[5] + " -> Destino:", linha[6] + "\nData:", str(linha[8]) + " -> Hora:", linha[1] + "\nDistância (Km):", str(linha[4]) + " -> Duração:", linha[7] + "\nAutocarro Nº:", str(linha[3]) + " -> Lugar:", str(linha[0]) + "\nPreço (€):", str(linha[2]))
            print("=========================================")

        while(1):
            opcao = input("Clique V para voltar: ")
            if(opcao == 'v' or opcao == 'V'):
                return 10,0,0
        
    elif(order == 8): # CÓDIGO PARA PESQUISAR PELA DATA -> BILHETES FUTUROS
        cur.execute("SELECT DISTINCT data FROM bilhete, viagem, percurso WHERE cliente_id_cliente = {} AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data >= '{}' ORDER BY data" .format(id_cliente, data_hoje))
        print("Datas Disponíveis:")
        for linha in cur.fetchall():
            data, = linha
            print("--> " + str(data))
        print("")

        var_data = input('Insira a data da viagem que pretende pesquisar (AAAA-MM-DD) (prima R para retroceder): ')
        if (var_data == 'r' or var_data == 'R'):
            return 10,0,0  # Volta para o menu 10   
        count = 1
        cur.execute("SELECT data FROM bilhete, viagem, percurso WHERE cliente_id_cliente = {} AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data = '{}' ORDER BY data" .format(id_cliente, var_data))
        for linha in cur.fetchall():
            data, = linha
            if (var_data == data):
                count = 0
        if (count != 0):
            print("Erro! Data não encontrada.")
            time.sleep(1)
            return 7, 8, 0 # Pede para inserir novamente
        
        cur.execute("SELECT lugar_escolhido, hora_partida, preco, autocarro_id_autocarro, distancia, origem, destino, duracao, data FROM bilhete, viagem, percurso WHERE cliente_id_cliente = {} AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data = '{}' ORDER BY data" .format(id_cliente,var_data))
        print("=========================================")

        for linha in cur.fetchall():
            print("Origem:", linha[5] + " -> Destino:", linha[6] + "\nData:", str(linha[8]) + " -> Hora:", linha[1] + "\nDistância (Km):", str(linha[4]) + " -> Duração:", linha[7] + "\nAutocarro Nº:", str(linha[3]) + " -> Lugar:", str(linha[0]) + "\nPreço (€):", str(linha[2]))
            print("=========================================")

        while(1):
            opcao = input("Clique V para voltar: ")
            if(opcao == 'v' or opcao == 'V'):
                return 10,0,0
            
    elif(order == 9): # CÓDIGO PARA PESQUISAR PELA DISTÂNCIA -> BILHETES FUTUROS
        while(1):
            var_distancia = input('Insira a distância (Km) que pretende pesquisar (prima R para retroceder): ')
            if (var_distancia == 'r' or var_distancia == 'R'):
                return 10,0,0 # Volta para o menu 6
            elif(var_distancia.isnumeric() == 1):
                var_distancia = int(var_distancia)
                break
            else:
                print('Digite algo válido')
                time.sleep(1)

        count = 1
        cur.execute("SELECT distancia FROM bilhete, viagem, percurso WHERE cliente_id_cliente = {} AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data >= '{}' AND distancia = {} ORDER BY data" .format(id_cliente, data_hoje, var_distancia))
        for linha in cur.fetchall():
            distancia, = linha
            if (var_distancia == distancia):
                count = 0
        if (count != 0):
            print("Erro! Distância não encontrada.")
            time.sleep(1)
            return 7, 9, 0 # Pede para inserir novamente
        
        cur.execute("SELECT lugar_escolhido, hora_partida, preco, autocarro_id_autocarro, distancia, origem, destino, duracao, data FROM bilhete, viagem, percurso WHERE cliente_id_cliente = {} AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data >= '{}' AND distancia = {} ORDER BY data" .format(id_cliente, data_hoje, var_distancia))
        print("=========================================")

        for linha in cur.fetchall():
            print("Origem:", linha[5] + " -> Destino:", linha[6] + "\nData:", str(linha[8]) + " -> Hora:", linha[1] + "\nDistância (Km):", str(linha[4]) + " -> Duração:", linha[7] + "\nAutocarro Nº:", str(linha[3]) + " -> Lugar:", str(linha[0]) + "\nPreço (€):", str(linha[2]))
            print("=========================================")

        while(1):
            opcao = input("Clique V para voltar: ")
            if(opcao == 'v' or opcao == 'V'):
                return 10,0,0

    elif(order == 10):
        cur.execute("SELECT id_bilhete,id_viagem,lugar_escolhido, hora_partida, preco, autocarro_id_autocarro, distancia, origem, destino, duracao, data FROM bilhete, viagem, percurso WHERE cliente_id_cliente = {} AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data >= '{}' ORDER BY data, hora_partida" .format(id_cliente, data_hoje))

        aux_bilhete = []
        aux_viagem = []
        for k,linha in enumerate(cur.fetchall(),1):
            aux_bilhete.append(linha[0])
            aux_viagem.append(linha[1])
            print("=====================Viagem %d=====================" % (k))
            print("Origem:", linha[7] + " -> Destino:", linha[8] + "\nData:", str(linha[10]) + " -> Hora:", linha[3] + "\nDistância (Km):", str(linha[6]) + " -> Duração:", linha[9] + "\nAutocarro Nº:", str(linha[5]) + " -> Lugar:", str(linha[2]) + "\nPreço (€):", str(linha[4]))
        
        while(1):
            opcao = input('Escolha a o bilhete que deseja cancelar (Clique 0 para retroceder): ')
            if(opcao.isnumeric() == 1):
                opcao = int(opcao)
                if(opcao == 0):
                    return 10,0,0
                elif(opcao <= k and opcao > 0):
                    break
                else:
                    opcao = str(opcao)
                    print('Digite algo válido')
                    time.sleep(1)


        id_bilhete = aux_bilhete[opcao-1]
        id_viagem = aux_viagem[opcao-1]

        while(1):
            escolha = input('Deseja mesmo cancelar este bilhete? (S/N): ')
            if(escolha == 'S' or escolha == 's'):
                cur.execute("DELETE FROM bilhete WHERE id_bilhete = %d" % (id_bilhete))
                cur.execute("SELECT bilhetes_cancelados FROM viagem WHERE id_viagem = %d" % (id_viagem))
                num_cancel, = cur.fetchone()
                num_cancel = num_cancel + 1
                cur.execute("UPDATE viagem SET bilhetes_cancelados = %d WHERE id_viagem = %d" % (num_cancel,id_viagem))
                print('Bilhete cancelado com sucesso!')
                conn.commit()
                time.sleep(2)
                return 10,0,0
            elif(escolha == 'N' or escolha == 'n'):
                return 10,0,0
            else:
                print('Tente novamente! Opção inválida.')
                time.sleep(1)

#=================================================================================================================
# Página de Viagens - Detalhes
#=================================================================================================================
def menu8(id_percurso,id_cliente):
    os.system('cls')
    print("Detalhes da viagem")
    cur.execute("SELECT * FROM percurso WHERE id_percurso = %d;" % (id_percurso))
    for linha in cur.fetchall():
        print("Origem:", linha[2] + "\nDestino:", linha[3] + "\nDistância (km):", str(linha[1]) + "\nDuração:", linha[4] + "\nData:", str(linha[5]))
    
    print("======================================================")

    cur.execute("SELECT gold FROM cliente WHERE id_cliente = %d;" % (id_cliente))
    gold, = cur.fetchone()
    if(gold == 1):
        cur.execute("SELECT id_viagem, hora_partida, preco FROM viagem WHERE percurso_id_percurso = %d ORDER BY hora_partida" % (id_percurso))
        aux = []
        for k,linha in enumerate(cur.fetchall(),1):
            aux.append(linha[0])
            print("[%d] " % (k) + "Preço (€):", str(linha[2] * 0.9) + " -> Hora de Partida:", linha[1])
    
    else:
        cur.execute("SELECT id_viagem, hora_partida, preco FROM viagem WHERE percurso_id_percurso = %d ORDER BY hora_partida" % (id_percurso))
        aux= []
        for k,linha in enumerate(cur.fetchall(),1):
            aux.append(linha[0])
            print("[%d] " % (k) + "Preço (€):", str(linha[2]) + " -> Hora de Partida:", linha[1])
    
    while(1):
            opcao = input('Escolha o bilhete que deseja reservar (Clique 0 para retroceder): ')
            if(opcao.isnumeric() == 1):
                opcao = int(opcao)
                if(opcao == 0):
                    return 6,0,0
                elif(opcao <= k and opcao > 0):
                    break
                else:
                    opcao = str(opcao)
                    print('Digite algo válido')
                    time.sleep(1)

    id_viagem = aux[opcao-1]

    while(1):
        opcao = input("Deseja passar para a reserva deste bilhete? (S/N): ")
        if(opcao == 'n' or opcao == 'N'):
            return 6,0,0
        elif(opcao == 's' or opcao == 'S'):
            cur.execute("SELECT autocarro_id_autocarro FROM viagem WHERE percurso_id_percurso = %d" % (id_percurso))
            id_autocarro, = cur.fetchone()
            return 9, id_viagem, id_autocarro
        else:
            print("Digite algo válido")
            time.sleep(1)
#=================================================================================================================
# Página de Viagens - Detalhes - Reserva
#=================================================================================================================
def menu9(id_viagem,id_autocarro,id_cliente):
    cur.execute("SELECT cheia FROM viagem WHERE id_viagem = %d" % (id_viagem))
    cheio, = cur.fetchone()

    if(cheio == 1):
        opcao = input("O autocarro está cheio, ficará na lista de espera, deseja continuar? (S/N): ")
        if(opcao == 'n' or opcao == 'N'):
            return 6,0
        elif(opcao == 's' or opcao == 'S'):
            print('Irá no autocarro: %d' % (id_autocarro))
            hora_compra = datetime.datetime.now()
            cur.execute("INSERT INTO bilhete(hora_compra, lista_espera, lugar_escolhido, cliente_id_cliente, viagem_id_viagem) VALUES ('%s', 'True', 0, %d, %d);" % (str(hora_compra), id_cliente, id_viagem))
            cur.execute("SELECT clientes_espera FROM viagem WHERE id_viagem = %d" % (id_viagem))
            clientes_espera, = cur.fetchone()
            clientes_espera = clientes_espera + 1
            cur.execute("UPDATE viagem SET clientes_espera = %d WHERE id_viagem = %d" % (clientes_espera,id_viagem))
            print('Bilhete reservado com sucesso!')
            conn.commit()
            return 4,0
    else:
        cur.execute("SELECT lugares_escolhidos FROM viagem WHERE id_viagem = %d" % (id_viagem))
        lugares_escolhidos, = cur.fetchone()
        cur.execute("SELECT lugares_ocupados FROM viagem WHERE id_viagem = %d" % (id_viagem))
        lugares_ocupados, = cur.fetchone()
        cur.execute("SELECT lotacao FROM autocarro WHERE id_autocarro = %d" % (id_autocarro))
        lotacao, = cur.fetchone()

        print("Lugares ocupados de %d: %d" % (lotacao, lugares_ocupados))
        while(1):
            lugar = input("Escolha o lugar que deseja ocupar: ")
            if(lugar.isnumeric() == 1):
                if(lotacao >= int(lugar)):
                    if(lugar in lugares_escolhidos):
                        print('Esse lugar está ocupado! Digite outro!')
                        time.sleep(1)
                    else:
                        print('Irá no autocarro: %d' % (id_autocarro))

                        lugares_ocupados = lugares_ocupados + 1
                        cur.execute("UPDATE viagem SET lugares_ocupados = '%s' WHERE id_viagem = %d;" % (lugares_ocupados, id_viagem))
                        soma_lugares = lugares_escolhidos + " " + lugar + ";"
                        cur.execute("UPDATE viagem SET lugares_escolhidos = '%s' WHERE id_viagem = %d;" % (soma_lugares, id_viagem))

                        hora_compra = datetime.datetime.now()
                        cur.execute("INSERT INTO bilhete(hora_compra, lista_espera, lugar_escolhido, cliente_id_cliente, viagem_id_viagem) VALUES ('%s', 'False', %d, %d, %d);" % (str(hora_compra), int(lugar), id_cliente, id_viagem))
                        cur.execute("SELECT numero_viagens FROM cliente WHERE id_cliente = %d" % (id_cliente))
                        num_viagens, = cur.fetchone()
                        num_viagens = num_viagens + 1
                        cur.execute("UPDATE cliente SET numero_viagens = %d WHERE id_cliente = %d;" % (num_viagens, id_cliente) )
                        print('Bilhete reservado com sucesso!')
                        time.sleep(2)
                        conn.commit()
                        return 4,0
                else:
                    print("Escolha um lugar válido")
                    time.sleep(1)
            else:
                print("Escolha um lugar válido")
                time.sleep(1)
        
    
#=================================================================================================================
# Página dos Meus Bilhetes
#=================================================================================================================
def menu10(nome,order,id_cliente):
    if(order == 1):
        os.system('cls')
        print('Página de', nome)
        print('Viagens Realizadas')        
        data_hoje = datetime.datetime.today()
        cur.execute("SELECT count(*) FROM bilhete, viagem, percurso WHERE cliente_id_cliente = %d AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data < '%s'" % (id_cliente, str(data_hoje)))
        viagens_realizadas, = cur.fetchone()

        cur.execute("SELECT count(*) FROM bilhete, viagem, percurso WHERE cliente_id_cliente = %d AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data < '%s' AND origem = 'Coimbra'" % (id_cliente, str(data_hoje)))
        ida, = cur.fetchone()

        cur.execute("SELECT count(*) FROM bilhete, viagem, percurso WHERE cliente_id_cliente = %d AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data < '%s' AND destino = 'Coimbra'" % (id_cliente, str(data_hoje)))
        regresso, = cur.fetchone()        
        print('Já realizou %d viagens, %d de ida e %d de regresso' % (viagens_realizadas, ida, regresso))

        while(1):
            opcao = input('Clique V para voltar: ')
            if(opcao == 'v' or opcao == 'V'):
                break
    elif(order == 2):
        os.system('cls')
        print('Página de', nome)        
        print('Viagens Passadas')
        data_hoje = datetime.datetime.today()
        cur.execute("SELECT lugar_escolhido, hora_partida, preco, autocarro_id_autocarro, distancia, origem, destino, duracao, data FROM bilhete, viagem, percurso WHERE cliente_id_cliente = %d AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data < '%s' ORDER BY data" % (id_cliente, str(data_hoje)))
        print("=========================================")

        for linha in cur.fetchall():
            print("Origem:", linha[5] + " -> Destino:", linha[6] + "\nData:", str(linha[8]) + " -> Hora:", linha[1] + "\nDistância (Km):", str(linha[4]) + " -> Duração:", linha[7] + "\nAutocarro Nº:", str(linha[3]) + " -> Lugar:", str(linha[0]) + "\nPreço (€):", str(linha[2]))
            print("=========================================")
        
        while(1):
            print('[1] Pesquisar por Destino')
            print('[2] Pesquisar por Data')
            print('[3] Pesquisar por Distância')
            print('[4] Voltar')

            opcao = input('Escolha a opção pretendida: ')
            
            if(opcao == '1'):
                return 7,4
            elif(opcao == '2'):
                return 7,5
            elif(opcao == '3'):
                return 7,6
            elif(opcao == '4'):
                break
            else:
                print('Opção inválida. Tente novamente!')
                time.sleep(1)
    elif(order == 3):
        os.system('cls')
        print('Página de', nome)         
        print('Viagens Futuras')
        data_hoje = datetime.datetime.today()
        cur.execute("SELECT lugar_escolhido, hora_partida, preco, autocarro_id_autocarro, distancia, origem, destino, duracao, data FROM bilhete, viagem, percurso WHERE cliente_id_cliente = %d AND viagem_id_viagem = id_viagem AND percurso_id_percurso = id_percurso AND data >= '%s' ORDER BY data, hora_partida" % (id_cliente, str(data_hoje)))
        print("=========================================")

        for linha in cur.fetchall():
            print("Origem:", linha[5] + " -> Destino:", linha[6] + "\nData:", str(linha[8]) + " -> Hora:", linha[1] + "\nDistância (Km):", str(linha[4]) + " -> Duração:", linha[7] + "\nAutocarro Nº:", str(linha[3]) + " -> Lugar:", str(linha[0]) + "\nPreço (€):", str(linha[2]))
            print("=========================================")
        
        while(1):
            print('[1] Pesquisar por Destino')
            print('[2] Pesquisar por Data')
            print('[3] Pesquisar por Distância')
            print('[4] Cancelar Viagem')
            print('[5] Voltar')

            opcao = input('Escolha a opção pretendida: ')
            
            if(opcao == '1'):
                return 7,7
            elif(opcao == '2'):
                return 7,8
            elif(opcao == '3'):
                return 7,9
            elif(opcao == '4'):
                return 7,10
            elif(opcao == '5'):
                break
            else:
                print('Opção inválida. Tente novamente!')
                time.sleep(1)
    while(1):
        os.system('cls')
        print('Página de', nome)
        print('Meus Bilhetes')
        print('[1] Viagens Realizadas')
        print('[2] Viagens Passadas')
        print('[3] Viagens Futuras')
        print('[4] Voltar')

        opcao = input('Escolha a opção pretendida: ')
        
        if(opcao == '1'):
            return 10,1
        elif(opcao == '2'):
            return 10,2
        elif(opcao == '3'):
            return 10,3
        elif(opcao == '4'):
            return 4,0
        else:
            print('Opção inválida. Tente novamente!')
            time.sleep(1)

#=================================================================================================================
# Página das Mensagens
#=================================================================================================================
def menu11(nome,order,id_cliente):
    if(order == 1):
        os.system('cls')
        print('Mensagens Não Lidas')
        cur.execute("SELECT texto FROM mensagem WHERE hora_vista ISNULL AND cliente_id_cliente = %d;" %(id_cliente))
        for k,linha in enumerate(cur.fetchall(),1):
            texto, = linha
            tamanho = len(texto)
            aux = 0
            print("[%d] " % (k) + "Mensagem Não Lida -", end =" ")
            while(aux < tamanho/2):
                print(texto[aux], end="")
                aux = aux + 1
            print("...")

        cur.execute("SELECT id_mensagem FROM mensagem WHERE hora_vista ISNULL AND cliente_id_cliente = %d;" %(id_cliente))
        aux = []
        for k,linha in enumerate(cur.fetchall(),1):
            texto, = linha
            aux.append(texto)

        while(1):
            opcao = input('Escolha o mensagem que deseja ler (Clique 0 para retroceder): ')
            if(opcao.isnumeric() == 1):
                opcao = int(opcao)
                if(opcao == 0):
                    return 11,0
                elif(opcao <= k and opcao > 0):
                    break
                else:
                    opcao = str(opcao)
                    print('Digite algo válido')
                    time.sleep(1)

        id_mensagem = aux[opcao-1]

        while(1):
            os.system('cls')
            print('Página de', nome)
            print('Mensagem %d' % (opcao))
            cur.execute("SELECT texto FROM mensagem WHERE id_mensagem = %d;" %(id_mensagem))
            mensagem, = cur.fetchone()
            print(mensagem)
            opcao = input('Clique V para voltar: ')
            if(opcao == 'v' or opcao == 'V'):
                hora = datetime.datetime.now()
                cur.execute("UPDATE mensagem SET hora_vista = '%s' WHERE id_mensagem = %d" % (hora,id_mensagem))
                conn.commit()
                return 11,1
            else:
                print('Tente novamente! Digite V para voltar')
                time.sleep(1)


    elif(order == 2):
        os.system('cls')
        print('Mensagens Lidas')
        cur.execute("SELECT texto FROM mensagem WHERE hora_vista NOTNULL AND cliente_id_cliente = %d;" %(id_cliente))
        for k,linha in enumerate(cur.fetchall(),1):
            texto, = linha
            tamanho = len(texto)
            aux = 0
            print("[%d] " % (k) + "Mensagem Lida -", end =" ")
            while(aux < tamanho/2):
                print(texto[aux], end="")
                aux = aux + 1
            print("...")

        cur.execute("SELECT id_mensagem FROM mensagem WHERE hora_vista NOTNULL AND cliente_id_cliente = %d;" %(id_cliente))
        aux = []
        for k,linha in enumerate(cur.fetchall(),1):
            texto, = linha
            aux.append(texto)

        while(1):
            opcao = input('Escolha o mensagem que deseja ler (Clique 0 para retroceder): ')
            if(opcao.isnumeric() == 1):
                opcao = int(opcao)
                if(opcao == 0):
                    return 11,0
                elif(opcao <= k and opcao > 0):
                    break
                else:
                    opcao = str(opcao)
                    print('Digite algo válido')
                    time.sleep(1)

        id_mensagem = aux[opcao-1]

        while(1):
            os.system('cls')
            print('Página de', nome)
            print('Mensagem %d' % (opcao))
            cur.execute("SELECT texto FROM mensagem WHERE id_mensagem = %d;" %(id_mensagem))
            mensagem, = cur.fetchone()
            print(mensagem)
            opcao = input('Clique V para voltar: ')
            if(opcao == 'v' or opcao == 'V'):
                return 11,2
            else:
                print('Tente novamente! Digite V para voltar')
                time.sleep(1)

    while(1):
        os.system('cls')
        print('Página de', nome)
        print('Mensagens')        
        print('[1] Mensagens Não Lidas')
        print('[2] Mensagens Lidas')
        print('[3] Voltar')

        opcao = input('Escolha a opção pretendida: ')
        
        if(opcao == '1'):
            return 11,1
        elif(opcao == '2'):
            return 11,2
        elif(opcao == '3'):
            return 4,0
        else:
            print('Opção inválida. Tente novamente!')
            time.sleep(1)   


#=================================================================================================================        
#=================================================================================================================   
#=============================================PÁGINA DO ADMINISTRADOR=============================================
#=================================================================================================================        
#=================================================================================================================   
def menu12(nome):
    while(1):
        os.system('cls')
        print('Página Inicial do Administrador', nome)
        print('[1] Menu de Tarefas')
        print('[2] Enviar Mensagens')
        print('[3] Visualização')
        print('[4] Estatísticas')
        print('[5] Terminar Sessão')

        opcao = input('Escolha a opção pretendida: ')

        if(opcao == '1'):
            return 13,0
        elif(opcao == '2'):
            return 17,0
        elif(opcao == '3'):
            return 19,0
        elif(opcao == '4'):
            return 21,0
        elif(opcao == '5'):
            return 0,0
        else:
            print('Opção inválida. Tente novamente!')
            time.sleep(2)

#=================================================================================================================
# Página do Menu de Tarefas
#=================================================================================================================
def menu13(nome):
    while(1):
        os.system('cls')
        print('Página do Administrador', nome)
        print('Menu de Tarefas')
        print('[1] Autocarro')
        print('[2] Viagem')
        print('[3] Cliente')
        print('[4] Voltar')

        opcao = input('Escolha a opção pretendida: ')
        breakpoint
        if(opcao == '1'):
            return 14,1
        elif(opcao == '2'):
            return 14,2
        elif(opcao == '3'):
            return 14,3
        elif(opcao == '4'):
            return 12,0
        else:
            print('Opção inválida. Tente novamente!')
            time.sleep(2)

def menu14(nome,order):
    os.system('cls')
    print('Página do Administrador', nome)
    if(order == 1):
        print('Autocarro')
        print('[1] Alterar')
        print('[2] Adicionar')
        print('[3] Remover')
        print('[4] Voltar')

        opcao = input('Escolha a opção pretendida: ')
        if(opcao == '1'):
            return 15,1
        elif(opcao == '2'):
            return 15,2
        elif(opcao == '3'):
            return 15,3
        elif(opcao == '4'):
            return 13,0
        else:
            print('Opção inválida. Tente novamente!')
            time.sleep(1)
            return 14,1

    elif(order == 2):
        print('Viagem')
        print('[1] Alterar')
        print('[2] Adicionar')
        print('[3] Remover')
        print('[4] Voltar')

        opcao = input('Escolha a opção pretendida: ')
        if(opcao == '1'):
            return 16,1
        elif(opcao == '2'):
            return 16,2
        elif(opcao == '3'):
            return 16,3
        elif(opcao == '4'):
            return 13,0
        else:
            print('Opção inválida. Tente novamente!')
            time.sleep(1)
            return 14,2            

    elif(order == 3):
        print('Cliente')
        print('[1] Atribuir Gold')
        print('[2] Retirar Gold')
        print('[3] Voltar')

        opcao = input('Escolha a opção pretendida: ')
        if(opcao == '1'):
            cur.execute("SELECT id_cliente, nome, nif, telefone, email, gold FROM cliente WHERE gold = 'False' ORDER BY nome")

            aux = []
            for k,linha in enumerate(cur.fetchall(),1):
                cliente = linha
                aux.append(cliente[0])
                print("[%d] " % (k) + "Nome:", cliente[1] + "; NIF:", str(cliente[2]) + "; Telemóvel:", str(cliente[3]) + "; Email:", cliente[4] + "; Gold: ", cliente[5])

            while(1):
                opcao = input('Escolha o cliente que deseja atribuir o gold (Clique 0 para retroceder): ')
                if(opcao.isnumeric() == 1):
                    opcao = int(opcao)
                    if(opcao == 0):
                        return 14,3
                    elif(opcao <= k and opcao > 0):
                        break
                    else:
                        opcao = str(opcao)
                        print('Digite algo válido')
                        time.sleep(1)

            id_cliente = aux[opcao-1]

            cur.execute("UPDATE cliente SET gold = 'True' WHERE id_cliente = %d;" % (id_cliente))
            conn.commit()
            print('Gold atribuído com sucesso')
            time.sleep(2)
            return 13,0
        
        elif(opcao == '2'):
            cur.execute("SELECT id_cliente, nome, nif, telefone, email, gold FROM cliente WHERE gold = 'True' ORDER BY nome")
            aux = []
            for k,linha in enumerate(cur.fetchall(),1):
                cliente = linha
                aux.append(cliente[0])
                print("[%d] " % (k) + "Nome:", cliente[1] + "; NIF:", str(cliente[2]) + "; Telemóvel:", str(cliente[3]) + "; Email:", cliente[4] + "; Gold: ", cliente[5])

            while(1):
                opcao = input('Escolha o cliente que deseja atribuir o gold (Clique 0 para retroceder): ')
                if(opcao.isnumeric() == 1):
                    opcao = int(opcao)
                    if(opcao == 0):
                        return 14,3
                    elif(opcao <= k and opcao > 0):
                        break
                    else:
                        opcao = str(opcao)
                        print('Digite algo válido')
                        time.sleep(1)

            id_cliente = aux[opcao-1]

            cur.execute("UPDATE cliente SET gold = 'False' WHERE id_cliente = %d;" % (id_cliente))
            conn.commit()
            print('Gold retirado com sucesso')
            time.sleep(2)
            return 13,0
        elif(opcao == '3'):
            return 13,0
        else:
            print('Opção inválida. Tente novamente!')
            time.sleep(1)
            return 14,3

#=================================================================================================================
# Página do Menu de Tarefas - Página dos Autocarros
#=================================================================================================================
def menu15(nome,order):
    os.system('cls')
    print('Página do Administrador', nome)
    if(order == 1): #ALTERAR AUTOBUS
        print('Alterar Autocarro')
        cur.execute('SELECT id_autocarro,matricula,lotacao, disponivel FROM autocarro')

        aux = []
        for k,linha in enumerate(cur.fetchall(),1):
            autocarro = linha
            aux.append(autocarro[0])
            print("[%d] " % (k) + "Matrícula:", autocarro[1] + "; Lotação:", str(autocarro[2]) + "; Disponível:", str(autocarro[3]))

        while(1):
            opcao = input('Escolha o autocarro que deseja alterar (Clique 0 para retroceder): ')
            if(opcao.isnumeric() == 1):
                opcao = int(opcao)
                if(opcao == 0):
                    return 14,1
                elif(opcao <= k and opcao > 0):
                    break
                else:
                    opcao = str(opcao)
                    print('Digite algo válido')
                    time.sleep(1)

        id_autocarro = aux[opcao-1] #AUTOCARRO QUE SE VAI ALTERAR
        
        while(1):
            escolha = input('Deseja alterar a matrícula? (S/N): ')
            if(escolha == 'S' or escolha == 's'):
                nova_matricula = input('Coloque a nova Matrícula (XX-XX-XX): ')
                nova_matricula = nova_matricula.upper()
                cur.execute("UPDATE autocarro SET matricula = '%s' " % (nova_matricula) + "WHERE id_autocarro = %d" % (id_autocarro))
                print('Matrícula alterada com sucesso')
                break
            elif(escolha == 'N' or escolha == 'n'):
                break
            else:
                print('Tente novamente! Opção inválida.')
                time.sleep(1)
        
        while(1):
            escolha = input('Deseja alterar a lotação? (S/N): ')
            if(escolha == 'S' or escolha == 's'):
                while(1):
                    nova_lotacao = input('Coloque a nova lotação: ')
                    if(nova_lotacao.isnumeric() == 1):
                        nova_lotacao = int(nova_lotacao)
                        cur.execute("UPDATE autocarro SET lotacao = %d " % (nova_lotacao) + "WHERE id_autocarro = %d" % (id_autocarro))
                        print('Lotação alterada com sucesso')
                        break
                    else:
                        print('Insira uma lotação válida')
                break
            elif(escolha == 'N' or escolha == 'n'):
                break
            else:
                print('Tente novamente! Opção inválida.')
                time.sleep(1)
        
        while(1):
            escolha = input('Deseja alterar a disponibilidade? (S/N): ')
            if(escolha == 'S' or escolha == 's'):
                nova_disponibilidade = input('Coloque se o autocarro está disponível ou não(True/False): ')
                while(nova_disponibilidade != 'True' or nova_disponibilidade != 'False'):
                    nova_disponibilidade = input('Coloque se o autocarro está disponível ou não(True/False): ')
                cur.execute("UPDATE autocarro SET disponivel = '%s' " % (nova_disponibilidade) + "WHERE id_autocarro = %d" % (id_autocarro))
                print('Disponibilidaded alterada com sucesso')
                break
            elif(escolha == 'N' or escolha == 'n'):
                break
            else:
                print('Tente novamente! Opção inválida.')
                time.sleep(1)   

        conn.commit()
        print('Terminado!')
        time.sleep(1)
        return 14,1

    elif(order == 2):
        print('Adicionar Autocarro') #VERIFICAR SE DÁ PARA MELHORAR A MATRICULA
        while (1):
            count = 0
            matricula_dada = input('Coloque a Matrícula (XX-XX-XX) (Clique R para retroceder): ')
            if(matricula_dada == 'R' or matricula_dada == 'r'):
                return 14,1
            matricula_dada = matricula_dada.upper()        
            cur.execute("SELECT matricula FROM autocarro;")
            for linha in cur.fetchall():
                matricula, = linha
                if(matricula_dada == matricula):
                    count += 1
                    print("\nEssa matricula já está em uso!\n")
            if (count == 0):
                break        

        while(1):
            lotacao = input('Coloque a lotação do Autocarro: ')
            if(lotacao.isnumeric() == 1):
                lotacao = int(lotacao)
                break
            else:
                print('Digite uma lotação válida')
                time.sleep(1)

        cur.execute("INSERT INTO autocarro (matricula, lotacao) VALUES ('%s', %d);" % (matricula_dada, lotacao))
        conn.commit()
        print('Terminado!')
        time.sleep(1)
        return 14,1        


    elif(order == 3):
        while(1):
            print('Remover Autocarro')     
            cur.execute("SELECT id_autocarro, matricula, lotacao, disponivel FROM autocarro WHERE disponivel = 'True' ORDER BY id_autocarro")

            aux = []
            for k,linha in enumerate(cur.fetchall(),1):
                autocarro = linha
                aux.append(autocarro[0])
                print("[%d] " % (k) + "Matrícula:", autocarro[1] + "; Lotação:", str(autocarro[2]) + "; Disponível:", str(autocarro[3]))

            while(1):
                opcao = input('Escolha o autocarro que deseja remover (Clique 0 para retroceder): ')
                if(opcao.isnumeric() == 1):
                    opcao = int(opcao)
                    if(opcao == 0):
                        return 14,1
                    elif(opcao <= k and opcao > 0):
                        break
                    else:
                        opcao = str(opcao)
                        print('Digite algo válido')
                        time.sleep(1)

            id_autocarro = aux[opcao-1] #AUTOCARRO QUE SE VAI REMOVER

            while(1):
                escolha = input('Deseja mesmo remover este autocarro? (S/N): ')
                if(escolha == 'S' or escolha == 's'):
                    cur.execute("DELETE FROM autocarro WHERE id_autocarro = %d" % (id_autocarro))
                    print('Autocarro removido com sucesso!')
                    conn.commit()
                    break
                elif(escolha == 'N' or escolha == 'n'):
                    break
                else:
                    print('Tente novamente! Opção inválida.')
                    time.sleep(1)

            print('Terminado!')
            time.sleep(2)
            break
        return 14,1
                
#=================================================================================================================                
# Página do Menu de Tarefas - Página das Viagens
#=================================================================================================================
def menu16(nome,order):
    os.system('cls')
    print('Página do Administrador', nome)
    if(order == 1): # ALTERAR VIAGEM
        print('Alterar Viagem')
        cur.execute("SELECT * FROM viagem, percurso WHERE id_percurso = percurso_id_percurso AND data >= '%s' ORDER BY data, hora_partida" % (str(datetime.date.today()))) #ver isto do datatime
        
        aux_viagem = []
        aux_percurso = []
        for k,linha in enumerate(cur.fetchall(),1):
            aux_viagem.append(linha[0])
            aux_percurso.append(linha[9])
            print("=====================Viagem %d=====================" % (k))
            print("Origem:", linha[12] + " -> Destino:", linha[13] + "\nData:", str(linha[15]) + " -> Hora:", linha[1] + "\nDistância (km):", str(linha[11]) + " -> Duração:", linha[14] + "\nAutocarro Nº:", str(linha[8]) + " -> Lugares escolhidos:", linha[3] + " -> Lugares ocupados:", str(linha[6]) + "\nCheia:", str(linha[4]) + " -> Clientes em espera:", str(linha[5]) + "\nPreço (€):", str(linha[2]))

        print("==========================================")

        while(1):
            opcao = input('Escolha a viagem que deseja alterar (Clique 0 para retroceder): ')
            if(opcao.isnumeric() == 1):
                opcao = int(opcao)
                if(opcao == 0):
                    return 14,2
                elif(opcao <= k and opcao > 0):
                    break
                else:
                    opcao = str(opcao)
                    print('Digite algo válido')
                    time.sleep(1)

        id_viagem = aux_viagem[opcao-1] # VIAGEM QUE SE VAI ALTERAR
        id_percurso = aux_percurso[opcao-1]

        count = 0
        cur.execute("SELECT lugares_ocupados FROM viagem, percurso WHERE id_percurso = percurso_id_percurso AND id_percurso = %d" % (id_percurso))
        for linha in cur.fetchall():
            lugares, = linha
            if(lugares != 0):
                count = 1
        if(count == 0):
            cur.execute("SELECT lugares_ocupados FROM viagem WHERE id_viagem = %d" % (id_viagem))
            lugares_ocupados, = cur.fetchone()
            if(lugares_ocupados == 0):
                cur.execute("SELECT origem FROM percurso WHERE id_percurso = %d" % (id_percurso))
                var, = cur.fetchone()

                if(var == 'Coimbra'):
                    while(1):
                        escolha = input('Deseja alterar o Destino? (S/N): ')
                        if(escolha == 'S' or escolha == 's'):
                            novo_destino = input('Coloque o novo Destino: ')
                            cur.execute("UPDATE percurso SET destino = '%s' " % (novo_destino) + "WHERE id_percurso = %d" % (id_percurso))
                            print('Destino alterado com sucesso')
                            while(1):
                                nova_distancia = input('Insira a nova distância (km): ')
                                if(nova_distancia.isnumeric() == 1):
                                    nova_distancia = int(nova_distancia)
                                    cur.execute("UPDATE percurso SET distancia = %d " % (nova_distancia) + "WHERE id_percurso = %d" % (id_percurso))
                                    print('Distância alterada com sucesso')
                                    break
                                else:
                                    print('Insira uma distância válida')
                            break
                        elif(escolha == 'N' or escolha == 'n'):
                            break
                        else:
                            print('Tente novamente! Opção inválida.')
                else:
                    while(1):
                        escolha = input('Deseja alterar a Origem? (S/N): ')
                        if(escolha == 'S' or escolha == 's'):
                            nova_origem = input('Coloque a nova Origem: ')
                            cur.execute("UPDATE percurso SET origem = '%s' " % (nova_origem) + "WHERE id_percurso = %d" % (id_percurso))
                            print('Destino alterado com sucesso')
                            while(1):
                                nova_distancia = input('Insira a nova distância (km): ')
                                if(nova_distancia.isnumeric() == 1):
                                    nova_distancia = int(nova_distancia)
                                    cur.execute("UPDATE percurso SET distancia = %d " % (nova_distancia) + "WHERE id_percurso = %d" % (id_percurso))
                                    print('Distância alterada com sucesso')
                                    break
                                else:
                                    print('Insira uma distância válida')
                            break
                        elif(escolha == 'N' or escolha == 'n'):
                            break
                        else:
                            print('Tente novamente! Opção inválida.')                    

                while(1):
                    escolha = input('Deseja alterar a Data? (S/N): ')
                    if(escolha == 'S' or escolha == 's'):
                        nova_data = input('Coloque a nova Data (AAAA-MM-DD): ')
                        cur.execute("UPDATE percurso SET data = '%s' " % (nova_data) + "WHERE id_percurso = %d" % (id_percurso))
                        print('Data alterada com sucesso')
                        break
                    elif(escolha == 'N' or escolha == 'n'):
                        break
                    else:
                        print('Tente novamente! Opção inválida.')

                while(1):
                    escolha = input('Deseja alterar a Hora de Partida? (S/N): ')
                    if(escolha == 'S' or escolha == 's'):
                        nova_hora = input('Coloque a nova Hora de Partida (00h:00min): ')
                        cur.execute("UPDATE viagem SET hora_partida = '%s' " % (nova_hora) + "WHERE id_viagem = %d" % (id_viagem))
                        print('Hora de Partida alterada com sucesso')
                        break
                    elif(escolha == 'N' or escolha == 'n'):
                        break
                    else:
                        print('Tente novamente! Opção inválida.')

                while(1):
                    escolha = input('Deseja alterar o Autocarro associado? (S/N): ')
                    if(escolha == 'S' or escolha == 's'):
                        while(1):
                            novo_autocarro = input('Coloque o novo Autocarro: ')
                            if(novo_autocarro.isnumeric() == 1):
                                novo_autocarro = int(novo_autocarro)
                                cur.execute("UPDATE viagem SET autocarro_id_autocarro = %d " % (novo_autocarro) + "WHERE id_viagem = %d" % (id_viagem))
                                break
                            else:
                                print('Insira um autocarro válido')
                        break
                    elif(escolha == 'N' or escolha == 'n'):
                        break
                    else:
                        print('Tente novamente! Opção inválida.')

                while(1):
                    escolha = input('Deseja alterar o Preço? (S/N): ')
                    if(escolha == 'S' or escolha == 's'):
                        while(1):
                            novo_preco = input('Coloque o novo Preço (€): ')
                            if(novo_preco.isnumeric() == 1):
                                novo_preco = int(novo_preco)
                                cur.execute("SELECT preco FROM viagem WHERE id_viagem = %d" % (id_viagem))
                                preco_antes, = cur.fetchone()
                                cur.execute("BEGIN TRANSACTION; UPDATE viagem SET preco = %d " % (novo_preco) + "WHERE id_viagem = %d;" % (id_viagem) + "INSERT INTO preco (preco_antes, preco_depois, hora_atualizacao, viagem_id_viagem) VALUES (%d, %d, '%s', %d); COMMIT;" % (preco_antes, novo_preco, str(datetime.datetime.now()), id_viagem))
                                conn.commit()
                                print('Preço alterado com sucesso')
                                break
                            else:
                                print('Insira um preço válido')
                        break
                    elif(escolha == 'N' or escolha == 'n'):
                        break
                    else:
                        print('Tente novamente! Opção inválida.')
                
                print('Terminado')
                conn.commit()
                time.sleep(2)
                return 14,2

            else:
                print("Não se pode alterar essa viagem, porque já tem reservas!")
                time.sleep(1)
                return 16,1
        else:
            print("Não se pode alterar essa viagem, porque já tem reservas!")
            time.sleep(1)
            return 16,1

    elif(order == 2): # ADICIONAR VIAGEM
        print('Adicionar Percurso e Viagem')
        while(1):
            escolha = input('Deseja adicionar um percurso? (S/N) (Clique R para retroceder): ')
            if(escolha == 'S' or escolha == 's'):
                origem = input('Coloque a origem (Clique R para retroceder): ')
                if(origem == 'R' or origem == 'r'):
                    return 14,2
                
                destino = input('Coloque o destino (Clique R para retroceder): ')
                if(destino == 'R' or destino == 'r'):
                    return 14,2
                
                if(origem != 'Coimbra' and destino != 'Coimbra'):
                    print("O percurso tem que começar ou acabar em Coimbra! Tente novamente")
                    time.sleep(1)
                    return 16,2
                    
                while(1):
                    distancia = input('Insira a distância (km) (Clique R para retroceder): ')
                    if(distancia == 'r' or destino == 'R'):
                        return 14,2
                    elif(distancia.isnumeric() == 1):
                        distancia = int(distancia)
                        break
                    else:
                        print('Insira uma distância válida')
                
                duracao = input('Coloque a duração do percurso (00h:00min) (Clique R para retroceder): ')
                if(duracao == 'R' or duracao == 'r'):
                    return 14,2
                
                data = input('Coloque a data do percurso (AAAA-MM-DD) (Clique R para retroceder): ')
                if(data == 'R' or data == 'r'):
                    return 14,2
                
                cur.execute("INSERT INTO percurso (distancia, origem, destino, duracao, data) VALUES (%d, '%s', '%s', '%s', '%s');" % (distancia, origem, destino, duracao,str(data)))
                print("Percurso adicionado!")
                conn.commit()
                break
                
            elif(escolha == 'N' or escolha == 'n'):
                print("Percurso não adicionado")
                break
            
            elif(escolha == 'R' or escolha == 'r'):
                return 14,2
            
            else:
                print('Tente novamente! Opção inválida.')
                time.sleep(1)
        
        while(1):
            escolha = input("Deseja adicionar uma viagem? (S/N) (Clique R para retroceder): ")
            if(escolha == 'S' or escolha == 's'):
                cur.execute("SELECT * FROM percurso WHERE data >= '%s'" % (str(datetime.date.today())))

                for k, linha in enumerate(cur.fetchall(),1):
                    print("ID do Percurso:", str(linha[0]) + " ; Origem:", linha[2] + " ; Destino:", linha[3])

                while(1):
                    id_percurso = input("Insira o percurso onde deseja adicionar uma viagem (Clique R para retroceder): ")
                    if(id_percurso.isnumeric() == 1):
                        id_percurso = int(id_percurso)
                        count = 0
                        cur.execute("SELECT id_percurso FROM percurso WHERE data >= '%s'" % (str(datetime.date.today())))
                        for linha in cur.fetchall():
                            if(id_percurso == linha[0]):
                                count = 1
                        if(count == 1):
                            break
                        else:
                            print('Tente novamente! Esse ID não existe')
                            time.sleep(1)
                    elif(id_percurso == 'R' or id_percurso == 'r'):
                        return 14,2
                    else:
                        print("Digite algo válido")
                        time.sleep(1)
                
                hora_partida = input('Coloque a hora da partida (00h:00min) (Clique R para retroceder): ')
                if(hora_partida == 'R' or hora_partida == 'r'):
                    return 14,2

                while(1):
                    cur.execute("SELECT id_autocarro FROM autocarro")
                    for linha in cur.fetchall():
                        print("ID Autocarro = %d" % (linha[0]))
                    autocarro = input("Insira o autocarro (Clique R para retroceder): ")
                    if(autocarro.isnumeric() == 1):
                        autocarro = int(autocarro)
                        count = 0
                        cur.execute("SELECT id_autocarro FROM autocarro")
                        for linha in cur.fetchall():
                            if(autocarro == linha[0]):
                                count = 1
                        
                        if(count == 1):
                            break
                        else:
                            print('Tente novamente! Esse ID não existe')
                            time.sleep(1)
                    elif(autocarro == 'R' or autocarro == 'r'):
                        return 14,2
                    else:
                        print("Digite algo válido")
                        time.sleep(1)
                
                while(1):
                    preco = input('Insira o preco (€) (Clique R para retroceder): ')
                    if(preco == 'r' or preco == 'R'):
                        return 14,2
                    elif(preco.isnumeric() == 1):
                        preco = int(preco)
                        break
                    else:
                        print('Insira um preço válido')

                cur.execute("INSERT INTO viagem (hora_partida, preco, autocarro_id_autocarro, percurso_id_percurso) VALUES ('%s', %d, %d, %d);" % (hora_partida, preco, autocarro, id_percurso,))
                conn.commit()
                print("Viagem adicionada!")
                break
            
            elif(escolha == 'N' or escolha == 'n'):
                print("Viagem não adicionada")
                time.sleep(2)
                break
            elif(escolha == 'R' or escolha == 'r'):
                return 14,2
            
            else:
                print('Tente novamente! Opção inválida.')
                time.sleep(1)

        print('Terminado')
        time.sleep(2)
        return 14,2
        
    
    elif(order == 3): # REMOVER VIAGEM
        print("Remover Viagem")
        while(1):
            escolha = input("Deseja remover uma viagem? (S/N) (Clique R para retroceder): ")
            if(escolha == 'S' or escolha == 's'):
                cur.execute("SELECT * FROM viagem, percurso WHERE id_percurso = percurso_id_percurso AND data >= '%s' ORDER BY data, hora_partida" % (str(datetime.date.today()))) #ver isto do datatime
                
                aux_viagem = []
                aux_percurso = []
                for k,linha in enumerate(cur.fetchall(),1):
                    aux_viagem.append(linha[0])
                    aux_percurso.append(linha[9])
                    print("=====================Viagem %d=====================" % (k))
                    print("Origem:", linha[12] + " -> Destino:", linha[13] + "\nData:", str(linha[15]) + " -> Hora:", linha[1] + "\nDistância (km):", str(linha[11]) + " -> Duração:", linha[14] + "\nAutocarro Nº:", str(linha[8]) + " -> Lugares escolhidos:", linha[3] + " -> Lugares ocupados:", str(linha[6]) + "\nCheia:", str(linha[4]) + " -> Clientes em espera:", str(linha[5]) + "\nPreço (€):", str(linha[2]))

                print("==========================================")

                while(1):
                    opcao = input('Escolha a viagem que deseja remover (Clique 0 para retroceder): ')
                    if(opcao.isnumeric() == 1):
                        opcao = int(opcao)
                        if(opcao == 0):
                            return 14,2
                        elif(opcao <= k and opcao > 0):
                            break
                        else:
                            opcao = str(opcao)
                            print('Digite algo válido')
                            time.sleep(1)

                id_viagem = aux_viagem[opcao-1] # VIAGEM QUE SE VAI REMOVER
                id_percurso = aux_percurso[opcao-1]

                cur.execute("SELECT lugares_ocupados FROM viagem, percurso WHERE id_viagem = %d AND id_percurso = %d AND percurso_id_percurso = id_percurso" % (id_viagem, id_percurso))
                lugares_ocupados, = cur.fetchone()
                if(lugares_ocupados == 0):
                    while(1):
                        escolha = input('Deseja mesmo remover esta viagem? (S/N): ')
                        if(escolha == 'S' or escolha == 's'):
                            cur.execute("DELETE FROM viagem WHERE id_viagem = %d" % (id_viagem))
                            print('Viagem removida com sucesso!')
                            conn.commit()
                            break
                        elif(escolha == 'N' or escolha == 'n'):
                            break
                        else:
                            print('Tente novamente! Opção inválida.')
                            time.sleep(1)
                else:
                    print("Não se pode remover essa viagem, porque já tem reservas!")
                    time.sleep(1)
                    return 16,3
            
            elif(escolha == 'N' or escolha == 'n'):
                break
            
            elif(escolha == 'R' or escolha == 'r'):
                return 14,2
            
            else:
                print('Digite algo válido')
                time.sleep(1)

        while(1):
            escolha = input("Deseja remover um percurso? (S/N) (Clique R para retroceder): ")
            if(escolha == 'S' or escolha == 's'):
                cur.execute("SELECT * FROM percurso WHERE data >= '%s' ORDER BY data" % (str(datetime.date.today()))) 
                aux_percurso = []
                for k,linha in enumerate(cur.fetchall(),1):
                    aux_percurso.append(linha[0])
                    print("=====================Percurso %d=====================" % (k))
                    print("Origem:", linha[2] + " -> Destino:", linha[3] + "\nData:", str(linha[5]) + " -> Duração:", linha[4] + "\nDistância (Km):", str(linha[1]))

                print("==========================================")

                while(1):
                    opcao = input('Escolha o percurso que deseja remover (Clique 0 para retroceder): ')
                    if(opcao.isnumeric() == 1):
                        opcao = int(opcao)
                        if(opcao == 0):
                            return 14,2
                        elif(opcao <= k and opcao > 0):
                            break
                        else:
                            opcao = str(opcao)
                            print('Digite algo válido')
                            time.sleep(1)
 
                id_percurso = aux_percurso[opcao-1] # PERCURSO QUE SE VAI REMOVER
                
                count = 0
                cur.execute("SELECT lugares_ocupados FROM viagem,percurso WHERE id_percurso = percurso_id_percurso AND id_percurso = %d" % (id_percurso))
                for linha in cur.fetchall():
                    linha, = linha
                    if(linha != 0):
                        count = 1
                
                if(count == 0):
                    while(1):
                        escolha = input('Deseja mesmo remover este percurso e todas as viagens associadas? (S/N): ')
                        if(escolha == 'S' or escolha == 's'):
                            cur.execute("DELETE FROM viagem WHERE percurso_id_percurso = %d" % (id_percurso))                            
                            cur.execute("DELETE FROM percurso WHERE id_percurso = %d" % (id_percurso))
                            print('Percurso removida com sucesso!')
                            conn.commit()
                            time.sleep(2)
                            return 14,2
                        elif(escolha == 'N' or escolha == 'n'):
                            break
                        else:
                            print('Tente novamente! Opção inválida.')
                            time.sleep(1)                    
                else:
                    print("Não se pode remover esse percurso, porque já tem reservas!")
                    time.sleep(1)
                    return 16,3

            
            elif(escolha == 'N' or escolha == 'n'):
                return 14,2
            
            elif(escolha == 'R' or escolha == 'r'):
                return 14,2
            
            else:
                print('Digite algo válido')
                time.sleep(1)

#=================================================================================================================
# Página de Enviar Mensagens   
#=================================================================================================================
def menu17(nome):
    while(1):
        os.system('cls')
        print('Página do Administrador', nome)
        print('Enviar Mensagens')
        print('[1] Individual')
        print('[2] Geral')
        print('[3] Voltar')

        opcao = input('Escolha a opção pretendida: ')

        if(opcao == '1'):
            return 18,1
        elif(opcao == '2'):
            return 18,2
        elif(opcao == '3'):
            return 12,0
        else:
            print('Opção inválida. Tente novamente!')
            time.sleep(2)

def menu18(nome,order,id_admin):
    os.system('cls')
    print('Página do Administrador', nome)  

    if(order == 1): # ENVIAR MENSAGEM INDIVIDUAL
        print('Mensagem Individual')
        
        aux = []
        cur.execute("SELECT id_cliente, nome, nif, telefone, email, gold FROM cliente")
        for k,linha in enumerate(cur.fetchall(),1):
            cliente = linha
            aux.append(cliente[0])
            print("[%d] " % (k) + "Nome:", cliente[1] + "; NIF:", str(cliente[2]) + "; Telemóvel:", str(cliente[3]) + "; Email:", cliente[4] + "; Gold:", str(cliente[5]))
        
        while(1):
            opcao = input('Escolha o cliente que deseja enviar mensagem (Clique 0 para retroceder): ')
            if(opcao.isnumeric() == 1):
                opcao = int(opcao)
                if(opcao == 0):
                    return 17,0
                elif(opcao <= k and opcao > 0):
                    break
                else:
                    opcao = str(opcao)
                    print('Digite algo válido')
                    time.sleep(1)

        id_cliente = aux[opcao-1]

        mensagem = input ("Escreva a mensagem que deseja enviar: ")

        cur.execute("INSERT INTO mensagem (texto, cliente_id_cliente, administrador_id_administrador) VALUES ('%s', %d, %d);" % (mensagem, id_cliente, id_admin)) 

        conn.commit()
        print('Mensagem enviada com sucesso!')
        time.sleep(2)

        return 17,0

    elif(order == 2):
        print('Mensagem Geral')

        mensagem = input ("Escreva a mensagem que deseja enviar: ")

        cur.execute("SELECT id_cliente FROM cliente")
        for linha in cur.fetchall():
            cliente, = linha
            cur.execute("INSERT INTO mensagem (texto, cliente_id_cliente, administrador_id_administrador) VALUES ('%s', %d, %d);" % (mensagem, cliente, id_admin)) 
            

        conn.commit()
        print('Mensagem enviada com sucesso!')
        time.sleep(2)

        return 17,0

#=================================================================================================================
# Página de Visualização    
#=================================================================================================================
def menu19(nome):
    while(1):
        os.system('cls')
        print('Página do Administrador', nome)
        print('Visualização')
        print('[1] Autocarros')
        print('[2] Percursos')
        print('[3] Viagens')
        print('[4] Clientes')
        print('[5] Preços Alterados')
        print('[6] Voltar')

        opcao = input('Escolha a opção pretendida: ')

        if(opcao == '1'):
            return 20,1
        elif(opcao == '2'):
            return 20,2
        elif(opcao == '3'):
            return 20,3
        elif(opcao == '4'):
            return 20,4
        elif(opcao == '5'):
            return 20,5
        elif(opcao == '6'):
            return 12,0
        else:
            print('Opção inválida. Tente novamente!')
            time.sleep(2)

def menu20(nome,order):
    if(order == 1):
        while(1):
            os.system('cls')
            print('Página do Administrador', nome)
            print('Autocarros')     
            cur.execute('SELECT id_autocarro, matricula, lotacao, disponivel FROM autocarro ORDER BY id_autocarro;')

    
            for k,linha in enumerate(cur.fetchall(),1):
                autocarro = linha
                print("[%d] " % (k) + "Matrícula:", autocarro[1] + "; Lotação:", str(autocarro[2]) + "; Disponivel:", str(autocarro[3]))


            opcao = input('Clique V para voltar: ')
            if(opcao == 'v' or opcao == 'V'):
                break
        return 19,0
    
    elif(order == 2):
        while(1):
            os.system('cls')
            print('Página do Administrador', nome)
            print('Percursos') 

            cur.execute("SELECT * FROM percurso WHERE data >= '%s' ORDER BY data" % (str(datetime.date.today())))

            for k,linha in enumerate(cur.fetchall(),1):
                    print("=====================Percurso %d=====================" % (k))
                    print("Origem:", linha[2] + " -> Destino:", linha[3] + "\nData:", str(linha[5]) + " -> Duração:", linha[4] + "\nDistância (Km):", str(linha[1]))

            print("==========================================")
            
            opcao = input('Clique V para voltar: ')
            if(opcao == 'v' or opcao == 'V'):
                break
        
        return 19,0  
    
    elif(order == 3):
        while(1):
            os.system('cls')
            print('Página do Administrador', nome)
            print('Viagens')     
            
            cur.execute("SELECT * FROM viagem, percurso WHERE id_percurso = percurso_id_percurso AND data >= '%s' ORDER BY data, hora_partida" % (str(datetime.date.today()))) #ver isto do datatime
            
            for k,linha in enumerate(cur.fetchall(),1):
                print("=====================Viagem %d=====================" % (k))
                print("Origem:", linha[12] + " -> Destino:", linha[13] + "\nData:", str(linha[15]) + " -> Hora:", linha[1] + "\nDistância (Km):", str(linha[11]) + " -> Duração:", linha[14] + "\nAutocarro Nº:", str(linha[8]) + " -> Lugares escolhidos:", linha[3] + " -> Lugares ocupados:", str(linha[6]) + "\nCheia:", str(linha[4]) + " -> Clientes em espera:", str(linha[5]) + "\nPreço (€):", str(linha[2]))

            print("==========================================")
            
            opcao = input('Clique V para voltar: ')
            if(opcao == 'v' or opcao == 'V'):
                break
        
        return 19,0    
    elif(order == 4):
        while(1):
            os.system('cls')
            print('Página do Administrador', nome)
            print('Clientes')     
            cur.execute("SELECT id_cliente, nome, nif, telefone, email, gold FROM cliente")

    
            for k,linha in enumerate(cur.fetchall(),1):
                cliente = linha
                print("[%d] " % (k) + "Nome:", cliente[1] + "; NIF:", str(cliente[2]) + "; Telemóvel:", str(cliente[3]) + "; Email:", cliente[4] + "; Gold:", str(cliente[5]))

            opcao = input('Clique V para voltar: ')
            if(opcao == 'v' or opcao == 'V'):
                break
        return 19,0
    
    elif(order == 5):
        while(1):
            os.system('cls')
            print('Página do Administrador', nome)
            print('Preços alterados')
            cur.execute("SELECT * FROM preco")

            for k,linha in enumerate(cur.fetchall(),1):
                print("============Atualização Nº: %d============" % (k))
                print("ID_Viagem Alterada:",str(linha[4]) + " -> Hora da Alteração:", str(linha[3]) + "\nPreço Antes:", str(linha[1]) + " -> Preço Atualizado:", str(linha[2]) + "\nID_Atualização:", str(linha[0]))
                
            print("=========================================")

            opcao = input('Clique V para voltar: ')
            if(opcao == 'v' or opcao == 'V'):
                break
        return 19,0
#=================================================================================================================
# Página das Estatísticas
#=================================================================================================================
def menu21(nome):
    while(1):
        os.system('cls')
        print('Página do Administrador', nome)
        print('Estatísticas')
        print('[1] Viagem mais vendida num mês')
        print('[2] Cliente que mais comprou viagens num mês')
        print('[3] Percurso com mais clientes num mês')
        print('[4] Dados estatísticos relativamente à venda de viagens num determinado ano')
        print('[5] Viagens que não tiveram reservas num determinado mês')
        print('[6] Reservas de uma viagem')
        print('[7] Reservas canceladas de uma viagem')
        print('[8] Clientes em espera')
        print('[9] Voltar')

        opcao = input('Escolha a opção pretendida: ')

        if(opcao == '1'):
            return 22,1
        elif(opcao == '2'):
            return 22,2
        elif(opcao == '3'):
            return 22,3
        elif(opcao == '4'):
            return 22,4
        elif(opcao == '5'):
            return 22,5
        elif(opcao == '6'):
            return 22,6
        elif(opcao == '7'):
            return 22,7        
        elif(opcao == '8'):
            return 22,8 
        elif(opcao == '9'):
            return 12,0
        else:
            print('Opção inválida. Tente novamente!')
            time.sleep(2)

def menu22(nome,order):
    os.system('cls')
    print('Página do Administrador', nome)

    if(order == 1): # Viagem mais vendida num mês
        print('Viagem mais vendida num mês')
        while(1):
            ano = input('Insira o ano que deseja visualizar (Prima V para voltar): ')
            if (ano == 'v' or ano == 'V'):
                return 21,0              
            elif(len(ano) != 4):
                print('Insira um ano válido')
            elif(ano.isnumeric() != True):
                print('Insira um NIF válido')
            else:
                ano = int(ano)
                if(ano < 2023 or ano > 2030):
                    print('Insira um ano válido')
                else:
                    break

        while(1):
            mes = input('Insira o mês que deseja visualizar (Prima V para voltar): ')
            if (mes == 'v' or mes == 'V'):
                return 21,0              
            elif(len(mes) < 1 or len(mes) > 2):
                print('Insira um mês válido')
            elif(mes.isnumeric() != True):
                print('Insira um mês válido')
            else:
                mes = int(mes)
                if(mes < 1 or mes > 12):
                    print('Insira um mês válido')
                else:
                    break

        data = datetime.date(ano, mes, 1)

        cur.execute("SELECT id_viagem, COUNT(id_bilhete) AS num_bilhetes_vendidos \
                        FROM viagem \
                        JOIN bilhete ON id_viagem = viagem_id_viagem \
                        WHERE DATE_TRUNC('month', hora_compra) = '%s' \
                        GROUP BY id_viagem \
                        ORDER BY num_bilhetes_vendidos DESC \
                        LIMIT 1;" % (str(data)))          
        count = 0
        for linha in cur.fetchall():
            valor = linha
            count = 1

        if count == 0:
            print("Não existem viagens compradas nesse mês")
            while(1):
                opcao = input('Clique V para voltar: ')
                if(opcao == 'v' or opcao == 'V'):
                    break
            return 21,0
        else:
            cur.execute("SELECT percurso_id_percurso FROM viagem WHERE id_viagem = %d" % (valor[0]))
            id_percurso, = cur.fetchone()
            cur.execute("SELECT * FROM viagem, percurso WHERE id_viagem = %d AND id_percurso = %d AND id_percurso = percurso_id_percurso" % (valor[0], id_percurso))
            
            print("A viagem mais vendida, no mês {} do ano {}, com {} bilhetes comprados foi: " .format(data.month, data.year, valor[1]))
            print("=========================================================")
            for linha in cur.fetchall():
                print("Origem:", linha[12] + " -> Destino:", linha[13] + "\nData:", str(linha[15]) + " -> Hora:", linha[1] + "\nDistância (km):", str(linha[11]) + " -> Duração:", linha[14] + "\nAutocarro Nº:", str(linha[8]) + " -> Lugares escolhidos:", linha[3] + " -> Lugares ocupados:", str(linha[6]) + "\nCheia:", str(linha[4]) + " -> Clientes em espera:", str(linha[5]) + "\nPreço (€):", str(linha[2]))
            print("=========================================================")

            while(1):
                opcao = input('Clique V para voltar: ')
                if(opcao == 'v' or opcao == 'V'):
                    break
            return 21,0
    

    elif(order == 2): # Cliente que mais comprou viagens num mês
        print('Cliente que mais comprou num mês')
        while(1):
            ano = input('Insira o ano que deseja visualizar (Prima V para voltar): ')
            if (ano == 'v' or ano == 'V'):
                return 21,0              
            elif(len(ano) != 4):
                print('Insira um ano válido')
            elif(ano.isnumeric() != True):
                print('Insira um NIF válido')
            else:
                ano = int(ano)
                if(ano < 2023 or ano > 2030):
                    print('Insira um ano válido')
                else:
                    break

        while(1):
            mes = input('Insira o mês que deseja visualizar (Prima V para voltar): ')
            if (mes == 'v' or mes == 'V'):
                return 21,0              
            elif(len(mes) < 1 or len(mes) > 2):
                print('Insira um mês válido')
            elif(mes.isnumeric() != True):
                print('Insira um mês válido')
            else:
                mes = int(mes)
                if(mes < 1 or mes > 12):
                    print('Insira um mês válido')
                else:
                    break

        data = datetime.date(ano, mes, 1)

        cur.execute("SELECT cliente.nome, COUNT(bilhete.id_bilhete) AS total_bilhetes \
                        FROM cliente \
                        JOIN bilhete ON cliente.id_cliente = bilhete.cliente_id_cliente \
                        JOIN viagem ON bilhete.viagem_id_viagem = viagem.id_viagem \
                        WHERE DATE_TRUNC('month', hora_compra) = '%s' \
                        GROUP BY cliente.nome \
                        ORDER BY total_bilhetes DESC \
                        LIMIT 1;" % (str(data)))
        count=0
        for linha in cur.fetchall():
            nome_cliente, num_bilhetes = linha
            count=1

        if count == 0:
            print("Não existem clientes que compraram nesse mês")
            while(1):
                opcao = input('Clique V para voltar: ')
                if(opcao == 'v' or opcao == 'V'):
                    break
            return 21,0
        else:
            print("O Cliente que mais comprou no mês {} do ano {}, foi:".format(data.month, data.year))
            print("Nome: {} -> Número de bilhetes: {}".format(nome_cliente, num_bilhetes))
            while(1):
                opcao = input('Clique V para voltar: ')
                if(opcao == 'v' or opcao == 'V'):
                    break
            return 21,0
    

    elif(order == 3): # Percurso com mais clientes num mês     
        print("Percurso com mais clientes num determinado mês")
        while(1):
            ano = input('Insira o ano que deseja visualizar (Prima V para voltar): ')
            if (ano == 'v' or ano == 'V'):
                return 21,0              
            elif(len(ano) != 4):
                print('Insira um ano válido')
            elif(ano.isnumeric() != True):
                print('Insira um NIF válido')
            else:
                ano = int(ano)
                if(ano < 2023 or ano > 2030):
                    print('Insira um ano válido')
                else:
                    break

        while(1):
            mes = input('Insira o mês que deseja visualizar (Prima V para voltar): ')
            if (mes == 'v' or mes == 'V'):
                return 21,0              
            elif(len(mes) < 1 or len(mes) > 2):
                print('Insira um mês válido')
            elif(mes.isnumeric() != True):
                print('Insira um mês válido')
            else:
                mes = int(mes)
                if(mes < 1 or mes > 12):
                    print('Insira um mês válido')
                else:
                    break

        data = datetime.date(ano, mes, 1)

        cur.execute("SELECT p.origem, p.destino, p.duracao, p.distancia, SUM(v.lugares_ocupados + v.clientes_espera) as lugares_ocupados \
                        FROM percurso p \
                        JOIN viagem v ON p.id_percurso = v.percurso_id_percurso \
                        JOIN ( \
                            SELECT viagem_id_viagem, COUNT(*) as lugares_ocupados \
                            FROM bilhete \
                            WHERE DATE_TRUNC('month', hora_compra) = '%s' \
                            GROUP BY viagem_id_viagem \
                        ) b ON v.id_viagem = b.viagem_id_viagem \
                        GROUP BY p.id_percurso, p.origem, p.destino \
                        ORDER BY lugares_ocupados DESC \
                        LIMIT 1;" % str(data))
        
        count = 0
        for linha in cur.fetchall():
            viagem = linha
            count = 1

        if count == 0:
            print("Não existem percusos com clientes nesse mês")
            while(1):
                opcao = input('Clique V para voltar: ')
                if(opcao == 'v' or opcao == 'V'):
                    break
            return 21,0
        else: 
            print("O percurso com mais clientes no mês {} do ano {} foi:".format(data.month, data.year))
            print("Origem: {} -> Destino: {} -> Distância (Km): {} -> Duração: {} -> Total de Clientes: {}".format(viagem[0], viagem[1], viagem[3], viagem[2], viagem[4]))
            while(1):
                opcao = input('Clique V para voltar: ')
                if(opcao == 'v' or opcao == 'V'):
                    break
            return 21,0  
    
    elif(order == 4): # Dados estatísticos relativamente à venda de viagens num determinado ano
        print("Dados estatísticos relativamente à venda de viagens num determinado ano")
        while(1):
            ano = input('Insira o ano que deseja visualizar (Prima V para voltar): ')
            if (ano == 'v' or ano == 'V'):
                return 21,0              
            elif(len(ano) != 4):
                print('Insira um ano válido')
            elif(ano.isnumeric() != True):
                print('Insira um NIF válido')
            else:
                ano = int(ano)
                if(ano < 2023 or ano > 2030):
                    print('Insira um ano válido')
                else:
                    break
        cur.execute("SELECT DATE_TRUNC('day', hora_compra) AS dia, COUNT(*) AS num_vendas \
                        FROM bilhete \
                        WHERE EXTRACT(year FROM hora_compra) = %d \
                        GROUP BY dia \
                        ORDER BY num_vendas DESC \
                        LIMIT 1;" % (ano))
        count = 0
        for linha in cur.fetchall():
            dia, num_vendas = linha
            count = 1
        cur.execute("SELECT  \
                            EXTRACT(MONTH FROM hora_compra) AS mes, \
                            COUNT(*) AS volume_de_vendas \
                        FROM  \
                            bilhete \
                        WHERE \
                            EXTRACT(YEAR FROM hora_compra) = %d \
                        GROUP BY \
                            mes \
                        ORDER BY \
                            mes ASC;" % (ano))
        
        for linha in cur.fetchall():
            mes, num_vendas1 = linha
        if(count == 0):
            print("Não houve vendas nesse mês")
            while(1):
                opcao = input('Clique V para voltar: ')
                if(opcao == 'v' or opcao == 'V'):
                    break
            return 21,0
        else:
            print("Volume de Vendas em cada mês:")
            print("Mês:", str(mes) + " -> Número de Vendas:", str(num_vendas1))
            print("Dia com mais vendas no ano de %d" % (ano))    
            print("Dia:", str(dia) + " -> Número de Vendas:", str(num_vendas))

            while(1):
                opcao = input('Clique V para voltar: ')
                if(opcao == 'v' or opcao == 'V'):
                    break
            return 21,0  
        
 
    elif(order == 5): # Viagens que não tiveram reservas num determinado mês
        print('Viagens sem reservas num mês')
        while(1):
            ano = input('Insira o ano que deseja visualizar (Prima V para voltar): ')
            if (ano == 'v' or ano == 'V'):
                return 21,0              
            elif(len(ano) != 4):
                print('Insira um ano válido')
            elif(ano.isnumeric() != True):
                print('Insira um NIF válido')
            else:
                ano = int(ano)
                if(ano < 2023 or ano > 2030):
                    print('Insira um ano válido')
                else:
                    break

        while(1):
            mes = input('Insira o mês que deseja visualizar (Prima V para voltar): ')
            if (mes == 'v' or mes == 'V'):
                return 21,0              
            elif(len(mes) < 1 or len(mes) > 2):
                print('Insira um mês válido')
            elif(mes.isnumeric() != True):
                print('Insira um mês válido')
            else:
                mes = int(mes)
                if(mes < 1 or mes > 12):
                    print('Insira um mês válido')
                else:
                    break

        data = datetime.date(ano, mes, 1)

        cur.execute("SELECT * \
                        FROM viagem, percurso \
                        WHERE percurso_id_percurso = id_percurso \
                        AND NOT EXISTS ( \
                            SELECT 1 \
                            FROM bilhete \
                            WHERE viagem_id_viagem = id_viagem \
                            AND DATE_TRUNC('month', hora_compra) =  '%s');" % (str(data)))
        
        print("As viagens sem reserva no mês {} no ano {} foram:".format(data.month, data.year))
        for k,linha in enumerate(cur.fetchall(),1):
            print("=====================Viagem %d=====================" % (k))
            print("Origem:", linha[12] + " -> Destino:", linha[13] + "\nData:", str(linha[15]) + " -> Hora:", linha[1] + "\nDistância (km):", str(linha[11]) + " -> Duração:", linha[14] + "\nAutocarro Nº:", str(linha[8]) + " -> Lugares escolhidos:", linha[3] + " -> Lugares ocupados:", str(linha[6]) + "\nCheia:", str(linha[4]) + " -> Clientes em espera:", str(linha[5]) + "\nPreço (€):", str(linha[2]))

        while(1):
            opcao = input('Clique V para voltar: ')
            if(opcao == 'v' or opcao == 'V'):
                break
        return 21,0
    
    
    elif(order == 6): # Reservas de uma viagem
        print("Reservas de uma viagem")
        cur.execute("SELECT * FROM viagem, percurso WHERE id_percurso = percurso_id_percurso AND data >= '%s' ORDER BY data, hora_partida" % (str(datetime.date.today())))

        for k,linha in enumerate(cur.fetchall(),1):
            print("=====================Viagem %d=====================" % (k))
            print("Origem:", linha[12] + " -> Destino:", linha[13] + "\nData:", str(linha[15]) + " -> Hora:", linha[1] + "\nDistância (km):", str(linha[11]) + " -> Duração:", linha[14] + "\nAutocarro Nº:", str(linha[8]) + " -> Reservas:", str(linha[6] + linha[5]) + "\nCheia:", str(linha[4]) + "\nPreço (€):", str(linha[2]))

        print("==========================================")

        while(1):
            opcao = input('Clique V para voltar: ')
            if(opcao == 'v' or opcao == 'V'):
                break
        return 21,0  
    
    
    elif(order == 7): # Reservas canceladas de uma viagem
        print("Reservas canceladas de uma viagem")
        cur.execute("SELECT * FROM viagem, percurso WHERE id_percurso = percurso_id_percurso AND data >= '%s' AND bilhetes_cancelados != 0 ORDER BY data, hora_partida" % (str(datetime.date.today())))

        for k,linha in enumerate(cur.fetchall(),1):
            print("=====================Viagem %d=====================" % (k))
            print("Origem:", linha[12] + " -> Destino:", linha[13] + "\nData:", str(linha[15]) + " -> Hora:", linha[1] + "\nDistância (Km):", str(linha[11]) + " -> Duração:", linha[14] + "\nAutocarro Nº:", str(linha[8]) + " -> Reservas:", str(linha[6] + linha[5]) + " -> Reservas Canceladas: ", str(linha[7]) + "\nCheia:", str(linha[4]) + "\nPreço (€):", str(linha[2]))

        print("==========================================")
        while(1):
            opcao = input('Clique V para voltar: ')
            if(opcao == 'v' or opcao == 'V'):
                break
        return 21,0  
    
    elif(order == 8): # Clientes em espera
        print("Clientes em Lista de Espera: ")
        cur.execute("SELECT nome, email, nif, telefone, gold, hora_compra \
                        FROM bilhete \
                        JOIN cliente ON cliente_id_cliente = id_cliente \
                        WHERE lista_espera = 'True';")
        for k,linha in enumerate(cur.fetchall(),1):
            print("[{}] Nome: {}; Email: {}; NIF: {}; Telemóvel: {}; Gold: {}; Hora de Compra: {}".format(k,linha[0],linha[1],linha[2],linha[3],linha[4],linha[5]))

        while(1):
            opcao = input('Clique V para voltar: ')
            if(opcao == 'v' or opcao == 'V'):
                break
        return 21,0  
                          
#=================================================================================================================
#=================================================================================================================
#=============================================MAIN================================================================
#=================================================================================================================
#=================================================================================================================
menu = 0
nome = 0
order = 0
id_admin = 0
id_cliente = 0
id_percurso = 0
id_viagem = 0
id_autocarro = 0

while(1):
    if(menu == -1):
        break

    elif(menu == 0):
        menu, order = menu0()
    
    elif(menu == 1):
        menu, nome, id_cliente = menu1()

    elif(menu == 2):
        menu, nome, id_admin = menu2()

    elif(menu == 3):
        menu, order = menu3()

    elif(menu == 4):
        menu, order = menu4(nome)

    elif(menu == 5):
        menu, order = menu5(nome,order)

    elif(menu == 6):
        menu, order = menu6(nome)

    elif(menu == 7):
        menu, order, id_percurso= menu7(nome,order,id_cliente)

    elif(menu == 8):
        menu, id_viagem, id_autocarro = menu8(id_percurso,id_cliente)

    elif(menu == 9):
        menu, order = menu9(id_viagem,id_autocarro,id_cliente)

    elif(menu == 10):
        menu, order = menu10(nome,order,id_cliente)

    elif(menu == 11):
        menu, order = menu11(nome,order,id_cliente)
    
    elif(menu == 12):
        menu, order = menu12(nome)

    elif(menu == 13):
        menu, order = menu13(nome)
    
    elif(menu == 14):
        menu, order = menu14(nome,order)

    elif(menu == 15):
        menu, order = menu15(nome,order)

    elif(menu == 16):
        menu, order = menu16(nome,order)

    elif(menu == 17):
        menu, order = menu17(nome)

    elif(menu == 18):
        menu, order = menu18(nome,order,id_admin)
    
    elif(menu == 19):
        menu, order = menu19(nome)

    elif(menu == 20):
        menu, order = menu20(nome,order)

    elif(menu == 21):
        menu, order = menu21(nome)

    elif(menu == 22):
        menu, order = menu22(nome,order)