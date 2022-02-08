import blockchain_func
import system_db


def send_assets():
    system_db.reset_ticket_stat_to_pending()
    ready=system_db.tickets_pending()
    for i in range(ready):
        item=system_db.pull_ticket_ready()
        system_db.update_pass_ticket_ID(item[0])
        print(item)
    print("ready count > "+str(ready))
    return

send_assets()