from pymongo import MongoClient
import time
import json
from datetime import datetime
import config
#======================================================================
#parametros de base de datos
#======================================================================
MONGO_URI=config.db_uri#'mongodb://localhost' #ubicacion DB
client = MongoClient(MONGO_URI) #inicializacion de la base datos
#======================================================================
# DB CREATE txs explorer stats
#======================================================================
def create_explorer_stats_db():
    db=client['tx_db'] # DB
    collection=db['explorer_stats'] # Collection
    collection.insert_one({
                "txs":"txs",
                "ERC20_tx": 0,
                "ERC721_tx": 0,
                })
    return True
#======================================================================
# exist   explorer_stats 
#======================================================================
def find_stats_exists():
    db=client['tx_db'] # DB
    collection=db['explorer_stats'] # Collection
    data=collection.find_one({'txs':"txs"})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE   explorer_stats - ERC20_tx new total_tx
#======================================================================
def update_explorer_ERC20_tx(total_tx):
    db=client['tx_db'] # DB
    collection=db['explorer_stats'] # Collection
    data=collection.update_one({'txs':"txs"},{"$set":{"ERC20_tx":total_tx}})
    return True

#======================================================================
# UPDATE   explorer_stats - ERC721_tx new total_tx
#======================================================================
def update_explorer_ERC721_tx(total_tx):
    db=client['tx_db'] # DB
    collection=db['explorer_stats'] # Collection
    data=collection.update_one({'txs':"txs"},{"$set":{"ERC721_tx":total_tx}})
    return True

#======================================================================
# UPDATE   ERC721_tx  ticket info and status = PASS
#======================================================================
def update_ERC721_tx_ticket_status_pass(ticket,proof_hash):
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection
    data=collection.update_one({'tx_hash':proof_hash},{"$set":{"ticket_id":ticket, "status":'PASS'}})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE   ERC20_tx  ticket info and status = PASS
#======================================================================
def update_ERC20_tx_ticket_status_pass(ticket,proof_hash):
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection
    data=collection.update_one({'tx_hash':proof_hash},{"$set":{"ticket_id":ticket, "status":'PASS'}})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE_MANY   ERC721_tx   and status = STAND_BY
#======================================================================
def update_ERC721_tx_all_standby_from_notfound():
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection
    data=collection.update_many({'status':'TX_NOT_FOUND'},{"$set":{"status":'STAND_BY'}})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE_MANY   ERC20_tx   and status = STAND_BY
#======================================================================
def update_ERC20_tx_all_standby_from_notfound():
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection
    data=collection.update_many({'status':'TX_NOT_FOUND'},{"$set":{"status":'STAND_BY'}})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE   ERC721_tx  ticket info and status = CANCEL_PENDING
#======================================================================
def update_ERC721_tx_ticket_status_cancel_pending(ticket,proof_hash):
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection
    data=collection.update_one({'tx_hash':proof_hash},{"$set":{"ticket_id":ticket, "status":'CANCEL_PENDING'}})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE   ERC20_tx  ticket info and status = CANCEL_PENDING
#======================================================================
def update_ERC20_tx_ticket_status_cancel_pending(ticket,proof_hash):
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection
    data=collection.update_one({'tx_hash':proof_hash},{"$set":{"ticket_id":ticket, "status":'CANCEL_PENDING'}})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE   ERC721_tx  ticket info and status = PENDING_TRACK
#======================================================================
def update_ERC721_tx_pending_track(proof_hash):
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection
    data=collection.update_one({'tx_hash':proof_hash},{"$set":{"status":'PENDING_TRACK'}})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE   ERC20_tx  ticket info and status = PENDING_TRACK
#======================================================================
def update_ERC20_tx_pending_track(proof_hash):
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection
    data=collection.update_one({'tx_hash':proof_hash},{"$set":{"status":'PENDING_TRACK'}})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE   ERC721_tx  ticket info and status = STAND_BY
#======================================================================
def update_ERC721_tx_stand_by(proof_hash):
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection
    data=collection.update_one({'tx_hash':proof_hash},{"$set":{"status":'STAND_BY'}})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE   ERC20_tx  ticket info and status = STAND_BY
#======================================================================
def update_ERC20_tx_stand_by(proof_hash):
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection
    data=collection.update_one({'tx_hash':proof_hash},{"$set":{"status":'STAND_BY'}})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE   ERC721_tx  ticket info and status = TX_NOT_FOUND
#======================================================================
def update_ERC721_tx_not_found(proof_hash):
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection
    data=collection.update_one({'tx_hash':proof_hash},{"$set":{"status":'TX_NOT_FOUND'}})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE   ERC20_tx  ticket info and status = TX_NOT_FOUND
#======================================================================
def update_ERC20_tx_not_found(proof_hash):
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection
    data=collection.update_one({'tx_hash':proof_hash},{"$set":{"status":'TX_NOT_FOUND'}})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE   ERC721_tx  ticket info and status = REFUND
