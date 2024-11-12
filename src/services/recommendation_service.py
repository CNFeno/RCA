# src/services/recommendation_service.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import logging
from configur.database import MariaDBConnection

class RecommendationService:
    def __init__(self):
        self.vectorizer = None
        self.svd = None
    
    def load_data_from_db(self):
        conn = MariaDBConnection.get_connection()
        if conn is None:
            raise Exception("Impossible de se connecter à la base de données")
            
        try:
            query = "SELECT Description, Plateforme, Cause, `action` FROM incident"
            cursor = conn.cursor()
            cursor.execute(query)
            
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(rows, columns=columns)
            logging.info("Données chargées avec succès.")
            
            cursor.close()
            conn.close()
            return df
        except Exception as e:
            if conn:
                conn.close()
            logging.error(f"Erreur lors du chargement des données : {e}")
            raise

    def preprocess_text(self, text):
        if pd.isna(text):
            return ""
        text = str(text).lower()
        text = ''.join(e for e in text if e.isalnum() or e.isspace())
        return text

    def prepare_data(self):
        try:
            # Charger les données
            df = self.load_data_from_db()
            
            # Prétraitement
            df['Description'] = df['Description'].apply(self.preprocess_text)
            df['Cause'] = df['Cause'].apply(self.preprocess_text)
            df['Plateforme'] = df['Plateforme'].apply(self.preprocess_text)
            df['combined'] = df['Description'] + " " + df['Cause'] + " " + df['Plateforme']
            
            # Vectorisation
            self.vectorizer = TfidfVectorizer(max_features=500)
            X = self.vectorizer.fit_transform(df['combined'])
            
            # Réduction dimensionnelle
            self.svd = TruncatedSVD(n_components=100)
            X_reduced = self.svd.fit_transform(X)
            
            return X_reduced, df
            
        except Exception as e:
            logging.error(f"Erreur lors de la préparation des données : {e}")
            raise

    def get_recommendation(self, description, plateforme):
        try:
            # Préparer les données
            X_reduced, df = self.prepare_data()
            
            # Prétraiter la nouvelle entrée
            description = self.preprocess_text(description)
            plateforme = self.preprocess_text(plateforme)
            nouvel_incident_combined = description + " " + plateforme
            
            # Vectoriser et transformer
            X_nouvel_incident = self.vectorizer.transform([nouvel_incident_combined])
            X_nouvel_incident_reduced = self.svd.transform(X_nouvel_incident)
            
            # Calculer similarités
            similarities = cosine_similarity(X_nouvel_incident_reduced, X_reduced)
            indice_similaire = similarities.argmax()
            
            return {
                'solution': df['action'].iloc[indice_similaire],
                'cause': df['Cause'].iloc[indice_similaire]
            }
            
        except Exception as e:
            logging.error(f"Erreur lors de la recommandation : {e}")
            raise