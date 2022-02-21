import discord #importamos para conectarnos con el bot
from discord.ext import commands #importamos los comandos
from discord.ext import tasks
import datetime
import config
import ES_msg_templates
import system_db
import aux_func
import blockchain_func
import explorer_tx_db
import assets_backend
#El bot es activado con el prefijo '_' + comando en la funcion
bot = commands.Bot(command_prefix='_',help_command=None)
client=discord.Client(activity=discord.Game(name='Axie Center'))

commands_limit=5
price_limit=config.price_limit
price_low_limit=config.price_low_limit

@commands.cooldown(rate=1, per=commands_limit, type=commands.BucketType.member)
@bot.command()
async def test(ctx): 
    user_id=str(ctx.message.author.id) 
    user = await bot.fetch_user(user_id) 
    #assets_backend.test_backend()
    await user.send("OK") 

@commands.cooldown(rate=1, per=commands_limit, type=commands.BucketType.member)
@bot.command()
async def ping(ctx: commands.Context):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")
    #channel=bot.get_channel(944088553510567966)
    #await channel.send('enviando mensaje')
  

#=======================
#Private Sale 
@commands.cooldown(rate=1, per=commands_limit, type=commands.BucketType.member)
@bot.command()
async def ps(ctx,axie_ID,price,password):
    user_id=str(ctx.message.author.id)
    user = await bot.fetch_user(user_id)
    
    #Verificar que se encuentre registrado
    verify=system_db.validate_user(user_id)
    if not verify:
            await user.send("You are **NOT** registered, use the command : **_enroll** [ronin_wallet]")
            return
    #Verificar que no tenga BAN
    banned=aux_func.ban_validation(user_id)
    if banned==True:
            await user.send("BANNED")
            return
            
    #verificacion numeros enteros y menores a 1000
    try:
        comision=aux_func.comision_calc(int(price))
        verify_axie_ID=int(axie_ID)
    except:
        await user.send("**ONLY** decimal values")
        return
    #verificar numeros positivos
    if int(price)<1 or int(verify_axie_ID)<1:
        await user.send("**ONLY** Positive decimal")
        return
    #limite de venta de acuerdo al price_limit
    if int(price) > int(price_limit):
        await user.send("Only private sales can be made for less than **$" + str(price_limit) + "** USDC")
        return
    if int(price)< int(price_low_limit):
        
        return user.send("Only private sales can be made for more than **$" + str(price_low_limit) + "** USDC")
    else:   
        #Revisar que el usuario no tenga ticket abierto o pendiente
        ticket_status=system_db.user_ticket_opened(user_id)
        if ticket_status[0] == True:
            await user.send("You already have a pending ticket, you must **cancel or finish** it before requesting a new one." +"\n" + "Your pending ticket ID is > **"+str(ticket_status[1])+"**")
            return
        else:
            #Flujo creación de Ticket para venta privada
            new_id=int(system_db.pull_tickets_stats_total())+1
            ronin_wallet=system_db.pull_ronin_wallet(user_id)
            ticket_vec=[
                str('PS-'+ str(new_id)),#"PS-0000001", ticket id
                int(axie_ID), #axie ID
                int(price), #price
                comision,#comision #pendiente hacer func comision
                datetime.datetime.utcnow(),#timestamp
                user_id,
                str(password),
                str(ronin_wallet)
            ]
            #Modificar user_status el ticket_last y ticket_status
            system_db.update_ticket_last_status(user_id,ticket_vec[0])
            #Crear Ticket
            system_db.create_ticket_PS(ticket_vec)
            #Incrementar total tickets stats
            system_db.update_tickets_stats()
            #pendiente para casos de huevos
            ps_msg_template=ES_msg_templates.ps_msg(ticket_vec)
            await user.send(embed=ps_msg_template)
            return

