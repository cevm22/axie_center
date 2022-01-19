import system_db


limit_user_ban=10
def ban_validation(discordID):
    ban_flag=system_db.user_gotban(discordID)
    if ban_flag == True:
        return True
    else:
        return False

#print("Estatus de Baneo > "+str(ban_validation(1642527399)))