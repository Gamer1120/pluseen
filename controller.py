import model_db

def create_pluseen(id):
    return model_db.create_pluseen(id)


def change_pluseen(id, name):
    return model_db.change_pluseen(id, name)


def view(id):
    return model_db.get_participants(id)


def get_non_participants(id):
    return model_db.get_non_participants(id)