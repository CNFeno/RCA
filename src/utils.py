# utils.py
from datetime import datetime, timedelta
from flask_mail import Message
from extensions import mail, db
from models.rca_models import RootCause, RCADocument, DocumentActionHistory

def get_recurrent_root_causes(timeframe_days=30, threshold=5):
    start_date = datetime.now() - timedelta(days=timeframe_days)
    result = db.session.query(
        RootCause.description, db.func.count(RootCause.id).label('count')
    ).join(RCADocument).filter(
        RCADocument.incident_date >= start_date
    ).group_by(RootCause.description).having(db.func.count(RootCause.id) >= threshold).all()
    return result

def send_notification_email(recurrent_causes):
    for cause, count in recurrent_causes:
        message = Message(
            subject="Alerte de récurrence de cause profonde",
            recipients=["admin@example.com"],
            body=f"La cause '{cause}' est apparue {count} fois récemment. Veuillez envisager une solution permanente."
        )
        mail.send(message)

def suggest_solution_for_cause(root_cause):
    actions = db.session.query(DocumentActionHistory.action).join(RootCause).filter(
        RootCause.description == root_cause
    ).all()
    solution_counts = {}
    for action, in actions:
        solution_counts[action] = solution_counts.get(action, 0) + 1
    return max(solution_counts, key=solution_counts.get, default=None)
