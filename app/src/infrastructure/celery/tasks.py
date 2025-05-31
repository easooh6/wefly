from .celery_app import celery_app
from src.infrastructure.auth.email.send_email import SendEmailVerification

from src.domain.auth.dto.request.user_create import UserCreateDTO
import asyncio
import logging

logger = logging.getLogger('wefly.celery')

@celery_app.task(
    name='send_email',
    bind=True,
    max_retries=3,
    default_retry_delay=60
)
def send_verification_email(self,**data):
    logger.info('Starting email send task for: %s', data.get('email', 'unknown'))
    try:
        email_sender = SendEmailVerification()
        email_dto = UserCreateDTO(**data)
        result = asyncio.run(email_sender.send_email(email_dto))
        if result:
            logger.info('Email sent successfully to: %s', email_dto.email)  # ✅ Логирование успеха
            return {'success': result}
        else:
            logger.warning('Email sending failed to: %s', email_dto.email)  # ✅ Логирование неудачи
            raise Exception(f"Failed to send email to {email_dto.email}")

    except Exception as e:
        logger.error('Email task failed for %s: %s', data.get('email', 'unknown'), str(e))  # ✅ Детальное логирование
        
        # ✅ Проверка количества попыток
        if self.request.retries < self.max_retries:
            logger.info('Retrying email task (attempt %d/%d)', self.request.retries + 1, self.max_retries)
            raise self.retry(exc=e, countdown=60)  # Retry через 60 секунд
        else:
            logger.error('Email task permanently failed after %d attempts', self.max_retries)
            return {'success': False, 'error': str(e)}

