# src/services/user_service.py
from datetime import datetime
from flask import flash, jsonify, redirect, session, url_for
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from models.rca_models import User, db

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session or session['user_role'] not in allowed_roles:
                flash('You do not have permission to access this page', 'danger')
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

class UserService:
    @staticmethod
    def register(data):
        hashed_password = generate_password_hash(data['password'])
        new_user = User(username=data['username'], 
                        email=data['email'],
                        password_hash=hashed_password, 
                        role=data['role'].upper())  # Assurez-vous que le rôle est en majuscules
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully', 'success')
        return redirect(url_for('users.user_list'))
    
    @staticmethod
    def update_user(user, data):
        user.username = data['username']
        user.email = data['email']
        user.role = data['role'].upper()  # Assurez-vous que le rôle est en majuscules
        
        if 'password' in data and data['password']:
            user.password_hash = generate_password_hash(data['password'])
        
        db.session.commit()
        return True 

    @staticmethod
    def login(data):
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password_hash, data['password']):
            session['user_id'] = user.id
            session['user_role'] = user.role  # Le rôle est déjà en majuscules dans la base de données
            user.last_login = datetime.utcnow()
            db.session.commit()
            flash('Logged in successfully', 'success')
            return redirect(url_for('main.index'))
        flash('Invalid credentials', 'danger')
        return redirect(url_for('auth.login'))

    @staticmethod
    def logout():
        session.pop('user_id', None)
        session.pop('user_role', None)
        flash('Logged out successfully', 'success')
        return redirect(url_for('auth.login'))