#======================================================================
def update_ERC721_tx_ticket_status_refund(ticket,proof_hash,refund_hash):
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection
    data=collection.update_one({'tx_hash':proof_hash},{"$set":{"ticket_id":ticket, "status":'REFUND','refund_hash':refund_hash}})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE   ERC20_tx  ticket info and status = REFUND
#======================================================================
def update_ERC20_tx_ticket_status_refund(ticket,proof_hash,refund_hash):
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection
    data=collection.update_one({'tx_hash':proof_hash},{"$set":{"ticket_id":ticket, "status":'REFUND','refund_hash':refund_hash}})
    if not data:
        return False
    else:
        return True
    
#======================================================================
# UPDATE   ERC721_tx  ticket info and status = REFUND_DONE
#======================================================================
def update_ERC721_tx_ticket_status_refund_done(ticket,proof_hash):
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection
    data=collection.update_one({'tx_hash':proof_hash},{"$set":{"ticket_id":ticket, "status":'REFUND_DONE'}})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE   ERC20_tx  ticket info and status = REFUND_DONE
#======================================================================
def update_ERC20_tx_ticket_status_refund_done(ticket,proof_hash):
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection
    data=collection.update_one({'tx_hash':proof_hash},{"$set":{"ticket_id":ticket, "status":'REFUND_DONE'}})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE   ERC721_tx  ticket info and status = REFUND_DONE
#======================================================================
def update_ERC721_tx_ticket_status_refund_done_2(proof_hash):
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection
    data=collection.update_one({'tx_hash':proof_hash},{"$set":{"status":'REFUND_DONE'}})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE   ERC20_tx  ticket info and status = REFUND_DONE
#======================================================================
def update_ERC20_tx_ticket_status_refund_done_2(proof_hash):
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection
    data=collection.update_one({'tx_hash':proof_hash},{"$set":{"status":'REFUND_DONE'}})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE   ERC721_tx  ticket info and status = INVALID_CONTRACT
#======================================================================
def update_ERC721_tx_invalid_contract(proof_hash):
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection
    data=collection.update_one({'tx_hash':proof_hash},{"$set":{"status":'INVALID_CONTRACT'}})
    if not data:
        return False
    else:
        return True
#======================================================================
# UPDATE   ERC20_tx  ticket info and status = INVALID_CONTRACT
#======================================================================
def update_ERC20_tx_invalid_contract(proof_hash):
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection
    data=collection.update_one({'tx_hash':proof_hash},{"$set":{"status":'INVALID_CONTRACT'}})
    if not data:
        return False
    else:
        return True
#======================================================================
# ADD txs explorer ERC721
#======================================================================
def add_ERC721_tx(vec):
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection
    collection.insert_one({
                "from":str(vec[0]),
                "to":str(vec[1]),
                "value":str(vec[2]),
                "log_index":str(vec[3]),
                "tx_hash":str(vec[4]),
                "block_number":str(vec[5]),
                "timestamp":str(vec[6]),
                "token_address":str(vec[7]),
                "token_symbol":str(vec[8]),
                "ticket_id":0,
                "status":"STAND_BY", #STAND_BY, DONE #faltan agregar otros status para control
                'created':str(int(datetime.timestamp(datetime.utcnow())))
                })
    return True
#======================================================================
# ADD txs explorer ERC20
#======================================================================
def add_ERC20_tx(vec):
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection
    collection.insert_one({
                "from":str(vec[0]),
                "to":str(vec[1]),
                "value":str(vec[2]),
                "log_index":str(vec[3]),
                "tx_hash":str(vec[4]),
                "block_number":str(vec[5]),
                "timestamp":str(vec[6]),
                "token_address":str(vec[7]),
                "token_symbol":str(vec[8]),
                "ticket_id":0,
                "status":"STAND_BY", #STAND_BY, DONE #faltan agregar otros status para control
                'created':str(int(datetime.timestamp(datetime.utcnow())))
                })
    return True
#======================================================================
# ADD txs explorer ERC20
#======================================================================
def add_ERC20_tx_profits(vec):
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection
    collection.insert_one({
                "from":str(vec[0]),
                "to":str(vec[1]),
                "value":str(vec[2]),
                "log_index":str(vec[3]),
                "tx_hash":str(vec[4]),
                "block_number":str(vec[5]),
                "timestamp":str(vec[6]),
                "token_address":str(vec[7]),
                "token_symbol":str(vec[8]),
                "ticket_id":str(vec[9]),
                "status":str(vec[10]), #STAND_BY, DONE #faltan agregar otros status para control
                'created':str(int(datetime.timestamp(datetime.utcnow())))
                })
    return True
#======================================================================
# PULL total docs in ERC721
#======================================================================
def pull_docs_erc721():
    db=client['tx_db'] # DB
    collection=db['explorer_stats'] # Collection     
    data=collection.find_one({"txs":"txs"},{"ERC721_tx":1})
    return data["ERC721_tx"]
