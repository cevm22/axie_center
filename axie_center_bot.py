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
        "4164536", #axie ID
        100, #price
    ]
    ps_msg_template=ES_msg_templates.ps_msg(vec)
    await ctx.send(embed=ps_msg_template)
    return
#=======================
#Ticket 
@bot.command()
async def ticket(ctx):
    #template MSG TICKET
    vec=[
        "PS-0000001",#Ticket ID:
        "PENDING",#Ticket Status:
        "2022-01-19 00:00:50",#str(datetime.datetime.utcnow()),#Opened:
        654321,#Axie ID:
        100,#Price:
        "0xcea4ced35f6e5d8ce647099f46d0706ddee5a3d521d169ee3cfbfafa098275c8",#Seller Proof Hash:
        ":white_check_mark:",#Seller Status Hash:
        "0xd1fa214b3e920c8d50ab83e502e4237b8de472cb3b3e2a4189d8830fcccedd65",#Buyer Proof Hash:
        ":x:",#Buyer Status Hash:
        ":x:",#Assets in AxieCenter: 
        "0xcea4ced35f6e5d8ce647099f46d0706ddee5a3d521d169ee3cfbfafa098275c8",#AxieCenter to Seller Hash:
        "0xd1fa214b3e920c8d50ab83e502e4237b8de472cb3b3e2a4189d8830fcccedd65",#AxieCenter to Buyer Hash:
        ":x:",#Closed:
        "notas varias en caso de cancelar o error" #Notes
    ]
    ticket_msg=ES_msg_templates.ticket_msg(vec)
    await ctx.send(embed=ticket_msg)
    return

#=======================
#Change Idiom 
@bot.command()
async def ch(ctx,languaje):
    if languaje.lower()=='es':
        #Actualizar base de datos del usuario agregando "es"
        await ctx.send("Has cambiado a ESPAÑOL")

    if languaje.lower()=='en':
        await ctx.send("You Changed to ENGLISH")
    return

#=======================
#Change enrol 
@bot.command()
async def enrol(ctx,ronin):
    
    await ctx.send("Welcome to Axie Center")
    #En caso que ya este registrado 
    #await ctx.send("You are already registered!")
    #En caso que el Wallet YA esta registrado
    #await ctx.send("This Ronin address is already in use, Please Verify it!")
    #Addres no validada por el nodo
    #await ctx.send("Invalid Address")
    return
print("bot started")
bot.run(config.token)