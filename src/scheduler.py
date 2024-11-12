# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from utils import get_recurrent_root_causes, send_notification_email, suggest_solution_for_cause

def check_and_notify_recurrent_causes():
    recurrent_causes = get_recurrent_root_causes()
    if recurrent_causes:
        send_notification_email(recurrent_causes)
        for cause, _ in recurrent_causes:
            suggested_solution = suggest_solution_for_cause(cause)
            if suggested_solution:
                print(f"Solution suggérée pour '{cause}': {suggested_solution}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=check_and_notify_recurrent_causes, trigger="interval", days=1)
scheduler.start()
