import discord #importamos para conectarnos con el bot
from discord.ext import commands #importamos los comandos
from discord.ext import tasks
import datetime
import config
#El bot es activado con el prefijo '_' + comando en la funcion
bot = commands.Bot(command_prefix='_',help_command=None)


@bot.command()
async def test(ctx):
    a=str(ctx.message)
    print(a)
    #print(type(a))
    #await ctx.send(f"se han agregado 200 puntos a <@{a}>")
    await ctx.send("Test")
    #<@!375140672329613324> # andres
    #358375624294924289 #lasthope
    #return

bot.run(config.token)