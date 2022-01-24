
tx_url="https://explorer.roninchain.com/tx/"

def seller_hash_status(hash_content):
    
    if hash_content=="0x1":
        return str("PENDING")
    else:
        return str("[Seller_Tx]"+'('+str(str(tx_url)+str(hash_content))+')')
    
def buyer_hash_status(hash_content):
    if hash_content=="0x2":
        return str("PENDING")
    else:
        return str("[Buyer_Tx]"+'('+str(str(tx_url)+str(hash_content))+')')

def AC_to_Seller_hash_status(hash_content):
    
    if hash_content=="ac1":
        return str("PENDING")
    else:
        return str("[AC_to_Seller_Tx]"+'('+str(str(tx_url)+str(hash_content))+')')
    
def AC_to_Buyer_hash_status(hash_content):
    if hash_content=="ac2":
        return str("PENDING")
    else:
        return str("[AC_to_Buyer_Tx]"+'('+str(str(tx_url)+str(hash_content))+')')

def check_mark(status):
    if status == True:
        return ":white_check_mark:"
    else:
        return ":x:"

def ticket_status_msg(status):
    if status == 0:
        return "TICKET CANCELLED"
    if status == 1:
        return "WAIT TO BE ACCEPTED"
    if status == 2:
        return "ACCEPTED, waiting to users send assets and proof hash"
    if status == 3:
        return "ASSETS ARE IN AXIE CENTER WALLETS"
    if status == 4:
        return "AXIE CENTER WORKING WITH YOUR ASSETS"
    if status == 5:
        return "TICKET CLOSED"

