import requests
import json
import explorer_tx_db
import math
import time     
headers = {
        'user-agent': 'Mozilla/5.0 ( Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
hotwallet='0x1ba2228e2c90bc6cc4fd7c3fe62e796c4321356f'

def pull_erc721(ronin):
    try:
        url = 'https://explorer.roninchain.com/api/tokentxs?addr='+str(ronin)+'&from=0&size=100&token=ERC721'
        r = requests.get(url, headers=headers)
        inforequest = r.content
        a=json.loads(inforequest)
        total=(a['total'])
        lista=(a['results'])
        vec=["ERC721",total,lista]
        store_tx(vec)
        return 
        
    except Exception as e:
        print(e)
        return False

def pull_erc20(ronin):
    try:
        url = 'https://explorer.roninchain.com/api/tokentxs?addr='+str(ronin)+'&from=0&size=100&token=ERC20'
        r = requests.get(url, headers=headers)
        inforequest = r.content
        a=json.loads(inforequest)
        total=(a['total'])
        lista=(a['results'])
        vec= ["ERC20",total,lista]
        store_tx(vec)
        return 
    except Exception as e:
        print(e)
        return False

def pull_cycle(tech,ronin,ind,size):
    try:
        time.sleep(5)
        if tech == 'ERC20':
            url = 'https://explorer.roninchain.com/api/tokentxs?addr='+str(ronin)+'&from='+str(ind) +'&size=100&token=ERC20'
            asset="ERC20"
        if tech == 'ERC721':
            url = 'https://explorer.roninchain.com/api/tokentxs?addr='+str(ronin)+'&from='+str(ind) +'&size=100&token=ERC721'
            asset="ERC721"

        r = requests.get(url, headers=headers)
        inforequest = r.content
        a=json.loads(inforequest)
        lista=(a['results'])
        #funcion para guardar documentos en DB TX ERC
        for i in range(size):
                        vec_info=[
                            lista[i]['from'],
                            lista[i]['to'],
                            lista[i]['value'],
                            lista[i]['log_index'],
                            lista[i]['tx_hash'],
                            lista[i]['block_number'],
                            lista[i]['timestamp'],
                            lista[i]['token_address'],
                            lista[i]['token_symbol'],
                            ]
                        if asset =="ERC20":
                                explorer_tx_db.add_ERC20_tx(vec_info)
                        if asset =="ERC721":
                                explorer_tx_db.add_ERC721_tx(vec_info)
                        #
                        #revisar duplicidad
                        #duplicated=str(lista[i]['tx_hash'])
                        #check_Tx=explorer_tx_db.test_duplicate(duplicated)
                        #if check_Tx == False:
                        #    if asset =="ERC20":
                        #        explorer_tx_db.add_ERC20_tx(vec_info)
                        #    if asset =="ERC721":
                        #        explorer_tx_db.add_ERC721_tx(vec_info)
                        #if check_Tx == True:
                        #    explorer_tx_db.add_ERC20_tx(vec_info)
                        #    print("REPETIDO > " + str(duplicated))
        return 
    except Exception as e:
        print(e)
        return False

def store_tx(vec):
    try:
            total=0 #func para pull ERC20_Tx status
            stats_erc20=int(vec[1])
            if total == stats_erc20:
                print("NO HAY CAMBIOS")
                return 
            else:
                delta=stats_erc20-total
                print("Hay diferencia de > "+str(delta))
                erc20_vec=vec[2]
                if delta > 100:
                    if delta % 100 == 0:
                        pag= int(delta/100)
                    else:
                        pag=math.floor(delta/100) + 1
                        ind=0
                        #COLOCAR IF PARA IDENTIFICAR ERC20 Y ERC721
                        if vec[0] == "ERC20":
                            ASSET="ERC20"
                        if vec[0] == "ERC721":
                            ASSET="ERC721"
                        for a in range(pag):
                            #caso cuando se necesiten los 100 items 
                            if delta < 101:
                                print("pagina " + str(a))
                                print("Delta > "+str(delta))
                                pull_cycle(ASSET,hotwallet,ind,int(delta))
                                delta=delta-100
                                ind=ind+100
                            if delta > 100:
                                print("pagina " + str(a))                           
                                print("Delta > "+str(delta))
                                pull_cycle(ASSET,hotwallet,ind,100)
                                delta=delta-100
                                ind=ind+100
                        ############################3
                        # Funcion para contar documentos y actualizar el status
                else:                    
                    for i in range(delta):
                        #agegar funcion para guardar los documentos
                        vec_info=[
                            erc20_vec[i]['from'],
                            erc20_vec[i]['to'],
                            erc20_vec[i]['value'],
                            erc20_vec[i]['log_index'],
                            erc20_vec[i]['tx_hash'],
                            erc20_vec[i]['block_number'],
                            erc20_vec[i]['timestamp'],
                            erc20_vec[i]['token_address'],
                            erc20_vec[i]['token_symbol'],
                            ]
                        if vec[0] == "ERC20":
                            explorer_tx_db.add_ERC20_tx(vec_info)
                        if vec[0] == "ERC721":
                            explorer_tx_db.add_ERC721_tx(vec_info)
                        
                        print(i)
                    print("terminado")
                    ############################3
                    # Funcion para contar documentos y actualizar el status
                    #agregar funcion actualizar stats en ERC_20 o ERC721
                    return
    except Exception as e:
        print(e)
        return False

def test():
    if 800 % 100 == 0:
        print("par")
    else:
        print("impar")

#pull_erc20(hotwallet)
pull_erc721(hotwallet)
#test()
#estructurar base de datos para guardar las transacciones ERC20 y ERC721
#base de datos para resumen estadisticas del hotwallet
#funcion en caso de que haya mas de 100 txs
#funcion para guardar txs 
