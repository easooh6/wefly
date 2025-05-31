from src.domain.auth.exceptions.exceptions_db import DBServiceError, UserAlreadyExists, UserNotFound
from src.domain.auth.exceptions.exceptions_email import EmailServiceError, RateLimitExceededError, WrongVerificationCodeError, VerificationCodeTimeExceeded
from src.domain.auth.exceptions.exceptions_hash import WrongPasswordError
from src.domain.auth.exceptions.exceptions_jwt import JWTServiceError, CredentialError, ExpiredCredentialError, InvalidPayloadError, RefreshNotFoundError
from src.domain.parsing.exceptions import APIRequestError, FlightNotFoundError, InvalidAPIResponseError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, status
import logging

logger = logging.getLogger("wefly.exceptions")

def setup_exception_handler(app: FastAPI):

    # DB exceptions
    @app.exception_handler(DBServiceError)
    async def db_service_error_handler(request: Request, exc: DBServiceError):
        logger.error("Database service error: %s | URL: %s | IP: %s", str(exc), request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An unexpected error occurred. Our admins are working on it."}
        )
    
    @app.exception_handler(UserAlreadyExists)
    async def db_user_exists_error_handler(request: Request, exc: UserAlreadyExists):
        logger.warning("User already exists: %s | IP: %s", str(exc), request.client.host)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": str(exc)}
        )
    
    @app.exception_handler(UserNotFound)
    async def db_user_not_found_error_handler(request: Request, exc: UserNotFound):
        logger.warning("User not found: %s | URL: %s | IP: %s", str(exc), request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)}
        )
    
    # Email exceptions
    @app.exception_handler(EmailServiceError)
    async def email_service_error_handler(request: Request, exc: EmailServiceError):  
        logger.error("Email service error: %s | URL: %s | IP: %s", str(exc), request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An unexpected error occurred. Our admins are working on it."}
        )
    
    @app.exception_handler(RateLimitExceededError)
    async def email_limit_exceeded_error_handler(request: Request, exc: RateLimitExceededError):
        logger.warning("Rate limit exceeded: %s | IP: %s", str(exc), request.client.host)
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"message": str(exc)}
        )
    
    @app.exception_handler(WrongVerificationCodeError)
    async def email_wrong_verification_error_handler(request: Request, exc: WrongVerificationCodeError):
        logger.warning("Wrong verification code: %s | IP: %s", str(exc), request.client.host)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)}
        )
    
    @app.exception_handler(VerificationCodeTimeExceeded)
    async def email_verification_time_exceeded_error_handler(request: Request, exc: VerificationCodeTimeExceeded):
        logger.warning("Verification code expired: %s | IP: %s", str(exc), request.client.host)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)}
        )

    # Hash error
    @app.exception_handler(WrongPasswordError)
    async def hash_wrong_password_error_handler(request: Request, exc: WrongPasswordError):
        logger.warning("Wrong password attempt | IP: %s", request.client.host)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            content={"message": str(exc)}
        )

    # JWT errors
    @app.exception_handler(JWTServiceError)
    async def jwt_service_error_handler(request: Request, exc: JWTServiceError):
        logger.error("JWT service error: %s | URL: %s | IP: %s", str(exc), request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An unexpected error occurred. Our admins are working on it."}
        )
    
    @app.exception_handler(CredentialError)
    async def jwt_credential_error_handler(request: Request, exc: CredentialError):
        logger.warning("Invalid credentials: %s | URL: %s | IP: %s", str(exc), request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)}
        )
    
    @app.exception_handler(InvalidPayloadError)
    async def jwt_invalid_payload_error_handler(request: Request, exc: InvalidPayloadError):
        logger.warning("Invalid token payload: %s | URL: %s | IP: %s", str(exc), request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)}
        )
    
    @app.exception_handler(ExpiredCredentialError)
    async def jwt_expired_credential_error_handler(request: Request, exc: ExpiredCredentialError):
        logger.warning("Expired token: %s | URL: %s | IP: %s", str(exc), request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)}
        )
    
    @app.exception_handler(RefreshNotFoundError)
    async def jwt_refresh_not_found_handler(request: Request, exc: RefreshNotFoundError):
        logger.warning("Refresh token not found: %s | IP: %s", str(exc), request.client.host)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,  # ✅ Изменен на 401
            content={"message": str(exc)}
        )
    
    @app.exception_handler(APIRequestError)
    async def parsing_api_request_error_handler(request: Request, exc: APIRequestError):
        logger.error("Flight API request failed: %s | URL: %s | IP: %s", 
                    str(exc), request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "message": "Flight search service temporarily unavailable. Please try again later.",
                "error_type": "service_unavailable"
            }
        )
    
    @app.exception_handler(FlightNotFoundError)
    async def parsing_flight_not_found_error_handler(request: Request, exc: FlightNotFoundError):
        logger.info("No flights found: %s | URL: %s | IP: %s", 
                   str(exc), request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "No flights found for your search criteria",
                "error_type": "no_results",
                "suggestions": [
                    "Try different dates",
                    "Check alternative airports",
                    "Modify passenger count"
                ]
            }
        )
    
    @app.exception_handler(InvalidAPIResponseError)
    async def parsing_invalid_response_error_handler(request: Request, exc: InvalidAPIResponseError):
        logger.error("Invalid API response structure: %s | URL: %s | IP: %s", 
                    str(exc), request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={
                "message": "Flight data service returned invalid response. Our team has been notified.",
                "error_type": "data_format_error"
            }
        )
    
    # ✅ Добавьте общий обработчик
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error("Unhandled exception: %s | URL: %s %s | IP: %s", 
                    str(exc), request.method, request.url, request.client.host, 
                    exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An unexpected error occurred. Our admins are working on it."}
        )




