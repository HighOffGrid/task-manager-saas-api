from app.workers.tasks import send_email_task
from app.repositories import user_repo

def register_user(db, email, password):

    user = user_repo.create_user(db, email, password)

    send_email_task.delay(email)

    return user