#=======================
#review ticket
@commands.cooldown(rate=1, per=commands_limit, type=commands.BucketType.member)
@bot.command()
async def review(ctx,ticket):
    user_id=str(ctx.message.author.id)
    user = await bot.fetch_user(user_id)
    #Verificar que se encuentre registrado
    verify=system_db.validate_user(user_id)
    if not verify:
            await user.send("You are **NOT** registered, use the command : **_enroll** [ronin_wallet]")
            return
    #Verificar que no tenga BAN
    banned=aux_func.ban_validation(user_id)
    if banned==True:
            await user.send("BANNED")
            return
    data=system_db.pull_ticket_allinfo(ticket)
    if not data:
        return await user.send('There is NO ticket with this ID')
    pending=data['ticket_stat']
    if pending == 1:
        ticket_vec=[
                    ticket,#str('PS-'+ str(new_id)),#"PS-0000001", ticket id
                    int(data['value_1']),#int(axie_ID), #axie ID
                    int(data['value_2'])#int(price), #price
                    ]
        if data['type']=='Private Sale':
            
            ps_msg_template=ES_msg_templates.ps_msg(ticket_vec)
            await user.send(embed=ps_msg_template)
            return
        else:
            trade_template=ES_msg_templates.trade_review_msg(ticket_vec)
            await user.send(embed=trade_template[0])
            await user.send(":arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise:")
            await user.send(embed=trade_template[1])
            return
    else:
        await user.send("This ticket was accepted or canceled")
        return

#=======================
#Ticket 
@commands.cooldown(rate=1, per=commands_limit, type=commands.BucketType.member)
@bot.command()
async def ticket(ctx,ticket):
    user_id=str(ctx.message.author.id)
    user = await bot.fetch_user(user_id)
    #Verificar que se encuentre registrado
    verify=system_db.validate_user(user_id)
    if not verify:
            await user.send("You are **NOT** registered, use the command : **_enroll** [ronin_wallet]")
            return
    #Verificar que no tenga BAN
    banned=aux_func.ban_validation(user_id)
    if banned==True:
            await user.send("BANNED")
            return
    #Revisar que el usuario no tenga ticket abierto o pendiente
    ticket_status=system_db.user_ticket_opened(user_id)
    if ticket_status[0] == False:
        await user.send("You dont have OPENED tickets")
        return
    #Revisar que exista el ticket ID
    find_ticket_id=system_db.pull_ticket_id(ticket)
    if find_ticket_id[0]==False:
        await user.send("There is **NOT** ticket with this ID")
        return
    #revisar que el ticket NO se ha cancelado antes
    if find_ticket_id[1]==0:
        await user.send("This ticket has been previously canceled")
        return
 
    #revisar que el usuario se encuentre en un ticket
    discord_users_IDS=system_db.pull_discords_ID_on_ticket(ticket)
    data=system_db.pull_ticket_allinfo(ticket)
    if data['type']=='Private Sale':
        if discord_users_IDS[0]==user_id or discord_users_IDS[1]==user_id:
            #Proceso para mostrar ticket
            #pull data from ticket
            ticket_id=data['ticket']
            ticket_status= data['ticket_stat']
            axie_id=data['value_1']
            price=data['value_2']
            #template MSG TICKET
            seller_proof_hash=data['tx_hash_1']
            buyer_proof_hash=data['tx_hash_2']
            AC_to_seller_proof_hash=data['ac_txhash_1']
            AC_to_buyer_proof_hash=data["ac_txhash_2"]
            #marks 
            seller_mark=data['status_hash_1'] 
            buyer_mark=data['status_hash_2'] 
            if seller_mark==False and buyer_mark ==False:
                assets_ready=False 
            else:
                assets_ready=True
            ticket_closed=data['ticket_stat'] 
            logs=data['log']
            timestamp_to_date=data['init_time'].strftime("%m/%d/%Y, %H:%M:%S")#datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
            vec=[
                ticket_id,#Ticket ID:
                ticket_status,#Ticket Status:
                str(timestamp_to_date),#Opened:
                axie_id,#Axie ID:
                price,#Price:
                seller_proof_hash,#Seller Proof Hash:
                seller_mark,#Seller Status Hash:
                buyer_proof_hash,#Buyer Proof Hash:
                buyer_mark,#Buyer Status Hash:
                assets_ready,#Assets in AxieCenter: 
                AC_to_seller_proof_hash,#AxieCenter to Seller Hash:
                AC_to_buyer_proof_hash,#AxieCenter to Buyer Hash:
                ticket_closed,#Closed:
                logs #Notes
            ]
            ticket_msg=ES_msg_templates.ticket_msg(vec)
            await user.send(embed=ticket_msg)
            return
        else:
            await user.send("You cannot see tickets from other users.")
            return
    else:
        if discord_users_IDS[0]==user_id or discord_users_IDS[1]==user_id:
            timestamp_to_date=data['init_time'].strftime("%m/%d/%Y, %H:%M:%S")
            #template MSG TICKET
            seller_proof_hash=data['tx_hash_1']
            buyer_proof_hash=data['tx_hash_2']
            AC_to_seller_proof_hash=data['ac_txhash_1']
            AC_to_buyer_proof_hash=data["ac_txhash_2"]
            #marks 
            seller_mark=data['status_hash_1'] 
            buyer_mark=data['status_hash_2'] 
            ticket_closed=data['ticket_stat'] 
            logs=data['log']
            if seller_mark==False and buyer_mark ==False:
                assets_ready=False 
            else:
                assets_ready=True
            vec_msg=[
                str(ticket),#Ticket ID:
                data['ticket_stat'],#Ticket Status:
                timestamp_to_date,#Opened:
                data['value_1'],#Axie_1 ID:
                #Axie_1 img:
                data['value_2'],#Axie_2 ID:
                #Axie_2 img:
                seller_proof_hash,#Owner_1 Proof Hash:
                seller_mark,#Owner_1 Status Hash:
                buyer_proof_hash,#Owner_2 Proof Hash:
                buyer_mark,#Owner_2 Status Hash:
                assets_ready,#Assets in AxieCenter: 
                AC_to_seller_proof_hash,#AxieCenter to Owner_1 Hash:
                AC_to_buyer_proof_hash,#AxieCenter to Owner_2 Hash:
                ticket_closed,#Closed:
                logs,#Notes:
            ]
            trade_msg_1=ES_msg_templates.trade_msg_1(vec_msg)
            trade_msg_2=ES_msg_templates.trade_msg_2(vec_msg)
            await ctx.send(embed=trade_msg_1)
            await ctx.send(":arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise:")
            await ctx.send(embed=trade_msg_2)
            return
        else:   
            await user.send("You cannot see tickets from other users.")
            return

