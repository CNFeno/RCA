# src/controllers/dashboard.py

from datetime import datetime, timedelta
from flask import render_template, request
import plotly.express as px
import plotly
from models.rca_models import IncidentSeverity, RCADocument, db
import pandas as pd
import json


class Dashboard:
    @staticmethod
    def parse_dates(start_date_str, end_date_str):
        """ Parse les dates du formulaire, avec des valeurs par défaut si elles sont manquantes. """
        # Par défaut, on prend les 6 derniers mois
        default_end_date = datetime.today()
        default_start_date = default_end_date - timedelta(days=180)
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else default_start_date
        except ValueError:
            start_date = default_start_date

        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else default_end_date
        except ValueError:
            end_date = default_end_date

        return start_date, end_date

    @staticmethod
    def apply_date_filter(query, model, start_date, end_date):
        """ Applique les filtres de date sur une requête SQLAlchemy """
        if start_date:
            query = query.filter(model.incident_date >= start_date)
        if end_date:
            query = query.filter(model.incident_date <= end_date)
        return query

    @staticmethod
    def serialize_plotly_figure(fig):
        """ Sérialise une figure Plotly en JSON pour être utilisée dans le template """
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    @staticmethod
    def dashboard():
        # Récupération des paramètres de date du formulaire
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        # Convertir les dates avec des valeurs par défaut
        start_date, end_date = Dashboard.parse_dates(start_date_str, end_date_str)

        # Filtrer les incidents par la plage de dates sélectionnée
        query = RCADocument.query
        query = Dashboard.apply_date_filter(query, RCADocument, start_date, end_date)

        # Statistiques générales
        total_incidents = query.count()
        open_incidents = query.filter_by(current_status='In Progress').count()

        # Incidents par sévérité avec filtre de date
        incidents_by_severity = db.session.query(
            IncidentSeverity.name,
            db.func.count(RCADocument.id)
        ).join(RCADocument)

        incidents_by_severity = Dashboard.apply_date_filter(incidents_by_severity, RCADocument, start_date, end_date)
        incidents_by_severity = incidents_by_severity.group_by(IncidentSeverity.name).all()

        # Incidents par mois avec filtre de date
        incidents_by_month = db.session.query(
            db.func.date_format(RCADocument.incident_date, '%Y-%m').label('month'),
            db.func.count(RCADocument.id)
        )
        incidents_by_month = Dashboard.apply_date_filter(incidents_by_month, RCADocument, start_date, end_date)
        incidents_by_month = incidents_by_month.group_by('month').order_by('month').all()

        # Conversion pour Plotly
        df_severity = pd.DataFrame(incidents_by_severity, columns=['Severity', 'Count'])
        fig_severity = px.pie(df_severity, values='Count', names='Severity', title='Incidents by Severity')
        graph_severity = Dashboard.serialize_plotly_figure(fig_severity)

        df_timeline = pd.DataFrame(incidents_by_month, columns=['Month', 'Count'])
        fig_timeline = px.line(df_timeline, x='Month', y='Count', title='Incident trends')
        graph_timeline = Dashboard.serialize_plotly_figure(fig_timeline)

        # Rendu du template avec les données
        return render_template('index.html',
                               total_incidents=total_incidents,
                               open_incidents=open_incidents,
                               graph_severity=graph_severity,
                               graph_timeline=graph_timeline,
                               start_date=start_date.strftime('%Y-%m-%d'),
                               end_date=end_date.strftime('%Y-%m-%d'))