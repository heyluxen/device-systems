# Base de datos en memoria
users_db = []
counter_id = 1

def reset_db():
    global users_db, counter_id
    users_db = []
    counter_id = 1