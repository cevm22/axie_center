import discord #importamos para conectarnos con el bot
from discord.ext import commands #importamos los comandos
from discord.ext import tasks
import datetime
import config
import ES_msg_templates
import system_db
import aux_func
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
#Axie Trade 
@bot.command()
async def trade(ctx):
    #template MSG TICKET
    #agregar condicional str('[Marketplace]'+'('+str(axie_url+str(msg[4])+')'))
    vec=[
        'T-00001',#Ticket ID:
        'PENDING',#Ticket Status:
        "2022-01-19 00:00:50",#Opened:
        '123456',#Axie_1 ID:
        #Axie_1 img:
        '654321',#Axie_2 ID:
        #Axie_2 img:
        '0xcea4ced35f6e5d8ce647099f46d0706ddee5a3d521d169ee3cfbfafa098275c8___1',#Owner_1 Proof Hash:
        ':white_check_mark:',#Owner_1 Status Hash:
        '0xd1fa214b3e920c8d50ab83e502e4237b8de472cb3b3e2a4189d8830fcccedd65___2',#Owner_2 Proof Hash:
        ':white_check_mark:',#Owner_2 Status Hash:
        ':white_check_mark:',#Assets in AxieCenter: 
        '0xcea4ced35f6e5d8ce647099f46d0706ddee5a3d521d169ee3cfbfafa098275c8',#AxieCenter to Owner_1 Hash:
        '0xd1fa214b3e920c8d50ab83e502e4237b8de472cb3b3e2a4189d8830fcccedd65',#AxieCenter to Owner_2 Hash:
        '2022-01-19 00:00:50',#Closed:
        'Notas varias en caso de cancelar o error',#Notes:
    ]
    trade_msg_1=ES_msg_templates.trade_msg_1(vec)
    trade_msg_2=ES_msg_templates.trade_msg_2(vec)
    await ctx.send(embed=trade_msg_1)
    await ctx.send(":arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise::arrows_counterclockwise:")
    await ctx.send(embed=trade_msg_2)
    return


#=======================
#Change Idiom 
@bot.command()
async def ch(ctx,languaje):
    user_id=str(ctx.message.author.id)
    #Verificar que se encuentre registrado
    verify=system_db.validate_user(user_id)
    if not verify:
            await ctx.send("**NO** estas registrado, usa el comando : **_enroll** para ingresar a Axie Center.")
            return
    #Verificar que no tenga BAN
    banned=aux_func.ban_validation(user_id)
    if banned==True:
            await ctx.send("BANNED")
            return
    else:
            if languaje.lower()=='es':
                system_db.change_language(user_id,'es')
                await ctx.send("Has cambiado a ESPAÑOL :flag_es:")

            if languaje.lower()=='en':
                system_db.change_language(user_id,'en')
                await ctx.send("You Changed to ENGLISH :flag_us:")
            return

#=======================
#Change enrol 
@bot.command()
async def enroll(ctx,ronin):
    
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