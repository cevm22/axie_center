import sys
import blockchain_func
import system_db
import config
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
            send_USDC=0 #blockchain_func.USDC_transfer(hotwallet,seller,USDC_asset)####################
            if send_USDC == False or send_USDC=="TIME_OUT":
                system_db.update_pass_ticket_ID(ticket)
            else:
                #actualizar status_ac_hash_1
                system_db.update_ac_hash_1_stat(ticket,True)
                system_db.update_ac_txhash_1(ticket,send_USDC)
                
        
        if status_hash_AC[1] == False:
            # flujo enviar axie al comprador
            # send AXIE to ronin_2 the value_1
            send_AXIE=0 #blockchain_func.AXIE_transfer(hotwallet,buyer,AXIE_id))####################
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
    return
#reset ticket
#system_db.reset_ticket_stat_to_pending()
send_assets()