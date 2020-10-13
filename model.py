import os
NAMES = ["Anne", "Hans", "Joaz", "Joël", "Lindsay", "Michael", "Michelle", "Pim", "René", "Sven"]


def create_pluseen(id):
    if not os.path.exists('pluseens'):
        os.makedirs('pluseens')
    if not os.path.exists('pluseens/' + id):
        with open("pluseens/" + id, 'a') as emptyfile:
            pass
        return 'Voeg nu jouw +1 toe aan de pluseen ' + id + '!\n<br><a href="/pluseen/pluseen/'+id+'">https://m5l.nl:8080/pluseen/pluseen/'+id+'</a>'
    return "pluseen already exists lol"

def change_pluseen(id, name):
    if not os.path.exists('pluseens'):
        os.makedirs('pluseens')
    if not os.path.exists('pluseens/' + id):
        return "lol that one doesn't exist"
    addrem = ""
    if name in get_participants(id):
        addrem = "verwijderd"
        #remove the pluseen
        with open("pluseens/" + id, "r") as f:
            lines = f.readlines()
        with open("pluseens/" + id, "w") as f:
            for line in lines:
                if line.strip("\n") != name:
                    f.write(line)
    else:
        addrem = "toegevoegd"
        #add the pluseen
        with open("pluseens/" + id, "a+") as towrite:
            towrite.write(name + "\n")
    return "Je pluseen is succesvol " + addrem + "!"


def view(id):
    return get_participants(id)

def get_participants(id):
    if not os.path.exists('pluseens'):
        os.makedirs('pluseens')
    if not os.path.exists('pluseens/' + id):
        return "lol that one doesn't exist"
    result= []
    with open("pluseens/" + id) as f:
        for line in f:
            result.append(line.strip())
    return result


def get_non_participants(id):
    names = NAMES
    participants = get_participants(id)
    result = names
    for n in participants:
        if n in result:
            result.remove(n)
    return result