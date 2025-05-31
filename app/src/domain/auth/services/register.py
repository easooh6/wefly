from src.infrastructure.celery.tasks import send_verification_email
from src.domain.auth.dto.response.created_user import CreatedUserDTO
from fastapi import Depends
from .verify_email import VerifyEmailCode
from src.infrastructure.db.repositories.user_crud import UserCRUD
from src.domain.auth.dto.request.verify_code import VerifyCodeDTO
from src.domain.auth.exceptions.exceptions_email import WrongVerificationCodeError, VerificationCodeTimeExceeded
from src.domain.auth.exceptions.exceptions_db import UserAlreadyExists
from sqlalchemy.exc import IntegrityError
from src.infrastructure.db.models.user_model import User
from src.infrastructure.redis.redis_user_store import RedisUserStore
import logging

logger = logging.getLogger('wefly.register')

class RegisterService:

    def __init__(self, email_service: VerifyEmailCode = Depends()
        , user: UserCRUD = Depends(),
        redis: RedisUserStore = Depends()):
        self.email_service = email_service
        self.user = user
        self.redis = redis
    
    async def register_user(self,verify: VerifyCodeDTO) -> CreatedUserDTO:
        logger.info('Attempt to register user %s', verify.email)
        try:
            await self.email_service.verify_code(verify)
            new_user = await self.redis.get_user_data(verify.email)
            user = User(name=new_user.name,email=new_user.email, hashed_password = new_user.password)
            result = await self.user.add_user(user)
            logger.info('User %s successfully registered', verify.email)
            return CreatedUserDTO(id=result.id, name=result.name, email=result.email,created_at=result.created_at)
        except WrongVerificationCodeError:
            raise
        except VerificationCodeTimeExceeded:
            raise
        except IntegrityError:
            raise UserAlreadyExists
            