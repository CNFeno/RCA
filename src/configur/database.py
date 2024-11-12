# src/config/database.py
import mariadb
import logging

class MariaDBConnection:
    @staticmethod
    def get_connection():
        try:
            conn = mariadb.connect(
                user="cedrix",
                password="AdmR@10ced39",
                host="localhost",
                port=3306,
                database="INC_DB"
            )
            logging.info("Connexion à la base de données réussie.")
            return conn
        except mariadb.Error as e:
            logging.error(f"Erreur lors de la connexion à MariaDB : {e}")
            return None