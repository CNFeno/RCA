# config.py
import os
from urllib.parse import quote_plus
from flask_mail import Mail, Message

class Config:
    password = quote_plus("AdmR@10ced39")  # Encoder le mot de passe pour gérer les caractères spéciaux
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://cedrix:{password}@localhost:3306/INC_DB_NEW'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Configurations pour Flask-Mail
    MAIL_SERVER = 'localhost'              # Serveur de messagerie (Postfix local)
    MAIL_PORT = 587                        # Port SMTP pour TLS
    MAIL_USE_TLS = True                    # Activer TLS
    MAIL_USERNAME = 'noreply@omittools.mg' # Adresse de l'expéditeur
    #MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Mot de passe, stocké en variable d'environnement pour plus de sécurité
    MAIL_DEFAULT_SENDER = ('omit-tools', 'noreply@omittools.mg')  # Nom et adresse de l'expéditeur par défaut