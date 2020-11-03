import os
import psycopg2
NAMES = ["Anne", "Hans", "Joaz", "Joël", "Lindsay", "Michael", "Michelle", "Pim", "René", "Sven"]

DATABASE_URL = os.environ['DATABASE_URL']
#DATABASE_URL = "localhost"



def do_query(query):
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = connection.cursor()
    cursor.execute(query)
    print("query")
    print (query)
    if (query.startswith("SELECT")):
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result;
    else:
        connection.commit()
        cursor.close()
        connection.close()
        return None

def get_list_pluseens():
    return do_query("SELECT * FROM pluseens;")

def create_pluseen(id):
    do_query("INSERT INTO pluseens (name) VALUES ('" +id+"');") #TODO fix sql injection
    return 'Voeg nu jouw +1 toe aan de pluseen ' + id + '!\n<br><a href="/pluseen/pluseen/' + id + '">https://pluseen.herokuapp.com/pluseen/pluseen/' + id + '</a>'


def change_pluseen(id, name):
    if check_pluseen_existance(id):
        result = do_query("SELECT ped.deelnemer FROM pluseendeelnemers ped, pluseens pe WHERE ped.pluseenid = pe.id AND pe.name = '" + str(id) + "';")
        names = []
        for n in result:
            names += n
        addrem = ""
        if name in names:
            #remove the pluseen
            addrem = "verwijderd"
            do_query("DELETE FROM pluseendeelnemers WHERE pluseenid = " + str(get_id_by_name(id)) + " AND deelnemer = '" + str(name) + "';") #TODO fix sql injection
        else:
            #add a pluseen
            addrem = "toegevoegd"
            do_query("INSERT INTO pluseendeelnemers (pluseenid, deelnemer) VALUES (" + str(get_id_by_name(id)) + ", '" + name + "');") #TODO fix sql injection
        return "Je pluseen is succesvol " + addrem + "!"
    return "lol die bestaat niet"

def view(id):
    return get_participants(id)

def get_participants(id):
    if check_pluseen_existance(id):
        res = do_query("SELECT ped.deelnemer FROM pluseendeelnemers ped, pluseens pe WHERE pe.id = ped.pluseenid AND pe.name = '" + str(id) + "';") #TODO fix sql injection
        result = []
        for r in res:
            result.append(r[0])
        return result
    return "lol die bestaat niet"

def get_non_participants(id):
    if check_pluseen_existance(id):
        names = NAMES.copy()
        participants = get_participants(id)
        result = names
        for n in participants:
            if n in result:
                result.remove(n)
        return result
    return "lol die bestaat niet"

def get_name_by_id(id):
    res = do_query("SELECT name FROM pluseens WHERE id = "+str(id)+";")
    result = []
    for r in res:
        return r[0]

def get_id_by_name(name):
    res = do_query("SELECT id FROM pluseens WHERE name = '"+name+"';")
    print("test")
    result = []
    for r in res:
        return r[0]

def check_pluseen_existance(id):
    result = do_query("SELECT * FROM pluseens WHERE name = '"+id+"';")
    if result:
        return True
    return False
