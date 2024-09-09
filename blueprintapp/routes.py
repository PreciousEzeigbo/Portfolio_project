from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash  # Import for checking hashed passwords

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
    
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
        
            # Retrieve user from database
            user = User.query.filter_by(username=username).first()
        
            if user and user.check_password(password):
                # User exists and password is correct
                login_user(user)
                flash('Login successful!', 'success')  # Flash message for successful login
                return redirect(url_for('/'))  # Redirect to a protected route or home page
            else:
                # Invalid credentials
                flash('Invalid username or password', 'danger')  # Flash message for login error
                return redirect(url_for('login'))  # Redirect back to login page

    @app.route('/forgotten', methods=['GET', 'POST'])
    def forgotten():
        if request.method == 'GET':
            return render_template('forgotten.html')
        elif request.method == 'POST':
            pass
    
    @app.route('/logout')
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('/'))  # Redirect to a public page
    
    @app.route('/profile') # only authenticated users can access
    @login_required
    def profile():
        return render_template('profile.html')
    
    # Custom error pages

    # Invalid pages
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404
    
    # Internal server error pages
    @app.errorhandler(500)
    def server_error(e):
        return render_template("500.html"), 500