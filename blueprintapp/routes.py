from flask import Flask

from blueprintapp.models import User


def register_routes(app, db):

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return ""