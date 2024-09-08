from flask import Flask, render_template, request
from flask_login import login_user, logout_user, current_user, login_required

from blueprintapp.models import User


def register_routes(app, db, bcrypt):

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('home.html')
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            pass

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            pass

    @app.route('/forgotten', methods=['GET', 'POST'])
    def forgotten():
        if request.method == 'GET':
            return render_template('forgotten.html')
        elif request.method == 'POST':
            pass
    
    @app.route('/logout')
    def logout():
        logout_user()
        return 'Success'