from flask import Flask


def create_app():
    app = Flask(__name__)

    from urllib.parse import quote
    app.jinja_env.filters['quote'] = lambda u: quote(u)

    from pluseen import db
    app.teardown_appcontext(db.close_db)

    from pluseen import pluseen
    app.register_blueprint(pluseen.bp)

    return app
