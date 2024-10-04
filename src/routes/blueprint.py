# src/routes/blueprint.py
from flask import Blueprint, render_template, request
from controllers.user_manage import UserController
from controllers.rca_controller import RCAController
from services.user_service import login_required, role_required, UserService

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
rca = Blueprint('rca', __name__)
users = Blueprint('users', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return UserService.login(request.form)
    return render_template('login.html')

@users.route('/users/register', methods=['GET', 'POST'])
@role_required(['ADMIN'])  # Seuls les administrateurs peuvent enregistrer de nouveaux utilisateurs
def register():
    if request.method == 'POST':
        return UserService.register(request.form)
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    return UserService.logout()

@rca.route('/rca')
@login_required
@role_required(['ADMIN', 'ANALYST', 'VIEWER'])  # Tous les rôles peuvent voir la liste des RCA
def rca_list():
    return RCAController.rca_list()

@users.route('/users')
@login_required
@role_required(['ADMIN', 'ANALYST'])
def user_list():
    return UserController.user_list()

@users.route('/users/create', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN'])
def create_user():
    return UserController.register()

@users.route('/users/<int:user_id>')
@login_required
@role_required(['ADMIN', 'ANALYST'])
def view_user(user_id):
    return UserController.view_user(user_id)

@users.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN'])
def edit_user(user_id):
    return UserController.edit_user(user_id)

@users.route('/users/<int:user_id>/delete', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN'])
def delete_user(user_id):
    return UserController.delete_user(user_id)

@rca.route('/rca/new', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN', 'ANALYST'])  # Seuls les administrateurs et les analystes peuvent créer des RCA
def create_rca():
    return RCAController.create_rca()

@rca.route('/rca/<int:rca_id>')
@login_required
@role_required(['ADMIN', 'ANALYST', 'VIEWER'])  # Tous les rôles peuvent voir un RCA spécifique
def view_rca(rca_id):
    return RCAController.view_rca(rca_id)

@rca.route('/rca/<int:rca_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN', 'ANALYST'])  # Seuls les administrateurs et les analystes peuvent éditer un RCA
def edit_rca(rca_id):
    #root_causes = rca.root_causes
    return RCAController.edit_rca(rca_id)

""" @rca.route('/rca/<int:rca_id>/root-cause', methods=['POST'])
@login_required
@role_required(['ADMIN', 'ANALYST'])  # Seuls les administrateurs et les analystes peuvent ajouter une cause racine
def add_root_cause(rca_id):
    return RCAController.add_root_cause(rca_id) """

@rca.route('/rca/<int:rca_id>/add_root_cause', methods=['POST'])
@login_required
@role_required(['ADMIN', 'ANALYST'])
def add_root_cause(rca_id):
    return RCAController.add_root_cause(rca_id)

@rca.route('/rca/root_cause/<int:root_cause_id>/delete', methods=['POST'])
@login_required
@role_required(['ADMIN', 'ANALYST'])
def delete_root_cause(root_cause_id):
    return RCAController.delete_root_cause(root_cause_id)