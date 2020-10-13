import flask
from flask import request
import controller

app = flask.Flask(__name__)
app.config["DEBUG"] = True
NAMES = ["Anne", "Hans", "Joaz", "Joël", "Lindsay", "Michael", "Michelle", "Pim", "René", "Sven"]

@app.route("/pluseen", methods=["GET"])
def home():
    return '''
    <html>
    <body>
    <form action="/pluseen/new">
    <label for="plusname">
    <input type="text" id="plusname" name="plusname">
    <input type="submit" value="Submit">
    </body>
    </html>
    </form>
    '''

@app.route("/pluseen/new")
def new():
    id = request.args.get('plusname')
    if (str(id).isalnum()):
        result = controller.create_pluseen(id)
        return result
    return "nah"

@app.route("/pluseen/pluseen/<id>")
def pluseen(id):
    if (str(id).isalnum()):
        result = '''
        <html>
        <body>
        '''
        participants = controller.view(id)
        result = "<strong>Klik op je naam om je +1 toe te voegen of weg te halen!</strong><br><strong>+1:</strong>\n<br>"
        for p in participants:
            result += '<a href="/pluseen/pluseen/'+id+'/'+p+'">'+p + '</a><br><br>\n'
        non_participants = controller.get_non_participants(id)
        result += "<strong>Geen +1:</strong>\n<br>"
        for np in non_participants:
            result += '<a href="/pluseen/pluseen/'+id+'/'+np+'">'+np + '</a><br><br>\n'
        # result += "asdf"
        result += '''
        </body>
        </html>
        </form>
            '''
        return result
    return "nah"

@app.route("/pluseen/pluseen/<id>/<name>")
def pluseenname(id, name):
    if (str(id).isalnum()):
        result = controller.change_pluseen(id, name)
        result += '<br><a href="/pluseen/view/' + id + '">Ga terug naar de overzichtspagina</a>'
        return result
    return "nah"

@app.route("/pluseen/view/<id>")
def view(id):
    if (str(id).isalnum()):
        participants = controller.view(id)
        result = "<strong>+1:</strong>\n<br>"
        for p in participants:
            result += p + "\n<br><br>"
        non_participants = controller.get_non_participants(id)
        result += "<strong>Geen +1:</strong>\n<br>"
        for np in non_participants:
            result += np + "\n<br><br>"
        return result
    return "nah"
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)