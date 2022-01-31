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