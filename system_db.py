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
                "discord_id_1":vec[5],
                "discord_id_2":0,
                "log": "comentarios",
                "ronin_1": vec[7],
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
                "ac_txhash_1": "ac1",
                "ac_txhash_2": "ac2",
                "type": "Private Sale",
                "value_1": vec[1], #AXIE id
                "value_2": vec[2], #USDC token
                "password":vec[6]
                })
    return

#======================================================================
# FIND USER ronin wallet
#======================================================================
def pull_ronin_wallet(discord_id):
    db=client['users_data'] # DB
    collection=db['user'] # Collection     
    data=collection.find_one({"discord_id":discord_id},{"ronin":1})
    return data['ronin']

#======================================================================
# VALIDATE USERS_TICKET in pending/opened
#======================================================================
def user_ticket_opened(user_ID):
    db=client['users_data'] # DB
    collection=db['user'] # Collection     
    data=collection.find_one({"discord_id":user_ID},{"ticket_open":1, "ticket_last":1}) 
    return [data["ticket_open"],data["ticket_last"]]
#======================================================================
# UPDATE  ticket_last y ticket_status
#======================================================================
def update_ticket_last_status(user,ticket_id):
    db=client['users_data'] # DB
    collection=db['user'] # Collection
    data=collection.update_one({'discord_id':user},{"$set":{"ticket_open":True, "ticket_last":ticket_id}})
    return True
#======================================================================
# UPDATE  to cancel tickets in user DB
#======================================================================
def update_cancel_ticket(user):
    db=client['users_data'] # DB
    collection=db['user'] # Collection
    data=collection.update_one({'discord_id':user},{"$set":{"ticket_open":False}})
    return True
#======================================================================
# UPDATE  to cancel ticket ID in ticket DB
#======================================================================
def update_cancel_ticket_ID(ticket):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection
    data=collection.update_one({'ticket':ticket},{"$set":{"ticket_stat":0}})
    return True
#======================================================================
# UPDATE  to ONGOING ticket ID in ticket DB
#======================================================================
def update_ongoing_ticket_ID(ticket):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection
    data=collection.update_one({'ticket':ticket},{"$set":{"ticket_stat":2}})
    return True

#======================================================================
# UPDATE  to DONE ticket ID in ticket DB
#======================================================================
def update_done_ticket_ID(ticket):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection
    data=collection.update_one({'ticket':ticket},{"$set":{"ticket_stat":4}})
    return True

#======================================================================
# UPDATE  to CLOSE ticket ID in ticket DB
#======================================================================
def update_close_ticket_ID(ticket):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection
    data=collection.update_one({'ticket':ticket},{"$set":{"ticket_stat":5}})
    return True
#======================================================================
# UPDATE  to SEND_MSG_TICKET_CLOSED ID in ticket DB
#======================================================================
def update_send_msg_ticket_ID(ticket):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection
    data=collection.update_one({'ticket':ticket},{"$set":{"ticket_stat":6}})
    return True
#======================================================================
# UPDATE to PASS ticket ID in ticket DB
#======================================================================
def update_pass_ticket_ID(ticket):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection
    data=collection.update_one({'ticket':ticket},{"$set":{"ticket_stat":9}})
    return True
#======================================================================
# UPDATE mark TRUE for discordID
#======================================================================
def update_mark_discordID_1(ticket):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection
    data=collection.update_one({'ticket':ticket},{"$set":{"status_hash_1":True}})
    return True
#======================================================================
# UPDATE mark TRUE for discordID_2
#======================================================================
def update_mark_discordID_2(ticket):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection
    data=collection.update_one({'ticket':ticket},{"$set":{"status_hash_2":True}})
    return True
#======================================================================
# UPDATE  tickets status and discord_id_2
#======================================================================
def update_ticket_status_discordID2_ronin(ticket_id,discord_id_2,ronin):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection
    data=collection.update_one({'ticket':ticket_id},{"$set":{"ticket_stat":2, "discord_id_2":discord_id_2, "ronin_2":ronin}})
    return True
#======================================================================
# validate_user2 if ticket was accepted by USER 2
#======================================================================
def validate_user2_accepted(ticket):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection
    data=collection.find_one({'ticket':ticket},{"ticket_stat":1})
    return data["ticket_stat"]
