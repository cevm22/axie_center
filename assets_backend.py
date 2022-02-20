import blockchain_func
import system_db
import config
import explorer_tx_db
from datetime import datetime
hotwallet=config.hotwallet
time_limit=config.time_limit
comision=config.comision
def send_assets():
    try:
        system_db.reset_ticket_stat_to_pending()
        # obtener num de ticket_stat = 3 (ready)
        ready=system_db.tickets_pending()
        for i in range(ready):
            # obtener data del primer ticket con stat 3
            item=system_db.pull_ticket_ready()
            ticket=item[0]
            seller=str(item[1].replace("ronin:", "0x"))
            buyer=str(item[2].replace("ronin:", "0x"))
            if item[0][0]== 'T':
                Axie_id_1=int(item[3])
                Axie_id_2=int(item[4])
                status_hash_AC=system_db.pull_ticket_status_ac(ticket) 
                
                if status_hash_AC[0] == False:
                    #flujo enviar asset USDC al vendedor
                    # send USDC to ronin_1 the value_2
                    send_AXIE_1=blockchain_func.AXIE_transfer(hotwallet,seller,Axie_id_2)####################
                    if send_AXIE_1 == False or send_AXIE_1=="TIME_OUT":
                        system_db.update_pass_ticket_ID(ticket)
                    else:
                        #actualizar status_ac_hash_1
                        system_db.update_ac_hash_1_stat(ticket,True)
                        system_db.update_ac_txhash_1(ticket,send_AXIE_1)
                        
                
                if status_hash_AC[1] == False:
                    # flujo enviar axie al comprador
                    # send AXIE to ronin_2 the value_1
                    send_AXIE_2=blockchain_func.AXIE_transfer(hotwallet,buyer,Axie_id_1)####################
                    if send_AXIE_2 == False or send_AXIE_2=="TIME_OUT":
                        system_db.update_pass_ticket_ID(ticket)
                    else:
                        #actualizar status_ac_hash_2
                        system_db.update_ac_hash_2_stat(ticket,True)
                        system_db.update_ac_txhash_2(ticket,send_AXIE_2)
                        
                #funcion para obtener hash
                confirm_status_hash_AC=system_db.pull_ticket_status_ac(ticket) 
                #print(confirm_status_hash_AC)
                if confirm_status_hash_AC[0] ==True and confirm_status_hash_AC[1]==True:
                    # Cerrar ticket como COMPLETADO
                    # Enviar Msg al buyer y seller que todo esta correcto
                    print(item)
                    system_db.update_done_ticket_ID(ticket)
                    system_db.update_tickets_stats_done()
                    print("COMPLETADO")
                else:
                    print(item)
                    # Cambiar a status PASS = 9, para CASO DE NO COMPLETARSE EL ENVIO DE AC -> OWNERS
                    system_db.update_pass_ticket_ID(item[0])
                    print("ERROR")
                continue
            else:
                #[data["ticket"],data["ronin_1"],data["ronin_2"],data["value_1"],data["value_2"]]
                AXIE_id=int(item[3])
                USDC_asset=int(item[4])-comision
                
                
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
                    system_db.update_tickets_stats_done()
                    print("COMPLETADO")
                else:
                    print(item)
                    # Cambiar a status PASS = 9, para CASO DE NO COMPLETARSE EL ENVIO DE AC -> OWNERS
                    system_db.update_pass_ticket_ID(item[0])
                    print("ERROR")
    except Exception as e:
            #print("ready count > "+str(ready))
            # agregar funcion para registrar tx desde los tickets a los logs ERC20 y ERC721 
            print('Error with assets_backend.py in func SEND_ASSETS  '+str(e))
            cross_tickets_to_api()
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
            continue
    #funcion para cambiar los tickets a CERRADO
    close_ticket()
    return

def close_ticket():
    total_done=system_db.tickets_done()
    for i in range(total_done):
        data=system_db.pull_ticket_done()
        ticket=data['ticket']
        seller=data['discord_id_1']
        buyer=data['discord_id_2']
        tx_hash_1=verify_pass(data['tx_hash_1'])
        tx_hash_2=verify_pass(data['tx_hash_2'])
        ac_txhash_1=verify_pass(data['ac_txhash_1'])
        ac_txhash_2=verify_pass(data['ac_txhash_1'])

        if tx_hash_1 == True and tx_hash_2 == True and ac_txhash_1 == True and ac_txhash_2 == True:
            #funcion para cerrar ticket
            system_db.update_close_ticket_ID(ticket)
            #cerrando ticket en los usuarios
            system_db.update_cancel_ticket(seller)
            system_db.update_cancel_ticket(buyer)
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

