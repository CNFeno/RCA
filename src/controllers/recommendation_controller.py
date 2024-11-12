# src/controllers/recommendation_controller.py
import logging
from flask import jsonify, request
from services.recommendation_service import RecommendationService

class RecommendationController:
    @staticmethod
    def recommander():
        try:
            description = request.form.get('incident')
            plateforme = request.form.get('platform')
            
            if not description or not plateforme:
                return jsonify({"error": "Veuillez remplir tous les champs."}), 400
                
            service = RecommendationService()
            result = service.get_recommendation(description, plateforme)
            
            return jsonify(result)
            
        except Exception as e:
            logging.error(f"Erreur dans le contrôleur de recommandation : {e}")
            return jsonify({"error": "Une erreur est survenue lors de la recommandation."}), 500