#=======================
#Ticket send hash
@bot.command()
@commands.cooldown(rate=1, per=commands_limit, type=commands.BucketType.member)
async def proof(ctx,ticket, proof_hash):
    user_id=str(ctx.message.author.id)
    user = await bot.fetch_user(user_id)
    #Verificar que se encuentre registrado
    verify=system_db.validate_user(user_id)
    if not verify:
            await user.send("You are **NOT** registered, use the command : **_enroll** [ronin_wallet]")
            return
    #Verificar que no tenga BAN
    banned=aux_func.ban_validation(user_id)
    if banned==True:
            await user.send("BANNED")
            return
    #Revisar que el usuario no tenga ticket abierto o pendiente
    ticket_status=system_db.user_ticket_opened(user_id)
    if ticket_status[0] == False:
        await user.send("You dont have OPENED tickets")
        return
    #Revisar que exista el ticket ID
    find_ticket_id=system_db.pull_ticket_id(ticket)
    if find_ticket_id[0]==False:
        await user.send("There is **NOT** ticket with this ID")
        return
    #revisar que el ticket NO se ha cancelado antes
    if find_ticket_id[1]==0:
        await user.send("This ticket has been previously canceled")
        return
    #revisar que el ticket se encuentre FINALIZADO
    if find_ticket_id[1]==5:
        await user.send("This ticket has been previously completed")
        return
    else:
        
        search_erc20=explorer_tx_db.pull_status_pass_erc20(proof_hash)
        search_erc721=explorer_tx_db.pull_status_pass_erc721(proof_hash)
        if search_erc721== "PASS" or search_erc20=="PASS" or search_erc721== "REFUND" or search_erc20=="REFUND"  or search_erc721== "CANCEL" or search_erc20=="CANCEL" :
            await user.send("This HASH has already been delivered before")
            return
        #revisar que el usuario se encuentre en un ticket
        discord_users_IDS=system_db.pull_discords_ID_on_ticket(ticket)
        
        #get TRADE or PRIVATE SALE
        type_ticket=ticket[0]
        if discord_users_IDS[0]==user_id: #usuario 1 - vendedor
            #funcion enviar hash
            if type_ticket =='T':
                verify_hash= aux_func.store_hash_flow_trade(user_id,proof_hash,"SELLER",ticket)
            else:
                verify_hash= aux_func.store_hash_flow(user_id,proof_hash,"SELLER",ticket)
            if verify_hash == True:
                system_db.verify_assets_in_hotwallet()
                await user.send(":white_check_mark: Proof Hash, verified. :white_check_mark:")
                return
            else:
                await user.send(verify_hash)
                return
            
        if discord_users_IDS[1]==user_id: #usuario 2 - comprador
            #funcion enviar hash
            if type_ticket =='T':
                verify_hash= aux_func.store_hash_flow_trade(user_id,proof_hash,"BUYER",ticket)
            else:
                verify_hash= aux_func.store_hash_flow(user_id,proof_hash,"BUYER",ticket)
            if verify_hash == True:
                system_db.verify_assets_in_hotwallet()
                await user.send(":white_check_mark: Proof Hash, verified. :white_check_mark:")
                return
            else:
                await user.send(verify_hash)
                return
        