#======================================================================
# FIND USER 2 in ongoing ticket, after accepted the private sale
#======================================================================
def pull_user2(ticket):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection     
    data=collection.find_one({"ticket":ticket},{"discord_id_2":1})
    return data['discord_id_2']
#======================================================================
# FIND USER 1 in ongoing ticket, after accepted the private sale
#======================================================================
def pull_user_seller(ticket):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection     
    data=collection.find_one({"ticket":ticket},{"discord_id_1":1})
    return data['discord_id_1']
#======================================================================
# FIND ticket and pull all data for ticket review
#======================================================================
def pull_ticket_allinfo(ticket):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection     
    data=collection.find_one({"ticket":ticket})
    return data
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
                "ticket_open": 0,
                "ticket_last":"0",
                "language": "EN"
                })
    return True

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
#======================================================================
# VALIDATE RONIN enrolled before
#======================================================================
def validate_ronin(ronin):
    db=client['users_data'] # DB
    collection=db['user'] # Collection     
    data=collection.find_one({"ronin":ronin})   
    return data
#======================================================================
# VALIDATE USER not banned
#======================================================================
def user_gotban(user_ID):
    db=client['users_data'] # DB
    collection=db['user'] # Collection     
    data=collection.find_one({"discord_id":user_ID},{"ban":1}) 
    return data['ban']
#======================================================================
# FIND USER ban count
#======================================================================
def user_ban_count(user_ID):
    db=client['users_data'] # DB
    collection=db['user'] # Collection     
    data=collection.find_one({"discord_id":user_ID},{"ban_alltime":1})
    return data['ban_alltime']
#======================================================================
# FIND tickets stats
#======================================================================
def pull_tickets_stats_total():
    db=client['tx_db'] # DB
    collection=db['tickets_stats'] # Collection     
    data=collection.find_one({"stats_db":"stats"},{"total":1})
    return data['total']
#======================================================================
# FIND tickets id status
#======================================================================
def pull_ticket_id(ticket):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection 
    exist_item=  collection.count_documents({"ticket":ticket})  
    if exist_item == 1:
        data=collection.find_one({"ticket":ticket},{"ticket_stat":1})
        return [True,data['ticket_stat']]
    else:
        return [False]
#======================================================================
# FIND tickets discords ID for user 1 and 2
#======================================================================
def pull_discords_ID_on_ticket(ticket):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection 
    data=collection.find_one({"ticket":ticket},{"discord_id_1":1})
    ID_2=collection.find_one({"ticket":ticket},{"discord_id_2":1})
    return [data['discord_id_1'],ID_2["discord_id_2"]]
#======================================================================
# FIND ticket password
#======================================================================
def pull_ticket_password(ticket):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection   
    data=collection.find_one({"ticket":ticket},{"password":1})
    return data['password']
#======================================================================
# CREATE tickets DB stats
#======================================================================
def create_tickets_stats_db():
    db=client['tx_db'] # DB
    collection=db['tickets_stats'] # Collection
    collection.insert_one({
                    "stats_db":"stats",
                    "total":0,
                    "canceled":0,
                    "done":0
                })
    return True
#======================================================================
# UPDATE   ticket_status - Total +1
#======================================================================
def update_tickets_stats():
    db=client['tx_db'] # DB
    collection=db['tickets_stats'] # Collection
    data=collection.update_one({'stats_db':"stats"},{"$inc":{"total":+1}})
    return True

#======================================================================
# UPDATE  ticket_status -  Cancelled +1 
#======================================================================
def update_tickets_stats_cancelled():
    db=client['tx_db'] # DB
    collection=db['tickets_stats'] # Collection
    data=collection.update_one({'stats_db':"stats"},{"$inc":{"canceled":+1}})
    return True

#======================================================================
# UPDATE  ticket_status -  DONE +1 
#======================================================================
def update_tickets_stats_done():
    db=client['tx_db'] # DB
    collection=db['tickets_stats'] # Collection
    data=collection.update_one({'stats_db':"stats"},{"$inc":{"done":+1}})
    return True
