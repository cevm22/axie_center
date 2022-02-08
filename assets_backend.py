import blockchain_func
import system_db


def send_assets():
    system_db.reset_ticket_stat_to_pending()
    # obtener num de ticket_stat = 3 (ready)
    ready=system_db.tickets_pending()
    for i in range(ready):
        # obtener data del primer ticket con stat 3
        item=system_db.pull_ticket_ready()
        print(item)
        # Cambiar a status PASS = 9, para CASO DE NO COMPLETARSE EL ENVIO DE AC -> OWNERS
        system_db.update_pass_ticket_ID(item[0])
        
    print("ready count > "+str(ready))
    return

send_assets()