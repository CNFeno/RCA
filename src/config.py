# config.py
import os
from urllib.parse import quote_plus

class Config:
    password = quote_plus("AdmR@10ced39")  # Encoder le mot de passe pour gérer les caractères spéciaux
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://cedrix:{password}@localhost:3306/INC_DB_NEW'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'