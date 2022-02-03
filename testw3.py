from datetime import datetime
from json.decoder import JSONDecodeError

from web3 import Web3

from axie_utils.abis import SLP_ABI
from axie_utils.abis import AXIE_ABI 

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36" # noqa
AXIE_CONTRACT = "0x32950db2a7164ae833121501c797d79e7b79d74c"
AXS_CONTRACT = "0x97a9107c1793bc407d6f527b77e7fff4d812bece"
SLP_CONTRACT = "0xa8754b9fa15fc18bb59458815510e40a12cd2014"
WETH_CONTRACT = "0xc99a6a985ed2cac1ef41640596c5a5f9f4e19ef5"
USDC_CONTRACT = "0x0b7007c13325c48911f73a2dad5fa5dcbf808adc"
RONIN_PROVIDER_FREE = "https://proxy.roninchain.com/free-gas-rpc"
RONIN_PROVIDER = "https://api.roninchain.com/rpc"

print("inciando")
ronin=str('0x1ba2228e2c90bc6cc4fd7c3fe62e796c4321356f')

def check_balance(token='slp'):
    if token == 'slp':
        contract = SLP_CONTRACT
    elif token == 'axs':
        contract = AXS_CONTRACT
    elif token == "axies":
        contract = AXIE_CONTRACT
    elif token == "weth":
        contract = WETH_CONTRACT
    else:
        return 0

    w3 = Web3(
            Web3.HTTPProvider(
                RONIN_PROVIDER,
                request_kwargs={
                    "headers": {"content-type": "application/json",
                                "user-agent": USER_AGENT}}))
    ctr = w3.eth.contract(
        address=Web3.toChecksumAddress(contract),
        abi=SLP_ABI
    )
    balance = ctr.functions(
        Web3.toChecksumAddress(account.replace("ronin:", "0x"))
    ).call()
    if token == 'weth':
        return float(balance/1000000000000000000)
    return int(balance)

def get_nonce():
    w3 = Web3(
            Web3.HTTPProvider(
                RONIN_PROVIDER_FREE,
                request_kwargs={
                    "headers": {"content-type": "application/json",
                                "user-agent": USER_AGENT}}))
    nonce = w3.eth.get_transaction_count(
        Web3.toChecksumAddress(ronin)
    )
    return nonce

def validate_ronin(address):
    ronin=address.lower()    
    w3 = Web3(
            Web3.HTTPProvider(
                RONIN_PROVIDER_FREE,
                request_kwargs={
                    "headers": {"content-type": "application/json",
                                "user-agent": USER_AGENT}}))
    tx = w3.isAddress(ronin.replace("ronin:", "0x")) #regres True si es un address valido 
    return tx

def get_tx(tx_hash):
    try:
        w3 = Web3(
                Web3.HTTPProvider(
                    RONIN_PROVIDER_FREE,
                    request_kwargs={
                        "headers": {"content-type": "application/json",
                                    "user-agent": USER_AGENT}}))
        tx = w3.eth.get_transaction(tx_hash)
        tx_confirm = w3.eth.get_transaction_receipt(tx_hash)
        #print(tx_confirm)
        if int(tx_confirm.status) == 1:
            tx_contract=str(tx['to'])
            tx_from=str(tx['from'])
            tx_coded=(tx.input)
            # Agregar filtros por contratos para poder identificar en caso de que hagan un envio de otro asset que no se tiene contemplado
            if tx_contract.lower() == AXIE_CONTRACT.lower():
                ctr = w3.eth.contract(address=Web3.toChecksumAddress(tx_contract), abi=AXIE_ABI)
                vector=AXIE_tx(ctr,tx_coded,tx_contract.lower())
                return vector
            else:
                ctr = w3.eth.contract(address=Web3.toChecksumAddress(tx_contract), abi=SLP_ABI)
                vector=TOKEN_tx(ctr,tx_coded,tx_contract.lower(),tx_from.lower())
                return vector
        else:
            return 'TX_FAIL'
    except Exception as e:
        return "NOT_FOUND"


def AXIE_tx(ctr,tx__input,tx__contract):
    decoded=ctr.decode_function_input(tx__input)
    tx_from=str(decoded[1]['_from']).lower()
    tx_to=str(decoded[1]['_to']).lower()
    tx_tokenID=str(decoded[1]['_tokenId'])
    vector=[tx__contract,tx_from,tx_to,tx_tokenID]
    return vector

def TOKEN_tx(ctr,tx__input,tx__contract,tx__from):
    decoded=ctr.decode_function_input(tx__input)
    tx_to=str(decoded[1]['_to']).lower()
    tx_value=str(decoded[1]['_value']).lower()
    vector=[tx__contract,tx__from,tx_to,tx_value]
    return vector   

#print("tx rechazada")
#print(get_tx('0x1124b6011f9b0014fc956e3b6debff7916551cf2b7a96430b27a99f45c84ede9'))
#print("tx aceptada")
#print(get_tx('0xeffc9c0d2f0e7ef7cc96d85aa1eda34efbda8f4a7245a2a793bda51c6f518095'))
#test("ronin:1ba2228e2c90bc6cc4fd7c3fe62e796c4321356f")