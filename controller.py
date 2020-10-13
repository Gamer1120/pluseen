import model

def create_pluseen(id):
    return model.create_pluseen(id)


def change_pluseen(id, name):
    return model.change_pluseen(id, name)


def view(id):
    return model.get_participants(id)


def get_non_participants(id):
    return model.get_non_participants(id)