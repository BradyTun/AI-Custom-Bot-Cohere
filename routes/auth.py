from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('list.home'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Check if email or username already exists
        existing_user = User.query.filter(
            (User.email == email) | (User.username == username)  # Check both email & username
        ).first()

        if existing_user:
            if existing_user.email == email:
                flash('Email is already registered.', 'danger')
            if existing_user.username == username:
                flash('Username is already taken.', 'danger')
            return redirect(url_for('auth.register'))  # Redirect to registration page

        # Hash password and create a new user
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(email=email, username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))
