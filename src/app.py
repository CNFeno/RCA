# app.py
from flask import Flask
from models.rca_models import db
from routes.blueprint import main, auth, rca, users
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(main)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(rca, url_prefix='/rca')
app.register_blueprint(users, url_prefix='/users')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)