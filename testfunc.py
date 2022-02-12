import requests
import json
import explorer_tx_db
import math
import time
import config     

import discord #importamos para conectarnos con el bot
from discord.ext import commands #importamos los comandos
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}


hotwallet=config.hotwallet

#======================================================================
# PULL ERC721 data from api
#======================================================================
def pull_erc721_api(ronin):
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

#======================================================================
# PULL ERC721 data from api
#======================================================================
def pull_erc20_api(ronin):
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

#======================================================================
# PULL ERC721 & ERC20 data from api in case delta > 100 items
#======================================================================
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
                                #buscar por duplicado
                                duplicated=str(lista[i]['tx_hash'])
                                check_Tx=explorer_tx_db.find_duplicate_erc20(duplicated)
                                if check_Tx == False:
                                    explorer_tx_db.add_ERC20_tx(vec_info)
                        if asset =="ERC721":
                                #buscar por duplicado
                                duplicated=str(lista[i]['tx_hash'])
                                check_Tx=explorer_tx_db.find_duplicate_erc721(duplicated)
                                if check_Tx == False:
                                    explorer_tx_db.add_ERC721_tx(vec_info)
        return 
    except Exception as e:
        print(e)
        return False

#======================================================================
# Store items ERC721 & ERC20 to DB
#======================================================================
def store_tx(vec):
    try:
            if vec[0] == "ERC20":
                total=int(explorer_tx_db.pull_docs_erc20())
            if vec[0] == "ERC721":
                total=int(explorer_tx_db.pull_docs_erc721())

            stats_erc20=int(vec[1])
            if total == stats_erc20:
                #print("NO HAY CAMBIOS")
                return False
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
                                #print("pagina " + str(a))
                                #print("Delta > "+str(delta))
                                pull_cycle(ASSET,hotwallet,ind,int(delta))
                                delta=delta-100
                                ind=ind+100
                            if delta > 100:
                                #print("pagina " + str(a))                           
                                #print("Delta > "+str(delta))
                                pull_cycle(ASSET,hotwallet,ind,100)
                                delta=delta-100
                                ind=ind+100
                        ############################3
                        # Funcion para contar documentos y actualizar el status
                        ############################3
                        # Funcion para contar documentos y actualizar el status ERC_20 o ERC721
                        if vec[0] == "ERC20":
                            total_erc20=explorer_tx_db.count_all_docs_ERC20()
                            explorer_tx_db.update_explorer_ERC20_tx(str(total_erc20))
                        if vec[0] == "ERC721":
                            total_erc721=explorer_tx_db.count_all_docs_ERC721()
                            explorer_tx_db.update_explorer_ERC721_tx(str(total_erc721))
                        #print("terminado")
                        return
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
                            #buscar por duplicado
                            duplicated=str(erc20_vec[i]['tx_hash'])
                            check_Tx=explorer_tx_db.find_duplicate_erc20(duplicated)
                            if check_Tx == False:
                                #guardar docs a db
                                explorer_tx_db.add_ERC20_tx(vec_info)
                        if vec[0] == "ERC721":
                            #buscar por duplicado
                            duplicated=str(erc20_vec[i]['tx_hash'])
                            check_Tx=explorer_tx_db.find_duplicate_erc721(duplicated)
                            if check_Tx == False:
                                #guardar docs a db
                                explorer_tx_db.add_ERC721_tx(vec_info)
                    ############################3
                    # Funcion para contar documentos y actualizar el status ERC_20 o ERC721
                    if vec[0] == "ERC20":
                        print("actualizando ERC20")
                        total_erc20=explorer_tx_db.count_all_docs_ERC20()
                        print(total_erc20)
                        explorer_tx_db.update_explorer_ERC20_tx(str(total_erc20))
                    if vec[0] == "ERC721":
                        print("actualizando ERC721")
                        total_erc721=explorer_tx_db.count_all_docs_ERC721()
                        print(total_erc721)
                        explorer_tx_db.update_explorer_ERC721_tx(str(total_erc721))
                    #print("terminado")
                    return
    except Exception as e:
        print(e)
        return False

def test():
    pull_erc20_api(hotwallet)
    pull_erc721_api(hotwallet)
    return

#pull_erc20_api(hotwallet)
#pull_erc721_api(hotwallet)
print(explorer_tx_db.count_docs_ERC721())
#test()