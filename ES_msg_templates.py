import discord
import datetime 
import msg_utils
import config
axie_url="https://marketplace.axieinfinity.com/axie/"
owner_url="https://marketplace.axieinfinity.com/profile/"
tx_url="https://explorer.roninchain.com/tx/"
wallet_axie=config.hotwallet#'ronin:1ba2228e2c90bc6cc4fd7c3fe62e796c4321356f'
wallet_usdc=config.hotwallet#'ronin:1ba2228e2c90bc6cc4fd7c3fe62e796c4321356f'
def ps_msg(msg):
    marketplace=str('[Marketplace]'+'('+str(axie_url+str(msg[1])+')'))
    
    embed = discord.Embed(title=('**PRIVATE SALE**'),
                            description=("**TICKET ID:** " + str(msg[0])),
                            timestamp=datetime.datetime.utcnow(),
                            color=discord.Color.orange())

    embed.set_image(url="https://storage.googleapis.com/assets.axieinfinity.com/axies/"+str(msg[1])+"/axie/axie-full-transparent.png")
    embed.add_field(name="Axie ID",value=str(msg[1]),inline=True)
    embed.add_field(name="Price",value=('$'+str(msg[2])),inline=True)
    embed.add_field(name="Axie URL",value=(marketplace),inline=True)
    embed.set_footer(text="PRIVATE SALE")
    return embed

def ticket_msg(msg):
    marketplace=str('[Marketplace]'+'('+str(axie_url+str(msg[3])+')'))
    #hashes
    seller_hash=msg_utils.seller_hash_status(msg[5])#str("[Seller_Tx]"+'('+str(str(tx_url)+str(msg[5]))+')')
    buyer_hash=msg_utils.buyer_hash_status(msg[7])#str("[Buyer_Tx]"+'('+str(str(tx_url)+str(msg[7]))+')')
    AC_to_Seller=msg_utils.AC_to_Seller_hash_status(msg[10])#str("[AC_to_Seller_Tx]"+'('+str(str(tx_url)+str(msg[10]))+')')
    AC_to_Buyer=msg_utils.AC_to_Buyer_hash_status(msg[11])#str("[AC_to_Buyer_Tx]"+'('+str(str(tx_url)+str(msg[11]))+')')
    #marks
    seller_mark=msg_utils.check_mark(msg[6]) 
    buyer_mark=msg_utils.check_mark(msg[8]) 
    assets_ready=msg_utils.check_mark(msg[9])
    ticket_closed=msg_utils.check_mark(msg[12])
    ticket_status=msg_utils.ticket_status_msg(msg[1])
    
    url_img=str("https://storage.googleapis.com/assets.axieinfinity.com/axies/"+str(msg[3])+"/axie/axie-full-transparent.png")
    embed = discord.Embed(title=('**PRIVATE SALE - STATUS**'),
    description=("**TICKET ID:** " + str(msg[0]) + '\n' 
                + "**STATUS**: " + str(ticket_status)),
    timestamp=datetime.datetime.utcnow(),
    color=discord.Color.orange())
    embed.set_image(url=url_img)
    embed.add_field(name="Axie ID",value=(str(msg[3])),inline=True)    
    embed.add_field(name="Axie URL",value=(marketplace),inline=True)
    embed.add_field(name="Price",value=('$'+str(msg[4])),inline=True)
    embed.add_field(name="Created ",value=str(msg[2]),inline=True)
    embed.add_field(name="Seller Hash ",value=seller_hash,inline=True)   
    embed.add_field(name="Seller Status ",value=seller_mark,inline=True)
    embed.add_field(name="Closed",value=ticket_closed,inline=True)    
    embed.add_field(name="Buyer Hash ",value=buyer_hash,inline=True)   
    embed.add_field(name="Buyer Status ",value=buyer_mark,inline=True)
    embed.add_field(name="AxieCenter Status ",value=assets_ready,inline=False)    
    embed.add_field(name="AC_to_Seller ",value=AC_to_Seller,inline=True)   
    embed.add_field(name="AC_to_Buyer ",value=AC_to_Buyer,inline=True) 
    embed.add_field(name="Notes",value=msg[13],inline=False)    
    embed.set_footer(text="PRIVATE SALE")
    return embed

