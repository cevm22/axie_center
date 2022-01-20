from axie_utils.abis import SLP_ABI
from axie_utils.abis import AXIE_ABI 
from web3 import Web3

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36" # noqa
AXIE_CONTRACT = "0x32950db2a7164ae833121501c797d79e7b79d74c"
AXS_CONTRACT = "0x97a9107c1793bc407d6f527b77e7fff4d812bece"
SLP_CONTRACT = "0xa8754b9fa15fc18bb59458815510e40a12cd2014"
WETH_CONTRACT = "0xc99a6a985ed2cac1ef41640596c5a5f9f4e19ef5"
USDC_CONTRACT = "0x0b7007c13325c48911f73a2dad5fa5dcbf808adc"
RONIN_PROVIDER_FREE = "https://proxy.roninchain.com/free-gas-rpc"
RONIN_PROVIDER = "https://api.roninchain.com/rpc"

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