#=======================
#Ticket cancel
@bot.command()
@commands.cooldown(rate=1, per=commands_limit, type=commands.BucketType.member)
async def cancel(ctx, ticket):
    user_id=str(ctx.message.author.id)
    user = await bot.fetch_user(user_id)
    verify=system_db.validate_user(user_id)
    if not verify:
            await user.send("You are **NOT** registered, use the command : **_enroll** [ronin_wallet]")
            return
    #Verificar que no tenga BAN
    banned=aux_func.ban_validation(user_id)
    if banned==True:
            await user.send("BANNED")
            return
    #Revisar que el usuario no tenga ticket abierto o pendiente
    ticket_status=system_db.user_ticket_opened(user_id)
    if ticket_status[0] == False:
        await user.send("You dont have OPENED tickets")
        return
    #Revisar que exista el ticket ID
    find_ticket_id=system_db.pull_ticket_id(ticket)
    if find_ticket_id[0]==False:
        await user.send("There is **NOT** ticket with this ID")
        return
    #revisar que el ticket NO se ha cancelado antes
    if find_ticket_id[1]==0:
        await user.send("This ticket has been previously canceled")
        return
#revisar que el usuario se encuentre involucrado en la venta privada
    else:
        #revisar que el usuario se encuentre en un ticket
        discord_users_IDS=system_db.pull_discords_ID_on_ticket(ticket)
        if discord_users_IDS[0]==user_id or discord_users_IDS[1]==user_id:
            #proceder a la cancelacion
            #actualizando user db ticket_open=false
            cancel_ticket_USER=system_db.update_cancel_ticket(user_id)
            #si fue previamente aceptado por user 2, buscar y actualizar user db ticket_open=false
            user2_accepted=system_db.validate_user2_accepted(ticket)
            if user2_accepted == 2:
                #funcion para actualizar ticket status en users DB del comprador
                status_user_1=system_db.update_cancel_ticket(discord_users_IDS[0])
                status_user_2=system_db.update_cancel_ticket(discord_users_IDS[1])
                #actualizar ticket status a cancel_peding=7
                system_db.update_cancel_process_ticket_ID(ticket)

                #agregar al contador de tickets cancelados
                system_db.update_tickets_stats_cancelled()
                if discord_users_IDS[0]== user_id:
                    user_2=await bot.fetch_user(discord_users_IDS[1])
                    await user.send("Ticket was CANCELED by the SELLER")
                    await user_2.send("Ticket was CANCELED by the SELLER")
                    return
                if discord_users_IDS[1]== user_id:
                    user_1=await bot.fetch_user(discord_users_IDS[0])
                    await user.send("Ticket was CANCELED by the BUYER")
                    await user_1.send("Ticket was CANCELED by the BUYER")
                    return
            #update ticket cancel
            #buscar el ticket en tickets DB por ticket ID y actualizar ticket status a 0
            if user2_accepted > 2:
                await user.send("Ticket can NOT be canceled, because it is in the process of completing sale")
                return
            else: 
                cancel_ticketID=system_db.update_cancel_ticket_ID(ticket)
                #agregar al contador de tickets cancelados
                system_db.update_tickets_stats_cancelled()
                await user.send("TICKET CANCELED")
                return
        else:
            await user.send("You can **NOT** cancel tickets from other users. You can only cancel your own tickets.")
            return