def cancel_process():   
    # cancel ticket by timeout and pass status cancel_pending = 7
    standby=system_db.tickets_stand_by()
    for a in range(standby):
        #buscar documentos en standby = 1
        data_created=system_db.pull_ticket_created()
        live_time= int(data_created['created']) + config.time_limit_ticket
        tiempo=int(datetime.timestamp(datetime.utcnow()))
        #comparar  la hora de creacion y que sea mayor a 30 min
        if  live_time < tiempo:
            #cambiarlo a status ancel_pending = 7
            discord_users_IDS=system_db.pull_discords_ID_on_ticket(data_created['ticket'])
            status_user_1=system_db.update_cancel_ticket(discord_users_IDS[0])
            status_user_2=system_db.update_cancel_ticket(discord_users_IDS[1])
            system_db.update_cancel_process_ticket_ID(data_created['ticket'])
            system_db.update_tickets_stats_cancelled()
            
            
    accepted=system_db.tickets_accepted()
    for b in range(accepted):
        #buscar documentos en standby = 2
        data_accepted=system_db.pull_ticket_accepted()
        live_time= int(data_accepted['created']) + config.time_limit_ticket
        tiempo=int(datetime.timestamp(datetime.utcnow()))
        #comparar  la hora de creacion y que sea mayor a 30 min
        if  live_time < tiempo:
            #cambiarlo a status ancel_pending = 7
            discord_users_IDS=system_db.pull_discords_ID_on_ticket(data_accepted['ticket'])
            status_user_1=system_db.update_cancel_ticket(discord_users_IDS[0])
            status_user_2=system_db.update_cancel_ticket(discord_users_IDS[1])
            system_db.update_cancel_process_ticket_ID(data_accepted['ticket']) 
            system_db.update_tickets_stats_cancelled()     
    # buscar cantidad tickets en status cancel_pending = 7
    docs=system_db.tickets_cancel_pending()
    for i in range (docs):
        # obtener la data del ticket
        data=system_db.pull_ticket_cancel_pending()
        if data['status_hash_1'] == False and data['status_hash_2'] == False:
            # actualizar el ticket status canceled = 0
            discord_users_IDS=system_db.pull_discords_ID_on_ticket(data['ticket'])
            status_user_1=system_db.update_cancel_ticket(discord_users_IDS[0])
            status_user_2=system_db.update_cancel_ticket(discord_users_IDS[1])
            system_db.update_cancel_ticket_ID(data['ticket'])
            system_db.update_tickets_stats_cancelled()
            continue
        else:
            USDC_CONTRACT = "0x0b7007c13325c48911f73a2dad5fa5dcbf808adc"
            AXIE_CONTRACT = "0x32950db2a7164ae833121501c797d79e7b79d74c"
            if data['status_hash_1'] == True:
                # buscar el hash en db ERC20 y ERC721 para cambiarlo a "CANCEL_PENDING"
                cancel_erc20=explorer_tx_db.pull_erc20_info(data['tx_hash_1'])
                cancel_erc721=explorer_tx_db.pull_erc721_info(data['tx_hash_1'])
                try:
                    if cancel_erc20 == False:
                        if cancel_erc721['token_address'] == AXIE_CONTRACT:
                            #regresar axie
                            explorer_tx_db.update_ERC721_tx_ticket_status_cancel_pending(data['ticket'],cancel_erc721['tx_hash'])
                            axie_id=int(cancel_erc721['value'])
                            refund_to=cancel_erc721['from']
                            refund_from=cancel_erc721['to']
                            refund_hash=blockchain_func.AXIE_transfer(refund_from,refund_to,axie_id)
                            if refund_hash == False or refund_hash=="TIME_OUT":
                                continue
                            else:
                                # actualizar el hash status = 'REFUND' y agregar el hash de REFUND a la db ERC20/ERC721
                                explorer_tx_db.update_ERC721_tx_ticket_status_refund(data['ticket'],cancel_erc721['tx_hash'],refund_hash)
                                # actualizar el ticket status canceled = 0
                                discord_users_IDS=system_db.pull_discords_ID_on_ticket(data['ticket'])
                                status_user_1=system_db.update_cancel_ticket(discord_users_IDS[0])
                                status_user_2=system_db.update_cancel_ticket(discord_users_IDS[1])
                                system_db.update_cancel_ticket_ID(data['ticket'])
                                system_db.update_tickets_stats_cancelled()
                                continue
                    else:
                        if cancel_erc20['token_address'] == USDC_CONTRACT:
                            explorer_tx_db.update_ERC20_tx_ticket_status_cancel_pending(data['ticket'],cancel_erc20['tx_hash'])
                            #regresar USCD 
                            usdc_value=int(cancel_erc20['value'])/1000000
                            refund_to=cancel_erc20['from']
                            refund_from=cancel_erc20['to']
                            refund_hash = blockchain_func.USDC_transfer(refund_from,refund_to,usdc_value)
                            if refund_hash == False or refund_hash=="TIME_OUT":
                                continue
                            else:
                                # actualizar el hash status = 'REFUND' y agregar el hash de REFUND a la db ERC20/ERC721
                                explorer_tx_db.update_ERC20_tx_ticket_status_refund(data['ticket'],cancel_erc20['tx_hash'],refund_hash)
                                # actualizar el ticket status canceled = 0
                                discord_users_IDS=system_db.pull_discords_ID_on_ticket(data['ticket'])
                                status_user_1=system_db.update_cancel_ticket(discord_users_IDS[0])
                                status_user_2=system_db.update_cancel_ticket(discord_users_IDS[1])
                                system_db.update_cancel_ticket_ID(data['ticket'])
                                system_db.update_tickets_stats_cancelled()
                                continue
                except Exception as e:
                    print(e)
                    continue

            if data['status_hash_2'] == True:
                # buscar el hash en db ERC20 y ERC721 para cambiarlo a "CANCEL_PENDING"
                cancel_erc20=explorer_tx_db.pull_erc20_info(data['tx_hash_2'])
                cancel_erc721=explorer_tx_db.pull_erc721_info(data['tx_hash_2'])
                try:
                    if cancel_erc20 == False:
                        if cancel_erc721['token_address'] == AXIE_CONTRACT:
                            explorer_tx_db.update_ERC721_tx_ticket_status_cancel_pending(data['ticket'],cancel_erc721['tx_hash'])
                            #regresar axie
                            axie_id=int(cancel_erc721['value'])
                            refund_to=cancel_erc721['from']
                            refund_from=cancel_erc721['to']
                            refund_hash=blockchain_func.AXIE_transfer(refund_from,refund_to,axie_id)
                        if refund_hash == False or refund_hash=="TIME_OUT":
                                continue
                        else:
                            # actualizar el hash status = 'REFUND' y agregar el hash de REFUND a la db ERC20/ERC721
                            explorer_tx_db.update_ERC721_tx_ticket_status_refund(data['ticket'],cancel_erc721['tx_hash'],refund_hash)
                            # actualizar el ticket status canceled = 0
                            discord_users_IDS=system_db.pull_discords_ID_on_ticket(data['ticket'])
                            status_user_1=system_db.update_cancel_ticket(discord_users_IDS[0])
                            status_user_2=system_db.update_cancel_ticket(discord_users_IDS[1])
                            system_db.update_cancel_ticket_ID(data['ticket'])
                            system_db.update_tickets_stats_cancelled()
                            continue
                    else:
                        if cancel_erc20['token_address'] == USDC_CONTRACT:
                            explorer_tx_db.update_ERC20_tx_ticket_status_cancel_pending(data['ticket'],cancel_erc20['tx_hash'])
                            #regresar USCD 
                            usdc_value=int(cancel_erc20['value'])/1000000
                            refund_to=cancel_erc20['from']
                            refund_from=cancel_erc20['to']
                            refund_hash = blockchain_func.USDC_transfer(refund_from,refund_to,usdc_value)
                            if refund_hash == False or refund_hash=="TIME_OUT":
                                continue
                            else:
                                # actualizar el hash status = 'REFUND' y agregar el hash de REFUND a la db ERC20/ERC721
                                explorer_tx_db.update_ERC20_tx_ticket_status_refund(data['ticket'],cancel_erc20['tx_hash'],refund_hash)
                                # actualizar el ticket status canceled = 0
                                discord_users_IDS=system_db.pull_discords_ID_on_ticket(data['ticket'])
                                status_user_1=system_db.update_cancel_ticket(discord_users_IDS[0])
                                status_user_2=system_db.update_cancel_ticket(discord_users_IDS[1])
                                system_db.update_cancel_ticket_ID(data['ticket'])
                                system_db.update_tickets_stats_cancelled()
                                continue
                except Exception as e:
                    print(e)
                    continue
    #print('se termino flujo de reembolsos')
    return

