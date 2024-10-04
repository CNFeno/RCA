from flask import render_template, request, redirect, url_for, flash, session
from sqlalchemy import desc
from models.rca_models import User, db
from services.user_service import UserService, login_required, role_required

class UserController:
    @staticmethod
    @login_required
    @role_required(['ADMIN', 'ANALYST'])
    def user_list():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        users = User.query.order_by(desc(User.created_at)).paginate(page=page, per_page=per_page, error_out=False)
        return render_template('user_manage.html', users=users, per_page=per_page)

    @staticmethod
    @login_required
    @role_required(['ADMIN'])
    def register():
        if request.method == 'POST':
            return UserService.register(request.form)
        return render_template('register.html')

    @staticmethod
    def view_user(user_id):
        user = User.query.get_or_404(user_id)
        return render_template('register.html', user=user, view_only=True)

    @staticmethod
    @login_required
    @role_required(['ADMIN'])
    def edit_user(user_id):
        user = User.query.get_or_404(user_id)
        if request.method == 'POST':
            user_data = {
                'username': request.form.get('username'),
                'email': request.form.get('email'),
                'role': request.form.get('role'),
                'password': request.form.get('password')  # Inclure le mot de passe seulement s'il est fourni
            }
            # Supprimer le mot de passe du dictionnaire s'il n'est pas fourni
            if not user_data['password']:
                del user_data['password']
            
            # Mettre à jour l'utilisateur en utilisant UserService
            UserService.update_user(user, user_data)
            flash('User updated successfully', 'success')
            return redirect(url_for('users.user_list'))
        
        return render_template('register.html', user=user, title='Edit User')

    @staticmethod
    @login_required
    @role_required(['ADMIN'])
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        #if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
        return redirect(url_for('users.user_list'))
        #return render_template('confirm_delete.html', user=user)