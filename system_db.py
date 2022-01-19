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
# DB CREATE ticket PRIVATE SALE
#======================================================================
def create_ticket_PS(vec):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection
    collection.insert_one({
                "init_time": vec[4],
                "comision": vec[3],
                "end_time": 0,
                "log": "comentarios",
                "ronin_1": "ronin:1ba2228e2c90bc6cc4fd7c3fe62e796c4321356f",
                "ronin_2": "0",
                "tx_hash_1": "0x1",
                "tx_hash_2": "0x2",
                "status_hash_1": False,
                "status_hash_2": False,
                "status_ac_hash_1": False,
                "status_ac_hash_2": False,
                "ticket": vec[0],
                "ticket_stat": 1,
                "token_1": "AXIE",
                "token_2": "USDC",
                "ac_txhash_1": "0",
                "ac_txhash_2": "0",
                "type": "Private Sale",
                "value_1": vec[1], #AXIE id
                "value_2": vec[2], #USDC token
                })
    return
#======================================================================
# DB ENROLL new users
#======================================================================
def enroll_new(vec):
    db=client['users_data'] # DB
    collection=db['user'] # Collection
    collection.insert_one({
                "discord_id": vec[0],
                "tickets_log": 0,
                "ronin": vec[1],
                "ban": False,
                "ban_alltime": 0,
                "num_tickets": 0,
                "num_commands": 0,
                "ticket_open": False,
                "language": "EN"
                })
    return

#======================================================================
# DB change status LANGUAGE
#======================================================================
def change_language(user,lan):
    db=client['users_data'] # DB
    collection=db['user'] # Collection
    data=collection.update_one({'discord_id':user},{"$set":{'language':lan}})
    return data
#======================================================================
# VALIDATE USER enrolled
#======================================================================
def validate_user(user_ID):
    db=client['users_data'] # DB
    collection=db['user'] # Collection     
    data=collection.find_one({"discord_id":user_ID})   
    return data

print("inicio")
#vector=[1642527399,'ronin:1bsdu3s8fnfd7823hdfsfv9'] #enroll func
#vector=["PS-000001",765432,100,2,1642617963] #private sale func

#print(validate_user(164252739))