def close_refund():
    refund_erc20=explorer_tx_db.count_docs_ERC20_refund()
    refund_erc721=explorer_tx_db.count_docs_ERC721_refund()
    for i in range(refund_erc721):
        data_erc721=explorer_tx_db.pull_txhash_refund_erc721()
        refund_hash_done=explorer_tx_db.update_ERC721_tx_ticket_status_refund_done_2(data_erc721['tx_hash'])
        if refund_hash_done == True:
            explorer_tx_db.update_ERC721_tx_ticket_status_refund_done(data_erc721['ticket_id'],data_erc721['refund_hash'])
        
    for i in range(refund_erc20):
        data_erc20=explorer_tx_db.pull_txhash_refund_erc20()
        refund_hash_done=explorer_tx_db.update_ERC20_tx_ticket_status_refund_done_2(data_erc20['tx_hash'])    
        if refund_hash_done == True:
            explorer_tx_db.update_ERC20_tx_ticket_status_refund_done(data_erc20['ticket_id'],data_erc20['refund_hash'])
    #print('Actualizados los hash de reembolso')
    return


def untracked_hash():
    erc20_standby=explorer_tx_db.count_docs_ERC20()
    erc721_standby=explorer_tx_db.count_docs_ERC721()
    for i in range(erc20_standby):
        try:
            data=explorer_tx_db.pull_txhash_standby_erc20_data()
            saved_limit= int(data['created']) + time_limit
            tiempo=int(datetime.timestamp(datetime.utcnow()))
            #buscar si hay refund_hash
            refund_created_verify=explorer_tx_db.pull_refund_hash_created_erc20(data['tx_hash'])
            print('revisando que exista' + str(refund_created_verify))
            if refund_created_verify == True:    
                #si hay, agregar refund_done y no ticket
                explorer_tx_db.update_ERC20_tx_ticket_status_refund_done('NO_TICKET',data['tx_hash'])
                continue
            else:
                #si no hay continuar
                if  saved_limit < tiempo:
                    #cambiar PENDING_TRACK al hash
                    explorer_tx_db.update_ERC20_tx_pending_track(data['tx_hash'])
                    #tomar le hash #comparar el contrato con USDC
                    USDC_CONTRACT = "0x0b7007c13325c48911f73a2dad5fa5dcbf808adc"
                    if data['token_address'] == USDC_CONTRACT:                
                        #revisar que no se encuentre en un ticket
                        verify_exist=system_db.find_untracked_hash(data['tx_hash'])
                        if data['from'] == hotwallet:
                            explorer_tx_db.update_ERC20_tx_ticket_status_refund_done('ASSET_ALREADY_SENT',data['tx_hash'])
                            continue
                        if verify_exist == False:
                            #verificar que sea mas de 5 USDC
                            usdc_value=int(data['value'])/1000000
                            if usdc_value < 5:
                                explorer_tx_db.update_ERC20_tx_ticket_status_refund('HOLD_ASSET',data['tx_hash'],'HOLD_ASSET')
                                continue
                            else:
                                #reenviar el asset al propietario  
                                refund_to=data['from']
                                refund_from=data['to']
                                refund_hash = blockchain_func.USDC_transfer(refund_from,refund_to,usdc_value)
                                if refund_hash == False or refund_hash=="TIME_OUT":
                                    explorer_tx_db.update_ERC20_tx_not_found(data['tx_hash'])
                                    continue
                                else:
                                    # dejar status como refund
                                    explorer_tx_db.update_ERC20_tx_ticket_status_refund('NO_TICKET',data['tx_hash'],refund_hash)
                                    continue
                        else:
                            discord_users_IDS=system_db.pull_discords_ID_on_ticket(data['ticket'])
                            status_user_1=system_db.update_cancel_ticket(discord_users_IDS[0])
                            status_user_2=system_db.update_cancel_ticket(discord_users_IDS[1])
                            system_db.update_cancel_process_ticket_ID(verify_exist['ticket'])
                            continue
                    else: 
                        explorer_tx_db.update_ERC20_tx_invalid_contract(data['tx_hash'])
                        continue

                else:
                    continue
        except Exception as e:
            explorer_tx_db.update_ERC20_tx_not_found(data['tx_hash'])
            print('Error in assets_backend.py in func untracked_hash section erc20_standby '+str(e))
            continue
            
