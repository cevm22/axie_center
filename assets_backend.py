import blockchain_func
import system_db
import config
import explorer_tx_db
hotwallet=config.hotwallet

def send_assets():
    #system_db.reset_ticket_stat_to_pending()
    # obtener num de ticket_stat = 3 (ready)
    ready=system_db.tickets_pending()
    for i in range(ready):
        # obtener data del primer ticket con stat 3
        item=system_db.pull_ticket_ready()
        #[data["ticket"],data["ronin_1"],data["ronin_2"],data["value_1"],data["value_2"]]
        ticket=item[0]
        seller=str(item[1].replace("ronin:", "0x"))
        buyer=str(item[2].replace("ronin:", "0x"))
        AXIE_id=int(item[3])
        USDC_asset=int(item[4])
        
        
        #funcion para obtener hash
        status_hash_AC=system_db.pull_ticket_status_ac(ticket) 
        
        if status_hash_AC[0] == False:
            #flujo enviar asset USDC al vendedor
            # send USDC to ronin_1 the value_2
            send_USDC=blockchain_func.USDC_transfer(hotwallet,seller,USDC_asset)####################
            if send_USDC == False or send_USDC=="TIME_OUT":
                system_db.update_pass_ticket_ID(ticket)
            else:
                #actualizar status_ac_hash_1
                system_db.update_ac_hash_1_stat(ticket,True)
                system_db.update_ac_txhash_1(ticket,send_USDC)
                
        
        if status_hash_AC[1] == False:
            # flujo enviar axie al comprador
            # send AXIE to ronin_2 the value_1
            send_AXIE=blockchain_func.AXIE_transfer(hotwallet,buyer,AXIE_id)####################
            if send_AXIE == False or send_AXIE=="TIME_OUT":
                system_db.update_pass_ticket_ID(ticket)
            else:
                #actualizar status_ac_hash_2
                system_db.update_ac_hash_2_stat(ticket,True)
                system_db.update_ac_txhash_2(ticket,send_AXIE)
                
        #funcion para obtener hash
        confirm_status_hash_AC=system_db.pull_ticket_status_ac(ticket) 
        #print(confirm_status_hash_AC)
        if confirm_status_hash_AC[0] ==True and confirm_status_hash_AC[1]==True:
            # Cerrar ticket como COMPLETADO
            # Enviar Msg al buyer y seller que todo esta correcto
            print(item)
            system_db.update_done_ticket_ID(ticket)
            print("COMPLETADO")
        else:
            print(item)
            # Cambiar a status PASS = 9, para CASO DE NO COMPLETARSE EL ENVIO DE AC -> OWNERS
            system_db.update_pass_ticket_ID(item[0])
            print("ERROR")
           
    print("ready count > "+str(ready))
    # agregar funcion para registrar tx desde los tickets a los logs ERC20 y ERC721 
    return


def cross_tickets_to_api():
    #tickets_done=system_db.tickets_done()
    erc20_standby=explorer_tx_db.count_docs_ERC20()
    erc721_standby=explorer_tx_db.count_docs_ERC721()
    for i in range(erc20_standby):
        try:
            hash=explorer_tx_db.pull_txhash_standby_erc20()
            data=system_db.verify_hash_in_ticket(hash)
            explorer_tx_db.update_ERC20_tx_ticket_status_pass(data["ticket"],hash)
        except:
            pass
    for i in range(erc721_standby):
        try:
            hash=explorer_tx_db.pull_txhash_standby_erc721()
            data=system_db.verify_hash_in_ticket(hash)
            explorer_tx_db.update_ERC721_tx_ticket_status_pass(data["ticket"],hash) 
        except:
            pass
    #funcion para cambiar los tickets a CERRADO
    close_ticket()
    return

def close_ticket():
    total_done=system_db.tickets_done()
    for i in range(total_done):
        data=system_db.pull_ticket_done()
        ticket=data['ticket']
        tx_hash_1=verify_pass(data['tx_hash_1'])
        tx_hash_2=verify_pass(data['tx_hash_2'])
        ac_txhash_1=verify_pass(data['ac_txhash_1'])
        ac_txhash_2=verify_pass(data['ac_txhash_1'])

        if tx_hash_1 == True and tx_hash_2 == True and ac_txhash_1 == True and ac_txhash_2 == True:
            #funcion para cerrar ticket
            system_db.update_close_ticket_ID(ticket)
            print("cerrando ticket > " + str(ticket))
            return
    return

def verify_pass(tx_hash):
    erc_20=explorer_tx_db.pull_status_pass_erc20(tx_hash)
    erc_721=explorer_tx_db.pull_status_pass_erc721(tx_hash)
    if erc_20 == "PASS":
        return True
    if erc_721 == "PASS":
        return True   
    else:
        return False

def prepare_ticket_stat_2_to_3():
    system_db.verify_assets_in_hotwallet()
    return True
#reset ticket
#print(prepare_ticket_stat_2_to_3())
#system_db.reset_ticket_stat_to_pending()
#send_assets()

######
cross_tickets_to_api()