#=======================
#Ticket accept
@bot.command()
@commands.cooldown(rate=1, per=commands_limit, type=commands.BucketType.member)
async def accept(ctx, ticket, password):
    user_id=str(ctx.message.author.id)
    user = await bot.fetch_user(user_id)
    verify=system_db.validate_user(user_id)
    #verificar que este registrado
    if not verify:
            await user.send("You are **NOT** registered, use the command : **_enroll** [ronin_wallet]")
            return
    #Verificar que no tenga BAN
    banned=aux_func.ban_validation(user_id)
    if banned==True:
            await user.send("BANNED")
            return
    #Revisar que el usuario no tenga ticket abierto o pendiente
    ticket_status=system_db.user_ticket_opened(user_id)
    if ticket_status[0] == True:
        await user.send("You already have a pending ticket, you must **cancel it or finish it** before requesting a new one." +"\n" + "Your pending Ticket ID is > **"+str(ticket_status[1])+"**")
        return
    #Revisar que exista el ticket ID
    find_ticket_id=system_db.pull_ticket_id(ticket)
    if find_ticket_id[0]==False:
        await user.send("There is **NOT** ticket with this ID")
        return
    #revisar que el ticket NO se ha cancelado antes
    if find_ticket_id[1]==0:
        await user.send("This ticket has been previously canceled")
        return    
    #verificar ticket no ha sido aceptado por alguien mas
    if find_ticket_id[1]==2: 
        await user.send("This ticket has already been accepted")
        return
    if find_ticket_id[1]==6: 
        await user.send("This ticket was closed")
        return
    if find_ticket_id[1]==1: 
        #####flujo de aceptacion de ticket por parte del comprador
        #verificar contrasena del ticket
        ticket_pass=system_db.pull_ticket_password(ticket)
        buyer_wallet=system_db.pull_ronin_wallet(user_id)
        if password ==ticket_pass:
            #actualizar el ticket a estatus incompleto y agregar discord_id_2
            actualizar=system_db.update_ticket_status_discordID2_ronin(ticket,user_id,buyer_wallet)
            #actualizar estatus del comprador con el mismo ticket ID y en ticket abierto
            actualizar_user=system_db.update_ticket_last_status(user_id,ticket)
            #enviar mensaje al comprador y vendedor de que ha sido aceptado
            data=system_db.pull_ticket_allinfo(ticket)
            if data['type']=='Private Sale':
                vendedor=system_db.pull_user_seller(ticket)
                user_2 = await bot.fetch_user(vendedor)
                #enviar mensaje al vendedor donde enviar su AXIE
                msg_1=ES_msg_templates.accept_msg_user_2(ticket)
                msg_2=ES_msg_templates.accept_msg_user_1(ticket)
                await user.send(embed=msg_1)
                #enviar mensaje al comprador donde enviar sus tokens USDC
                await user_2.send(embed=msg_2)
                return
            else:
                vendedor=system_db.pull_user_seller(ticket)
                user_2 = await bot.fetch_user(vendedor)
                #enviar mensaje al vendedor donde enviar su AXIE
                msg_1=ES_msg_templates.accept_msg_user_1(ticket)
                msg_2=ES_msg_templates.accept_msg_user_1(ticket)
                await user.send(embed=msg_1)
                #enviar mensaje al comprador donde enviar sus tokens USDC
                await user_2.send(embed=msg_2)
                return
        else:
            await user.send("The ticket password is **incorrect**")
            return
    else:
        return await user.send("This Ticket is in process by Axie Center")
    
