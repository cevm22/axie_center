import discord
import datetime 

axie_url="https://marketplace.axieinfinity.com/axie/"
owner_url="https://marketplace.axieinfinity.com/profile/"
tx_url="https://explorer.roninchain.com/tx/"
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
    seller_hash=str("[Seller_Tx]"+'('+str(str(tx_url)+str(msg[5]))+')')
    buyer_hash=str("[Buyer_Tx]"+'('+str(str(tx_url)+str(msg[7]))+')')
    AC_to_Seller=str("[AC_to_Seller_Tx]"+'('+str(str(tx_url)+str(msg[10]))+')')
    AC_to_Buyer=str("[AC_to_Buyer_Tx]"+'('+str(str(tx_url)+str(msg[11]))+')')
    url_img=str("https://storage.googleapis.com/assets.axieinfinity.com/axies/"+str(msg[3])+"/axie/axie-full-transparent.png")
    embed = discord.Embed(title=('**PRIVATE SALE - STATUS**'),
    description=("**TICKET ID:** " + str(msg[0]) + '\n' 
                + "**STATUS**: " + str(msg[1])),
    timestamp=datetime.datetime.utcnow(),
    color=discord.Color.orange())
    embed.set_image(url=url_img)
    embed.add_field(name="Axie ID",value=(str(msg[3])),inline=True)    
    embed.add_field(name="Axie URL",value=(marketplace),inline=True)
    embed.add_field(name="Price",value=('$'+str(msg[4])),inline=True)
    embed.add_field(name="Created ",value=str(msg[2]),inline=True)
    embed.add_field(name="Seller Hash ",value=seller_hash,inline=True)   
    embed.add_field(name="Seller Status ",value=msg[6],inline=True)
    embed.add_field(name="Closed",value=msg[12],inline=True)    
    embed.add_field(name="Buyer Hash ",value=buyer_hash,inline=True)   
    embed.add_field(name="Buyer Status ",value=msg[8],inline=True)
    embed.add_field(name="AxieCenter Status ",value=msg[9],inline=False)    
    embed.add_field(name="AC_to_Seller ",value=AC_to_Seller,inline=True)   
    embed.add_field(name="AC_to_Buyer ",value=AC_to_Buyer,inline=True) 
    embed.add_field(name="Notes",value=msg[13],inline=False)    
    embed.set_footer(text="PRIVATE SALE")
    return embed

def trade_msg_1(msg):
    axieID_1=str('[Marketplace]'+'('+str(axie_url+str(msg[3])+')'))
    Owner_tx_1=str("[Owner_tx_1]"+'('+str(str(tx_url)+str(msg[5]))+')')
    #buyer_hash=str("[Buyer_Tx]"+'('+str(str(tx_url)+str(msg[7]))+')')
    #AC_to_Seller=str("[AC_to_Seller_Tx]"+'('+str(str(tx_url)+str(msg[10]))+')')
    #AC_to_Buyer=str("[AC_to_Buyer_Tx]"+'('+str(str(tx_url)+str(msg[11]))+')')
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
    Owner_tx_2=str("[Owner_tx_2]"+'('+str(str(tx_url)+str(msg[7]))+')')
    #buyer_hash=str("[Buyer_Tx]"+'('+str(str(tx_url)+str(msg[7]))+')')
    #AC_to_Seller=str("[AC_to_Seller_Tx]"+'('+str(str(tx_url)+str(msg[10]))+')')
    #AC_to_Buyer=str("[AC_to_Buyer_Tx]"+'('+str(str(tx_url)+str(msg[11]))+')')
    url_img_axie_1=str("https://storage.googleapis.com/assets.axieinfinity.com/axies/"+str(msg[4])+"/axie/axie-full-transparent.png")
    embed = discord.Embed(timestamp=datetime.datetime.utcnow(),
    color=discord.Color.green())
    embed.set_image(url=url_img_axie_1)
    embed.add_field(name="Axie(2) ID",value=(str(msg[4])),inline=True) #   
    embed.add_field(name="Axie(2) URL",value=(axieID_2),inline=True)
    embed.add_field(name="Owner(2)",value=Owner_tx_2,inline=True) 
    embed.add_field(name="Owner(2) Status ",value=msg[8],inline=True)
    #embed.add_field(name="Price",value=('$'+str(msg[4])),inline=True)
    #embed.add_field(name="Created ",value=str(msg[2]),inline=True)
      
    #embed.add_field(name="Closed",value=msg[12],inline=True)    
    #embed.add_field(name="Buyer Hash ",value=buyer_hash,inline=True)   
    #embed.add_field(name="Buyer Status ",value=msg[8],inline=True)
    #embed.add_field(name="AxieCenter Status ",value=msg[9],inline=False)    
    #embed.add_field(name="AC_to_Seller ",value=AC_to_Seller,inline=True)   
    #embed.add_field(name="AC_to_Buyer ",value=AC_to_Buyer,inline=True) 
    #embed.add_field(name="Notes",value=msg[13],inline=False)    
    embed.set_footer(text="AXIE TRADE")
    return embed