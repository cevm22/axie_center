import discord #importamos para conectarnos con el bot
from discord.ext import commands #importamos los comandos
from discord.ext import tasks
import datetime
import config
import ES_msg_templates
#El bot es activado con el prefijo '_' + comando en la funcion
bot = commands.Bot(command_prefix='_',help_command=None)


#@bot.command()
async def test1(ctx):
    a=str(ctx.message)
    print(a)
    #print(type(a))
    #await ctx.send(f"se han agregado 200 puntos a <@{a}>")
    await ctx.send("Test")
    #<@!375140672329613324> # andres
    #358375624294924289 #lasthope
    #return
#=======================
#Private Sale 
@bot.command()
async def ps(ctx):
    #template MSG
    vec=[
        "PS-0000001",
        123456, #axie ID
        100, #price
        "4164536", #Axie URL
    ]
    ps_msg_template=ES_msg_templates.ps_msg(vec)
    await ctx.send(embed=ps_msg_template)
    return
print("bot started")
bot.run(config.token)