from flask import Flask, render_template, request, redirect, url_for, flash
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
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            # Check if the passwords match
            if password != confirm_password:
                flash("Passwords do not match", 'danger')
                return redirect(url_for('signup'))

            # Check if the username or email already exists
            user_exists = User.query.filter_by(username=username).first()
            email_exists = User.query.filter_by(email=email).first()

            if user_exists:
                flash("Username already taken", 'danger')
                return redirect(url_for('signup'))

            if email_exists:
                flash("Email already in use", 'danger')
                return redirect(url_for('signup'))

            # Hash the password
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            # Create and save the new user
            user = User(username=username, email=email, password=hashed_password)

            db.session.add(user)
            db.session.commit()

            flash("Account created successfully!", 'success')
            return redirect(url_for('login'))
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