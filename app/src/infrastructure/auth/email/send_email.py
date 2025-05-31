from src.infrastructure.auth.email.settings_smpt import settings
from email.message import EmailMessage
from aiosmtplib import SMTP
from src.domain.auth.utils.code import random_code
from contextlib import asynccontextmanager
import asyncio
from src.domain.auth.dto.request.user_create import UserCreateDTO
import logging

logger = logging.getLogger('wefly.email')

class SendEmailVerification:

    def __init__(self):
        self.host = settings.EMAIL_HOST
        self.port = settings.EMAIL_PORT
        self.host_user = settings.EMAIL_HOST_USER
        self.host_password = settings.EMAIL_HOST_PASSWORD
    
    @staticmethod
    @asynccontextmanager
    async def smtp_client_context(host, port):
        client = SMTP(hostname=host, port=port,start_tls=False)
        await client.connect()
        await client.starttls()
        yield client
        await client.quit()

    
    async def send_email(self,data: UserCreateDTO):
        try:
            async with self.smtp_client_context(self.host, self.port) as smtp_client:

                await smtp_client.login(self.host_user, self.host_password)

                message = EmailMessage()
                code = data.code
                message['From'] = self.host_user
                message['To'] = data.email
                message['Subject'] = 'Verification code'
                message.set_content(f'Your code is {code}\nFor {data.name} from WeFly ❤')

                await smtp_client.send_message(message)
                logger.info('Email sent to %s', data.email)
                return True
            
        except Exception as e:
                logger.error('an error occured during sending the verification code. error: %s',e)
                return False
