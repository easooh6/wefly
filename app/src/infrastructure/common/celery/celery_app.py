from celery import Celery
from src.infrastructure.common.redis.redis_pool import REDIS_URL

celery_app = Celery(
    "celery_worker",  
    broker=REDIS_URL,  
    backend=REDIS_URL  
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Moscow",
    enable_utc=True,
    include=[
        'src.infrastructure.auth.celery.email',
    ]
)