#========================================
    for i in range(erc721_standby):
        try:
            data=explorer_tx_db.pull_txhash_standby_erc721_data()
            saved_limit= int(data['created']) + time_limit
            tiempo=int(datetime.timestamp(datetime.utcnow()))
            refund_created_verify=explorer_tx_db.pull_refund_hash_created_erc721(data['tx_hash'])
            print('revisando que exista ERC721' + str(refund_created_verify))
            if refund_created_verify == True:    
                #si hay, agregar refund_done y no ticket
                explorer_tx_db.update_ERC721_tx_ticket_status_refund_done('NO_TICKET',data['tx_hash'])
                continue
            else:
                if  saved_limit < tiempo:
                    #cambiar PENDING_TRACK al hash
                    explorer_tx_db.update_ERC721_tx_pending_track(data['tx_hash'])
                    #tomar le hash #comparar el contrato con USDC
                    AXIE_CONTRACT = "0x32950db2a7164ae833121501c797d79e7b79d74c"
                    if data['token_address'] == AXIE_CONTRACT:                
                        #revisar que no se encuentre en un ticket
                        verify_exist=system_db.find_untracked_hash(data['tx_hash'])
                        if data['from'] == hotwallet:
                            explorer_tx_db.update_ERC721_tx_ticket_status_refund_done('ASSET_ALREADY_SENT',data['tx_hash'])
                            continue
                        if verify_exist == False:
                                #reenviar el asset al propietario
                                refund_to=data['from']
                                refund_from=data['to']
                                axie_id=int(data['value'])
                                refund_hash = blockchain_func.AXIE_transfer(refund_from,refund_to,axie_id)
                                if refund_hash == False or refund_hash=="TIME_OUT":
                                    explorer_tx_db.update_ERC721_tx_not_found(data['tx_hash'])
                                    continue
                                else:
                                    # dejar status como refund
                                    explorer_tx_db.update_ERC721_tx_ticket_status_refund('NO_TICKET',data['tx_hash'],refund_hash)
                                    continue
                        else:
                            discord_users_IDS=system_db.pull_discords_ID_on_ticket(data['ticket'])
                            status_user_1=system_db.update_cancel_ticket(discord_users_IDS[0])
                            status_user_2=system_db.update_cancel_ticket(discord_users_IDS[1])
                            system_db.update_cancel_process_ticket_ID(verify_exist['ticket'])
                            continue
                    else: 
                        explorer_tx_db.update_ERC721_tx_invalid_contract(data['tx_hash'])
                        continue
                else:
                    continue
        except Exception as e:
            explorer_tx_db.update_ERC721_tx_not_found(data['tx_hash'])
            print('Error in assets_backend.py in func untracked_hash section erc721_standby '+str(e))
            continue
    explorer_tx_db.update_ERC721_tx_all_standby_from_notfound()
    explorer_tx_db.update_ERC20_tx_all_standby_from_notfound()            
    return

def prepare_ticket_stat_2_to_3():
    system_db.verify_assets_in_hotwallet()
    return True

def test_backend():
    import pull_api
    try:
        print("PULL API")
        pull_api.pull_tx_api()
        print('SENDING ASSETS')
        send_assets()
        print('CROSS TICKETS TO API')
        cross_tickets_to_api()
        print('CANCEL PROCESS ')
        cancel_process()
        print('CLOSE REFUND')
        close_refund()
        print('UNTRACKED HASH')
        untracked_hash()
        return
    except Exception as e:
        print('error en TEST_BACKEND funct')
        print(e)
        return
#reset ticket
#print(prepare_ticket_stat_2_to_3())
#system_db.reset_ticket_stat_to_pending()
send_assets()

######
#cross_tickets_to_api()
#print(cancel_process())
#test_backend()
#close_refund()