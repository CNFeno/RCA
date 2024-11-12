# src/models/rca_models.py
from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('ADMIN', 'ANALYST', 'VIEWER'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

class IncidentSeverity(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class RCADocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_number = db.Column(db.Integer, nullable=False)
    #incident_number = db.Column(db.String(10), nullable=False, unique=True)
    customer_name = db.Column(db.String(100))
    product_name = db.Column(db.String(100))
    product_version = db.Column(db.String(50))
    incident_date = db.Column(db.Date)
    incident_time = db.Column(db.Time)
    reported_date = db.Column(db.Date)
    restored_date = db.Column(db.Date)
    rca_report_status = db.Column(db.Enum('PRELIMINARY', 'FINAL'))
    rca_submission_date = db.Column(db.DateTime, default=datetime.now)
    problem_category = db.Column(db.String(100))
    problem_sub_category = db.Column(db.String(100))
    service_impact = db.Column(db.Enum('FULL', 'PARTIAL'))
    #service_impact_duration = db.Column(db.Time)
    service_impact_duration = db.Column(db.String(50))  # Stockage sous forme de texte
    incident_impact = db.Column(db.Text)
    current_status = db.Column(db.Text)
    problem_statement = db.Column(db.Text)
    way_forward = db.Column(db.Text)
    incident_severity_id = db.Column(db.String(20), db.ForeignKey('incident_severity.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    root_causes = db.relationship('RootCause', backref='rca_document', lazy=True, cascade="all, delete-orphan")
    action_history = db.relationship('DocumentActionHistory', backref='rca_document', lazy=True, cascade="all, delete-orphan")

class RootCause(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rca_document_id = db.Column(db.Integer, db.ForeignKey('rca_document.id'))
    description = db.Column(db.Text)

class DocumentActionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rca_document_id = db.Column(db.Integer, db.ForeignKey('rca_document.id'))
    action = db.Column(db.String(100))
    performed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    action_datetime = db.Column(db.DateTime, default=datetime.now)

    # Relation vers le modèle User
    user = db.relationship('User', backref='actions')