#=======================
#Axie Trade 
@commands.cooldown(rate=1, per=commands_limit, type=commands.BucketType.member)
@bot.command()
async def trade(ctx,axie_ID_1,axie_ID_2,password):
    user_id=str(ctx.message.author.id)
    user = await bot.fetch_user(user_id)
    #Verificar que se encuentre registrado
    verify=system_db.validate_user(user_id)
    if not verify:
            await user.send("You are **NOT** registered, use the command : **_enroll** [ronin_wallet]")
            return
    #Verificar que no tenga BAN
    banned=aux_func.ban_validation(user_id)
    if banned==True:
            await user.send("BANNED")
            return
    #Revisar que el usuario no tenga ticket abierto o pendiente
    ticket_status=system_db.user_ticket_opened(user_id)
    if ticket_status[0] == True:
        await user.send("You already have a pending ticket, you must **cancel or finish** it before requesting a new one." +"\n" + "Your pending ticket ID is > **"+str(ticket_status[1])+"**")
        return
    else:
        #template MSG TICKET
        #Flujo creación de Ticket para venta privada
        new_id=int(system_db.pull_tickets_stats_total())+1
        ronin_wallet=system_db.pull_ronin_wallet(user_id)
        ticket_vec=[
                    str('T-'+ str(new_id)),#"PS-0000001", ticket id
                    int(axie_ID_1), #axie ID
                    int(axie_ID_2), #price
                    0,#comision #pendiente hacer func comision
                    datetime.datetime.utcnow(),#timestamp
                    user_id,
                    str(password),
                    str(ronin_wallet)
                ]
        
        vec=[
            str('T-'+ str(new_id)),#Ticket ID:
            1,#Ticket Status:
            datetime.datetime.utcnow(),#Opened:
            str(axie_ID_1),#Axie_1 ID:
            #Axie_1 img:
            str(axie_ID_2),#Axie_2 ID:
            #Axie_2 img:
            '0x1',#Owner_1 Proof Hash:
            ':x:',#Owner_1 Status Hash:
            '0x2',#Owner_2 Proof Hash:
            ':x:',#Owner_2 Status Hash:
            ':x:',#Assets in AxieCenter: 
            'ac1',#AxieCenter to Owner_1 Hash:
            'ac2',#AxieCenter to Owner_2 Hash:
            ':x:',#Closed:
            'Notes',#Notes:
        ]
         #Modificar user_status el ticket_last y ticket_status
        system_db.update_ticket_last_status(user_id,ticket_vec[0])
        #Incrementar total tickets stats
        system_db.update_tickets_stats()
        #crear ticket
        system_db.create_ticket_TRADE(ticket_vec)
        trade_msg_1=ES_msg_templates.trade_msg_1(vec)
        trade_msg_2=ES_msg_templates.trade_msg_2(vec)
        await ctx.send(embed=trade_msg_1)
        await ctx.send(":arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise:")
        await ctx.send(embed=trade_msg_2)
        return

#=======================
#Change enrol 
@bot.command()
@commands.cooldown(rate=1, per=commands_limit, type=commands.BucketType.member)
async def enroll(ctx,ronin):
    #En caso que ya este registrado 
    user_ID=str(ctx.message.author.id)
    user_exist=system_db.validate_user(user_ID)
    if not user_exist:
            valid_address=blockchain_func.validate_ronin(ronin)
            if valid_address == True:
                #Verificar que el Wallet YA esta registrado
                ronin_exist=system_db.validate_ronin(str(ronin.lower()))
                if not ronin_exist:
                    #### Hacer flujo de registro
                    vector=[user_ID,str(ronin.lower())]
                    validate_enroll=system_db.enroll_new(vector)            
                    if validate_enroll == True:
                        await ctx.send("Welcome to Axie Center")
                        return
                    else:
                        await ctx.send("Somthing is wrong, please verify with an Admin")
                        return
                else:
                    await ctx.send("This Ronin address is already in use, Please Verify it! and send it again")
                    return
            else:
                await ctx.send("Invalid Address, Please use a valid **ronin** Address")
                return
    else:
        await ctx.send("You are already registered!")
        return

#=======================
#Create DBS
@bot.command()
@commands.cooldown(rate=1, per=commands_limit, type=commands.BucketType.member)
async def deploybot(ctx):
    user_id=str(ctx.message.author.id)
    user = await bot.fetch_user(user_id)
    #crear bases de datos STATS  de tickets
    stats=explorer_tx_db.find_stats_exists()
    if stats == False:
        explorer_tx_db.create_explorer_stats_db()
        await user.send("DB - Explorer Stats Created")
    ticket_stats=system_db.find_ticket_stats()
    if ticket_stats == False:
        system_db.create_tickets_stats_db()
        await user.send('DB - Ticket Stats Created')
    await user.send("BOT deployed")
    return

