from axie_utils.abis import SLP_ABI
from axie_utils.abis import AXIE_ABI 
from web3 import Web3, exceptions
from time import sleep
from datetime import datetime, timedelta
import config
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36" 
AXIE_CONTRACT = "0x32950db2a7164ae833121501c797d79e7b79d74c"
AXS_CONTRACT = "0x97a9107c1793bc407d6f527b77e7fff4d812bece"
SLP_CONTRACT = "0xa8754b9fa15fc18bb59458815510e40a12cd2014"
WETH_CONTRACT = "0xc99a6a985ed2cac1ef41640596c5a5f9f4e19ef5"
USDC_CONTRACT = "0x0b7007c13325c48911f73a2dad5fa5dcbf808adc"
RONIN_PROVIDER = "https://api.roninchain.com/rpc"
key=config.private_key


def USDC_transfer(from_wallet,to_wallet, value):
        print("get provider")
        w3 = Web3(
            Web3.HTTPProvider(
                RONIN_PROVIDER,
                request_kwargs={"headers": {"content-type": "application/json", "user-agent": USER_AGENT}}))
        amount = int(value) * 1000000
        contract = w3.eth.contract(
            address=Web3.toChecksumAddress(USDC_CONTRACT),
            abi=SLP_ABI)
    
        # Get Nonce
        print("get nonce")
        nonce = get_nonce(from_wallet)#get nonce from wallet ronin 
        # Build transaction
        transaction = contract.functions.transfer(
            Web3.toChecksumAddress(to_wallet),
            amount
        ).buildTransaction({
            "chainId": 2020,
            "gas": 50000, #39020
            "gasPrice":  w3.toWei("1.5", "gwei"),
            "nonce": nonce
        })
        # Sign Transaction
        print("signing transaction")
        signed = w3.eth.account.sign_transaction(
            transaction,
            private_key=key
        )
        # Send raw transaction
        print("sending to blockchain")
        w3.eth.send_raw_transaction(signed.rawTransaction)
        # get transaction hash
        print("waiting for proof hash")
        hash =  w3.toHex( w3.keccak(signed.rawTransaction))
        print(hash)
        # Wait for transaction to finish or timeout
        start_time = datetime.now()
        while True:
            print("waiting to hash")
            # We will wait for max 5minutes for this tx to respond, if it does not, we will re-try
            if datetime.now() - start_time > timedelta(minutes=5):
                success = False
                print("Transaction timed out!")
                break
            try:
                recepit =  w3.eth.get_transaction_receipt(hash)
                if recepit["status"] == 1:
                    success = True
                    print("LISTO")
                else:
                    print("error")
                    success = False
                break
            except exceptions.TransactionNotFound:
                # Sleep 10s while waiting
                sleep(10)
                print("Waiting for transaction  to finish (Nonce:)... " + str(nonce))

        if success:
            print("Transaction  completed! Hash: - " + "Explorer: https://explorer.roninchain.com/tx/"+str(hash) )
        else:
            print("Transaction failed. Trying to replace it with a 0 value tx and re-try.")


def AXIE_transfer(from_wallet,to_wallet, axie_id):
        print("get provider")
        w3 = Web3(
            Web3.HTTPProvider(
                RONIN_PROVIDER,
                request_kwargs={"headers": {"content-type": "application/json", "user-agent": USER_AGENT}}))
        axie_contract = w3.eth.contract(
            address=Web3.toChecksumAddress(AXIE_CONTRACT),
            abi=AXIE_ABI)
    
        # Get Nonce
        print("get nonce")
        nonce = get_nonce(from_wallet)#get nonce from wallet ronin 
        # Build transaction
        transaction = axie_contract.functions.safeTransferFrom(
            Web3.toChecksumAddress(from_wallet),
            Web3.toChecksumAddress(to_wallet),
            axie_id
        ).buildTransaction({
            "chainId": 2020,
            "gas": 130000,
            "from": Web3.toChecksumAddress(from_wallet),
            "gasPrice": w3.toWei("1.5", "gwei"),
            "value": 0,
            "nonce": nonce
        })
        # Sign Transaction
        print("signing transaction")
        signed = w3.eth.account.sign_transaction(
            transaction,
            private_key=key
        )
        # Send raw transaction
        print("sending to blockchain")
        w3.eth.send_raw_transaction(signed.rawTransaction)
        # get transaction hash
        print("waiting for proof hash")
        hash =  w3.toHex( w3.keccak(signed.rawTransaction))
        print(hash)
        # Wait for transaction to finish or timeout
        start_time = datetime.now()
        while True:
            print("waiting to hash")
            # We will wait for max 5minutes for this tx to respond, if it does not, we will re-try
            if datetime.now() - start_time > timedelta(minutes=5):
                success = False
                print("Transaction timed out!")
                break
            try:
                recepit =  w3.eth.get_transaction_receipt(hash)
                if recepit["status"] == 1:
                    success = True
                    print("LISTO")
                else:
                    print("error")
                    success = False
                break
            except exceptions.TransactionNotFound:
                # Sleep 10s while waiting
                sleep(10)
                print("Waiting for transaction  to finish (Nonce:)... " + str(nonce))

        if success:
            print("Transaction  completed! Hash: - " + "Explorer: https://explorer.roninchain.com/tx/"+str(hash) )
        else:
            print("Transaction failed. Trying to replace it with a 0 value tx and re-try.")


def get_nonce(from_wallet):
    w3 = Web3(
            Web3.HTTPProvider(
                RONIN_PROVIDER,
                request_kwargs={
                    "headers": {"content-type": "application/json",
                                "user-agent": USER_AGENT}}))
    nonce = w3.eth.get_transaction_count(
        Web3.toChecksumAddress(from_wallet)
    )
    return nonce


def validate_ronin(address):
    ronin=address.lower()    
    w3 = Web3(
            Web3.HTTPProvider(
                RONIN_PROVIDER,
                request_kwargs={
                    "headers": {"content-type": "application/json",
                                "user-agent": USER_AGENT}}))
    tx = w3.isAddress(ronin.replace("ronin:", "0x")) 
    return tx

def get_tx(tx_hash):
    try:
        w3 = Web3(
                Web3.HTTPProvider(
                    RONIN_PROVIDER,
                    request_kwargs={
                        "headers": {"content-type": "application/json",
                                    "user-agent": USER_AGENT}}))
        tx = w3.eth.get_transaction(tx_hash)
        tx_confirm = w3.eth.get_transaction_receipt(tx_hash)
        if int(tx_confirm.status) == 1:
            tx_contract=str(tx['to'])
            tx_from=str(tx['from'])
            tx_coded=(tx.input)
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

#axie_id_1=4116684
#axie_id_2=32817
ronin='0x1ba2228e2c90bc6cc4fd7c3fe62e796c4321356f'
from_wallet='0xcb0e8315633348f559bc0edf781f53b48c97ebca'

#print(USDC_transfer(from_wallet,ronin,1))