#======================================================================
# UPDATE  proof hash discord_ID_1
#======================================================================
def update_hash_user_1(ticket,proof_hash):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection
    data=collection.update_one({'ticket':ticket},{"$set":{"tx_hash_1":proof_hash}})
    return True

#======================================================================
# UPDATE  proof hash discord_ID_2
#======================================================================
def update_hash_user_2(ticket,proof_hash):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection
    data=collection.update_one({'ticket':ticket},{"$set":{"tx_hash_2":proof_hash}})
    return True

#======================================================================
# UPDATE  proof hash status_ac_hash_1 to False or True
#======================================================================
def update_ac_hash_1_stat(ticket,stat):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection3
    data=collection.update_one({'ticket':ticket},{"$set":{"status_ac_hash_1":stat}})
    return True
#======================================================================
# UPDATE  proof hash status_ac_hash_2 False or True
#======================================================================
def update_ac_hash_2_stat(ticket,stat):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection
    data=collection.update_one({'ticket':ticket},{"$set":{"status_ac_hash_2":stat}})
    return True

#======================================================================
# UPDATE  proof hash ac_txhash_1 
#======================================================================
def update_ac_txhash_1(ticket,proof_hash):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection3
    data=collection.update_one({'ticket':ticket},{"$set":{"ac_txhash_1":proof_hash}})
    return True
#======================================================================
# UPDATE  proof hash ac_txhash_2
#======================================================================
def update_ac_txhash_2(ticket,proof_hash):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection
    data=collection.update_one({'ticket':ticket},{"$set":{"ac_txhash_2":proof_hash}})
    return True

#======================================================================
# VERIFY owners send proof_hash correct and change ticket_stat = 3
#======================================================================
def verify_assets_in_hotwallet():
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection
    data=collection.update_many({"$and":[{"ticket_stat":2},{"status_hash_1":True},{"status_hash_2":True}]},
                                { "$set": { "ticket_stat":3 } })
    return True
#======================================================================
# VERIFY tx hash is IN TICKET db
#======================================================================
def verify_hash_in_ticket(hash):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection
    data=collection.find_one({"$or":[{"tx_hash_1":hash},{"tx_hash_2":hash},{"ac_txhash_1":hash},{"ac_txhash_2":hash}]})
    return data
#======================================================================
# PULL total of tickets in status PENDING = 3
#======================================================================
def tickets_pending():
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection 
    data = collection.count_documents({"ticket_stat":3})  
    return data
#======================================================================
# PULL total of tickets in status DONE = 4
#======================================================================
def tickets_done():
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection 
    data = collection.count_documents({"ticket_stat":4})  
    return data
#======================================================================
# FIND one ticket with ticket_stat = 4 and pull info to send assets
#======================================================================
def pull_ticket_done():
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection 
    data = collection.find_one({"ticket_stat":4})  
    return data
#======================================================================
# FIND one ticket with ticket_stat = 5 and pull info 
#======================================================================
def pull_ticket_closed():
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection 
    data = collection.find_one({"ticket_stat":5})  
    return data
#======================================================================
# FIND one ticket with ticket_stat = 3 and pull info to send assets
#======================================================================
def pull_ticket_ready():
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection 
    data = collection.find_one({"ticket_stat":3})  
    return [data["ticket"],data["ronin_1"],data["ronin_2"],data["value_1"],data["value_2"]]
#======================================================================
# FIND status_ac_hash_1 and 2 status
#======================================================================
def pull_ticket_status_ac(ticket):
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection 
    data = collection.find_one({"ticket":ticket})  
    return [data["status_ac_hash_1"],data["status_ac_hash_2"]]
#======================================================================
# Reset all tickets with errors to pending again
#======================================================================
def reset_ticket_stat_to_pending():
    db=client['tx_db'] # DB
    collection=db['tickets'] # Collection
    data=collection.update_many({"ticket_stat":9},
                                { "$set": { "ticket_stat":3 } })
    return True

# Funcion para enviar assets a los owners correspondientes (quitando la comision)
# Funcion enviar comision a otra wallet
# Funcion guardar proof hash en ticket status
# Funcion actualizar all ticket status
# Funcion cerrar ticket
# Funcion Enviar mensaje a los dos Owners de que sus assets se han enviado