#==================================================
#Routine to send profits to master wallet 
@bot.command()
@commands.cooldown(rate=1, per=commands_limit, type=commands.BucketType.member)
async def takeprofits(ctx,usdc_value):
    master=config.master_id
    user_id=str(ctx.message.author.id)
    user = await bot.fetch_user(user_id)
    if master == str(user_id):
        to_wallet=system_db.pull_ronin_wallet(master)
        answer=aux_func.send_profit(to_wallet.replace("ronin:", "0x"),usdc_value)
        if answer == False:
            await user.send(str(answer))
            return 
        else:
            #guardar la tx
            vec=[
                str(config.hotwallet),
                to_wallet.replace("ronin:", "0x"),
                usdc_value,
                0,
                answer,
                0,
                0,
                0,
                'USDC',
                'take_profits',
                'PASS'
            ]
            explorer_tx_db.add_ERC20_tx_profits(vec)
            await user.send(str(answer))
            return 
    else:
        return

#==================================================
#Routine to send Ticket closed to Buyer and Seller
@tasks.loop(seconds=60)
async def closeticket():
        #buscar tickets DONE = 5
        data=system_db.pull_ticket_closed()
        if not data:
            #print("no hay ticket")
            return
        else:
            #print(ticket)
            seller = await bot.fetch_user(data['discord_id_1'])
            buyer = await bot.fetch_user(data['discord_id_2'])
            #Proceso para mostrar ticket
            #pull data from ticket
            #data=system_db.pull_ticket_closed()
            ticket_id=data['ticket']
            ticket_status= data['ticket_stat']
            if data['ticket'][0]=='T':

                discord_users_IDS=system_db.pull_discords_ID_on_ticket(data['ticket'])
                status_user_1=system_db.update_cancel_ticket(discord_users_IDS[0])
                status_user_2=system_db.update_cancel_ticket(discord_users_IDS[1])
                
                
                system_db.update_send_msg_ticket_ID(data['ticket'])
                testimonial=ES_msg_templates.testimonial()
                channel=bot.get_channel(944088553510567966)
                #=====================================
                ticket_vec=[
                    data['ticket'],#str('PS-'+ str(new_id)),#"PS-0000001", ticket id
                    int(data['value_1']),#int(axie_ID), #axie ID
                    int(data['value_2'])#int(price), #price
                    ]
                trade_template=ES_msg_templates.trade_review_msg(ticket_vec)
                await seller.send(embed=trade_template[0])
                await seller.send(":arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise:")
                await seller.send(embed=trade_template[1])
                await seller.send(embed=testimonial)
                
                await buyer.send(embed=trade_template[0])
                await buyer.send(":arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise:")
                await buyer.send(embed=trade_template[1])
                await buyer.send(embed=testimonial)
                 
                await channel.send(embed=trade_template[0])
                await channel.send(":arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise:")
                await channel.send(embed=trade_template[1])


            else:   
                axie_id=data['value_1']
                price=data['value_2']
                #template MSG TICKET
                seller_proof_hash=data['tx_hash_1']
                buyer_proof_hash=data['tx_hash_2']
                AC_to_seller_proof_hash=data['ac_txhash_1']
                AC_to_buyer_proof_hash=data["ac_txhash_2"]
                #marks 
                seller_mark=data['status_hash_1'] 
                buyer_mark=data['status_hash_2'] 
                if seller_mark==False and buyer_mark ==False:
                    assets_ready=False 
                else:
                    assets_ready=True
                logs=data['log']
                timestamp_to_date=data['init_time'].strftime("%m/%d/%Y, %H:%M:%S")#datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
                vec=[
                    ticket_id,#Ticket ID:
                    ticket_status,#Ticket Status:
                    str(timestamp_to_date),#Opened:
                    axie_id,#Axie ID:
                    price,#Price:
                    seller_proof_hash,#Seller Proof Hash:
                    seller_mark,#Seller Status Hash:
                    buyer_proof_hash,#Buyer Proof Hash:
                    buyer_mark,#Buyer Status Hash:
                    assets_ready,#Assets in AxieCenter: 
                    AC_to_seller_proof_hash,#AxieCenter to Seller Hash:
                    AC_to_buyer_proof_hash,#AxieCenter to Buyer Hash:
                    True,#Closed:
                    logs #Notes
                ]
                discord_users_IDS=system_db.pull_discords_ID_on_ticket(data['ticket'])
                status_user_1=system_db.update_cancel_ticket(discord_users_IDS[0])
                status_user_2=system_db.update_cancel_ticket(discord_users_IDS[1])
                ticket_msg=ES_msg_templates.ticket_msg(vec)
                #cambiar tickets CLOSED = 6
                system_db.update_send_msg_ticket_ID(data['ticket'])
                testimonial=ES_msg_templates.testimonial()
                channel=bot.get_channel(944088553510567966)
                await seller.send(embed=ticket_msg)
                await seller.send(embed=testimonial)
                await buyer.send(embed=ticket_msg)
                await buyer.send(embed=testimonial)            
                await channel.send(embed=ticket_msg)

