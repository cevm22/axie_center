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
        return [total,lista]
    except Exception as e:
        return False

def pull_erc20(ronin):
    try:
        url = 'https://explorer.roninchain.com/api/tokentxs?addr='+str(ronin)+'&from=0&size=100&token=ERC20'
        r = requests.get(url, headers=headers)
        inforequest = r.content
        a=json.loads(inforequest)
        total=(a['total'])
        lista=(a['results'])
        return [total,lista]
    except Exception as e:
        return False
        
#print(pull_erc721(hotwallet))

#estructurar base de datos para guardar las transacciones ERC20 y ERC721
#base de datos para resumen estadisticas del hotwallet
#funcion en caso de que haya mas de 100 txs
#funcion para guardar txs 
