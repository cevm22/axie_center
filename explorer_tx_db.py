from operator import truediv
from pymongo import MongoClient
import datetime
import time
import datetime 
import json

#======================================================================
#parametros de base de datos
#======================================================================
MONGO_URI='mongodb://localhost' #ubicacion DB
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
                })
    return True
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
# COUNT ALL DOCS ERC721
#======================================================================
def count_docs_ERC721():
    db=client['tx_db'] # DB
    collection=db['ERC721'] # Collection     
    data=collection.count_documents({}) 
    return (data) 
#======================================================================
# COUNT ALL DOCS ERC20
#======================================================================
def count_docs_ERC20():
    db=client['tx_db'] # DB
    collection=db['ERC20'] # Collection     
    data=collection.count_documents({}) 
    return (data) 
