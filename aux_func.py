import system_db
import math     

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

#print("Estatus de Baneo > "+str(ban_validation(1642527399)))
