import requests
import json

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
        return ["ERC721",total,lista]
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


def store_tx(vec):
    try:
        if vec[0] == "ERC20":
            total=750 #func para pull ERC20_Tx status
            stats_erc20=int(vec[1])
            if total == stats_erc20:
                print("NO HAY CAMBIOS")
                return 
            else:
                delta=stats_erc20-total
                print("Hay diferencia de > "+str(delta))
                erc20_vec=vec[2]
                size=delta#len(erc20_vec)
                for i in range(size):
                    #agegar funcion para guardar los documentos
                    #print(erc20_vec[i])
                    print(i)
                print("terminado")
                #agregar funcion actualizar stats en ERC_20 o ERC721

                return
        return True
    except Exception as e:
        print(e)
        return False

pull_erc20(hotwallet)

#estructurar base de datos para guardar las transacciones ERC20 y ERC721
#base de datos para resumen estadisticas del hotwallet
#funcion en caso de que haya mas de 100 txs
#funcion para guardar txs 