#======================================================================
# PULL total docs in ERC20
#======================================================================
def pull_docs_erc20():
    db=client['tx_db'] # DB
    collection=db['explorer_stats'] # Collection     
    data=collection.find_one({"txs":"txs"},{"ERC20_tx":1})
    return data["ERC20_tx"]

#======================================================================
# PULL TX_HASH ERC721 info
#======================================================================
def pull_erc721_info(tx_hash):
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection     
    data=collection.find_one({"tx_hash":tx_hash})
    if not data:
        return False
    else:
        return data
#======================================================================
# PULL TX_HASH ERC20 info
#======================================================================
def pull_erc20_info(tx_hash):
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection     
    data=collection.find_one({"tx_hash":tx_hash})
    if not data:
        return False
    else:
        return data
#======================================================================
# search for Duplications in TX_HASH ERC721
#======================================================================
def find_duplicate_erc721(tx_hash):
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection     
    data=collection.find_one({"tx_hash":tx_hash})
    if not data:
        return False
    else:
        return True
#======================================================================
# search for Duplications in TX_HASH ERC20
#======================================================================
def find_duplicate_erc20(tx_hash):
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection     
    data=collection.find_one({"tx_hash":tx_hash})
    if not data:
        return False
    else:
        return True
#======================================================================
# search  in TX_HASH ERC721 and pull status PASS
#======================================================================
def pull_status_pass_erc721(tx_hash):
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection     
    data=collection.find_one({"tx_hash":tx_hash},{"status":1})
    if not data:
        return False
    else:
        return data["status"]

#======================================================================
# search  TX_HASH ERC20 - and pull status PASS
#======================================================================
def pull_status_pass_erc20(tx_hash):
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection     
    data=collection.find_one({"tx_hash":tx_hash},{"status":1})
    if not data:
        return False
    else:
        return data["status"]

#======================================================================
# COUNT ALL DOCS ERC721 
#======================================================================
def count_all_docs_ERC721():
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection     
    data=collection.count_documents({}) 
    return data
#======================================================================
# COUNT ALL DOCS ERC20
#======================================================================
def count_all_docs_ERC20():
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection     
    data=collection.count_documents({}) 
    return data 

#======================================================================
# COUNT  ERC721 in STAND_BY
#======================================================================
def count_docs_ERC721():
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection     
    data=collection.count_documents({"status":"STAND_BY"}) 
    return data 
#======================================================================
# COUNT  ERC20 in STAND_BY
#======================================================================
def count_docs_ERC20():
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection     
    data=collection.count_documents({"status":"STAND_BY"}) 
    return data
#======================================================================
# pull  TX_HASH ERC20 - and pull data TX_hash
#======================================================================
def pull_txhash_standby_erc20():
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection     
    data=collection.find_one({"status":"STAND_BY"})
    return data['tx_hash']
#======================================================================
# pull  TX_HASH ERC721 - and pull data TX_hash
#======================================================================
def pull_txhash_standby_erc721():
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection     
    data=collection.find_one({"status":"STAND_BY"})
    return data['tx_hash']

#======================================================================
# pull  TX_HASH ERC20 - and pull all data
#======================================================================
def pull_txhash_standby_erc20_data():
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection     
    data=collection.find_one({"status":"STAND_BY"})
    return data
#======================================================================
# pull  TX_HASH ERC721 - and pull all data
#======================================================================
def pull_txhash_standby_erc721_data():
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection     
    data=collection.find_one({"status":"STAND_BY"})
    return data
#======================================================================
# COUNT  ERC721 in REFUND
#======================================================================
def count_docs_ERC721_refund():
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection     
    data=collection.count_documents({"status":"REFUND"}) 
    return data 
#======================================================================
# COUNT  ERC20 in REFUND
#======================================================================
def count_docs_ERC20_refund():
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection     
    data=collection.count_documents({"status":"REFUND"}) 
    return data

#======================================================================
# pull  TX_HASH ERC20 - and pull data with REFUND status
#======================================================================
def pull_txhash_refund_erc20():
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection     
    data=collection.find_one({"status":"REFUND"})
    return data
#======================================================================
# pull  TX_HASH ERC721 - and pull datadata with REFUND status
#======================================================================
def pull_txhash_refund_erc721():
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection     
    data=collection.find_one({"status":"REFUND"})
    return data

#======================================================================
# pull  TX_HASH ERC20 - and pull data with REFUND_hash created
#======================================================================
def pull_refund_hash_created_erc20(tx):
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection     
    data=collection.find_one({"refund_hash":tx})
    if not data:
        return False
    else:
        return True
#======================================================================
# pull  TX_HASH ERC721 - and pull datadata with REFUND_hash created
#======================================================================
def pull_refund_hash_created_erc721(tx):
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection     
    data=collection.find_one({"refund_hash":tx})
    if not data:
        return False
    else:
        return True