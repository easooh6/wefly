from src.infrastructure.celery.celery_app import celery_app
from src.infrastructure.celery.tasks import send_verification_email



if __name__ == '__main__':
    celery_app.worker_main(['worker', '--loglevel=info'])