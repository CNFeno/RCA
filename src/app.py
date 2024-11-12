# app.py
from flask import Flask
from extensions import db, mail
from models.rca_models import db
from routes.blueprint import main, auth, rca, users
from config import Config
from scheduler import scheduler

app = Flask(__name__)
app.config.from_object(Config)

# Initialisation de db et mail
db.init_app(app)
mail.init_app(app)

app.register_blueprint(main)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(rca, url_prefix='/rca')
app.register_blueprint(users, url_prefix='/users')

# Démarrage du planificateur si non démarré
if not scheduler.running:
    scheduler.start()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
