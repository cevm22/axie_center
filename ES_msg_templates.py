import discord
import datetime 

axie_url="https://marketplace.axieinfinity.com/axie/"
owner_url="https://marketplace.axieinfinity.com/profile/"

def ps_msg(msg):
    marketplace=str('[Marketplace]'+'('+str(axie_url+str(msg[1])+')'))
    embed = discord.Embed(title=('**PRIVATE SALE**'),
    description=("**TICKET ID:** " + str(msg[0])),
    timestamp=datetime.datetime.utcnow(),
    color=discord.Color.orange())
    embed.set_image(url="https://storage.googleapis.com/assets.axieinfinity.com/axies/123456/axie/axie-full-transparent.png")
    embed.add_field(name="Axie ID",value=str(msg[1]),inline=True)
    embed.add_field(name="Price",value=('$'+str(msg[2])),inline=True)
    embed.add_field(name="Axie URL",value=(marketplace),inline=True)
    embed.set_footer(text="PRIVATE SALE")
    return embed