@trade.error
async def trade_error(ctx: commands.Context, error: commands.CommandError):
    user_id=str(ctx.message.author.id)
    user = await bot.fetch_user(user_id)
    if isinstance(error, commands.MissingRequiredArgument):
        msg= "__Missing a required argument__ -> **_trade** [Axie ID 1] [Axie ID 2] [password] \n -> ` _trade 12345 67890 p4s5W0rd` " 
    return await user.send(msg)            

@ps.error
async def ps_error(ctx: commands.Context, error: commands.CommandError):
    user_id=str(ctx.message.author.id)
    user = await bot.fetch_user(user_id)
    if isinstance(error, commands.MissingRequiredArgument):
        msg= "__Missing a required argument__ -> **_ps** [Axie ID] [Sell price, (decimal)] [password] \n -> ` _ps 12345 300 p4s5W0rd` " 
    return await user.send(msg)

@review.error
async def review_error(ctx: commands.Context, error: commands.CommandError):
    user_id=str(ctx.message.author.id)
    user = await bot.fetch_user(user_id)
    if isinstance(error, commands.MissingRequiredArgument):
        msg= "__Missing a required argument__ -> **_review** [ticket ID] \n -> `_review PS-1` "
    return await user.send(msg)

@ticket.error
async def ticket_error(ctx: commands.Context, error: commands.CommandError):
    user_id=str(ctx.message.author.id)
    user = await bot.fetch_user(user_id)
    if isinstance(error, commands.MissingRequiredArgument):
        msg= "__Missing a required argument__ -> **_ticket** [ticket ID] \n -> `_ticket PS-12` "
    return await user.send(msg)

@proof.error
async def proof_error(ctx: commands.Context, error: commands.CommandError):
    user_id=str(ctx.message.author.id)
    user = await bot.fetch_user(user_id)
    if isinstance(error, commands.MissingRequiredArgument):
        msg= "__Missing a required argument__ -> **_proof** [ticket ID] [proof hash of tx] \n -> `_proof PS-123 0xfe72a592a6c4d93d58fbb6e514283187789ca0427db87373cde75e8bd5fd1518` "
    return await user.send(msg)

@cancel.error
async def cancel_error(ctx: commands.Context, error: commands.CommandError):
    user_id=str(ctx.message.author.id)
    user = await bot.fetch_user(user_id)
    if isinstance(error, commands.MissingRequiredArgument):
        msg= "__Missing a required argument__ -> **_cancel** [ticket ID] \n -> `_ticket PS-3` "
    return await user.send(msg)

@accept.error
async def accept_error(ctx: commands.Context, error: commands.CommandError):
    user_id=str(ctx.message.author.id)
    user = await bot.fetch_user(user_id)
    if isinstance(error, commands.MissingRequiredArgument):
        msg= "__Missing a required argument__ -> **_accept** [ticket ID] [password, given by seller] \n -> `_accept PS-3 p4s5W0rd` "
    return await user.send(msg)

@enroll.error
async def enroll_error(ctx: commands.Context, error: commands.CommandError):
    user_id=str(ctx.message.author.id)
    user = await bot.fetch_user(user_id)
    if isinstance(error, commands.MissingRequiredArgument):
        msg= "__Missing a required argument__ -> **_enroll** [wallet start with 'ronin:'] \n -> `_enroll ronin:0f14612bad915aa3c5d6f43f1b046f703c6dead0`"
    return await user.send(msg)

@bot.event
async def on_command_error( ctx: commands.Context, error: commands.CommandError):
        user_id=str(ctx.message.author.id)
        user = await bot.fetch_user(user_id)
        if isinstance(error, commands.CommandNotFound):
            return await user.send('Command not found, please review the commands list with > _help ')
        if isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds. Remember, rate limit of 1 command type every "+ str(commands_limit) +" secs"
            return await user.send(message)
        print(error)
        
@bot.event
async def on_ready():
    print('AXIE CENTER READY')
    closeticket.start()
    
print("bot started")
bot.run(config.token)