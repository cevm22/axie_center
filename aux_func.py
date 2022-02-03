import system_db
import math     
import system_db
import explorer_tx_db
#parametros
comision=0.02
limit_user_ban=10
def ban_validation(discordID):
    ban_flag=system_db.user_gotban(discordID)
    if ban_flag == True:
        return True
    else:
        return False

def comision_calc(price):
    res=math.floor(price*comision)
    if res < 1:
        return 1
    else:
        return res 

            # Primero buscar el hash en el historial (en caso de EXISTIR)
            #   -Comparar el hash coincida que usuario discord lo envio
            #   -Comparar que los assets coincidan con los terminos de la venta privada (en caso que NO, usar status INCORRECTO)
            #   -Actualizar el hash con el ticket
            #   -Actualizar la marca de la venta privada
            
            # Caso de no encontrar el hash actualizado
            #   -Buscar que el hash sea valido
            #   -Buscar el input del hash venga el wallet del usuario, monto/axie correcto con PS
            #   -Actualizar status mark venta privada

def store_hash_flow(discord_ID,proof_hash,seller_or_buyer,ticket):
    
    if seller_or_buyer == 'SELLER':
        #obtener info del hash en DB (en caso de existir)   
        hash_info=explorer_tx_db.pull_erc721_info(proof_hash)
        print("obtener hash info")
        if hash_info == False:
            ########################################################################
            #crear funcion para en caso de que sea falso para SELLER
            ########################################################################
            print("CASO en donde no hay registro en la DB")
            return
        else: #flow cuando se tenga la informacion
            validate_user_ID=system_db.validate_ronin(hash_info['from'].replace("0x", "ronin:"))
            print("Validando USER ID")
            if not validate_user_ID:
                return "USER_NOT_EXIST"
            if str(validate_user_ID["discord_id"]) == str(discord_ID):
                ticket_info=system_db.pull_ticket_allinfo(ticket)
                axie_id_PS=str(ticket_info['value_1'])
                axie_id_hash=str(hash_info['value'])
                print("Discord ID correcto con el vendedor")
                if axie_id_PS == axie_id_hash:
                    #hacer flujo para actualizar la marca y el hash ticket con la informacion de la PS
                    print("guardando marcas, actualizando tickets y hash")
                    system_db.update_mark_discordID_1(ticket) #mark TRUE 
                    system_db.update_hash_user_1(ticket,proof_hash) #update proof hash in ticket status
                    system_db.update_ongoing_ticket_ID(ticket) #update ticket status to 2 - ONGOING
                    explorer_tx_db.update_ERC721_tx_ticket_status_pass(ticket,proof_hash) #update to add ticketid and status = PASS
                    print("todo correcto, sin problema registrado")
                    return True
                else:
                    return "WRONG_AXIE_ID"
            else: #caso en que NO este registrado el ronin o NO corresponda al usuario de la venta privada
                return "USER_NOT_EXIST" 
    else:
        if seller_or_buyer == 'BUYER':
        #obtener info del hash en DB (en caso de existir)   
            hash_info=explorer_tx_db.pull_erc20_info(proof_hash)
            print("obtener hash info")
            if hash_info == False:
                ########################################################################
                #crear funcion para en caso de que sea falso para buyer########################################################################
                print("CASO en donde no hay registro en la DB")
                return
            else: #flow cuando se tenga la informacion
                validate_user_ID=system_db.validate_ronin(hash_info['from'].replace("0x", "ronin:"))
                print("Validando USER ID")
                if not validate_user_ID:
                    return "USER_NOT_EXIST"
                if str(validate_user_ID["discord_id"]) == str(discord_ID):
                    ticket_info=system_db.pull_ticket_allinfo(ticket)
                    token_amount=str(ticket_info['value_2'])
                    token_amount_hash=str(hash_info['value'])
                    print("Discord ID correcto con el vendedor")
                    if token_amount == token_amount_hash:
                        #hacer flujo para actualizar la marca y el hash ticket con la informacion de la PS
                        print("guardando marcas, actualizando tickets y hash")
                        system_db.update_mark_discordID_2(ticket) #mark TRUE 
                        system_db.update_hash_user_2(ticket,proof_hash) #update proof hash in ticket status
                        system_db.update_ongoing_ticket_ID(ticket) #update ticket status to 2 - ONGOING
                        explorer_tx_db.update_ERC20_tx_ticket_status_pass(ticket,proof_hash) #update to add ticketid and status = PASS
                        print("todo correcto, sin problema registrado")
                        return True
                    else:
                        #monto incorrecto, es distinto a la venta privada
                        return "INCORRECT_AMOUNT"
                else: #caso en que NO este registrado el ronin o NO corresponda al usuario de la venta privada
                    return "USER_NOT_EXIST"

#print("Estatus de Baneo > "+str(ban_validation(1642527399)))