def trade_msg_1(msg):
    axieID_1=str('[Marketplace]'+'('+str(axie_url+str(msg[3])+')'))
    Owner_tx_1=str("[Proof_hash]"+'('+str(str(tx_url)+str(msg[5]))+')')
    url_img_axie_1=str("https://storage.googleapis.com/assets.axieinfinity.com/axies/"+str(msg[3])+"/axie/axie-full-transparent.png")
    embed = discord.Embed(title=('**AXIE TRADE - STATUS**'),
    description=("**TICKET ID: ** " + str(msg[0]) + '\n' 
                + "**STATUS: ** " + str(msg[1])  ),
    color=discord.Color.green())
    embed.set_image(url=url_img_axie_1)
    embed.add_field(name="Axie(1) ID",value=(str(msg[3])),inline=True) #   
    embed.add_field(name="Axie(1) URL",value=(axieID_1),inline=True)
    embed.add_field(name="Opened",value=(str(msg[2])),inline=True)
    embed.add_field(name="Owner(1)",value=Owner_tx_1,inline=True) 
    embed.add_field(name="Owner(1) Status ",value=msg[6],inline=True)
    return embed

def trade_msg_2(msg):
    axieID_2=str('[Marketplace]'+'('+str(axie_url+str(msg[4])+')'))
    Owner_tx_2=str("[Proof_hash]"+'('+str(str(tx_url)+str(msg[7]))+')')
    AC_to_Owner_1=str("[Proof_hash]"+'('+str(str(tx_url)+str(msg[10]))+')')
    AC_to_Owner_2=str("[Proof_hash]"+'('+str(str(tx_url)+str(msg[11]))+')')
    url_img_axie_1=str("https://storage.googleapis.com/assets.axieinfinity.com/axies/"+str(msg[4])+"/axie/axie-full-transparent.png")
    embed = discord.Embed(timestamp=datetime.datetime.utcnow(),
    color=discord.Color.green())
    embed.set_image(url=url_img_axie_1)
    embed.add_field(name="Axie(2) ID",value=(str(msg[4])),inline=True) #   
    embed.add_field(name="Axie(2) URL",value=(axieID_2),inline=True)
    embed.add_field(name="-",value='-',inline=True) 
    embed.add_field(name="Owner(2)",value=Owner_tx_2,inline=True) 
    embed.add_field(name="Owner(2) Status ",value=msg[8],inline=True)
    embed.add_field(name="AxieCenter Status ",value=msg[9],inline=False)  
    embed.add_field(name="AC_to_Owner_1 ",value=AC_to_Owner_1,inline=True) 
    embed.add_field(name="AC_to_Owner_2 ",value=AC_to_Owner_2,inline=True)
    embed.add_field(name="Closed",value=msg[12],inline=True)    
    embed.add_field(name="Notes",value=msg[13],inline=False)    
    embed.set_footer(text="AXIE TRADE") 
    return embed

def accept_msg_user_1(ticket_id):
    embed = discord.Embed(title=('**ACCEPTED BY BUYER**'),
                description=("**TICKET ID:** "  + str(ticket_id) + "\n"
                + " Please send your pretty **AXIE** to this wallet: **" + str(wallet_axie.lower().replace("0x", "ronin:")) + "** \n"
                + " Once the transaction is accepted, share the hash receipt with the command:  **_proof** [ticket_ID] [proof_hash]" #pendiente comando envio de hash
                ),
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.blue())
    return embed

def accept_msg_user_2(ticket_id):
    embed = discord.Embed(title=('**ACCEPTED BY BUYER**'),
                description=("**TICKET ID:**  "  + str(ticket_id) + "\n"
                + " Please send the **TOTAL** of the sale price in **USDC** tokens to the wallet: **" + str(wallet_usdc.lower().replace("0x", "ronin:")) + "** \n"
                + " Once the transaction is accepted, share the hash receipt with the command: **_proof** [ticket_ID] [proof_hash]" #pendiente comando envio de hash
                ),
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.blue())
    return embed

def testimonial():
    embed = discord.Embed(title=('**TICKET CLOSED**'),
                description=("Thank you so much to use Axie Center!, Please give us a testimonial of your experience with us in our server. "  
                ),
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.red())
    return embed