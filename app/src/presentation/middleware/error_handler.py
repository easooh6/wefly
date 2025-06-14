from src.domain.auth.exceptions.db import DBServiceError, UserAlreadyExists, UserNotFound
from src.domain.auth.exceptions.email import EmailServiceError, RateLimitExceededError, WrongVerificationCodeError, VerificationCodeTimeExceeded
from src.domain.auth.exceptions.hash import WrongPasswordError
from src.domain.auth.exceptions.jwt import JWTServiceError, CredentialError, ExpiredCredentialError, InvalidPayloadError, RefreshNotFoundError
from src.domain.parsing.exceptions import APIRequestError, FlightNotFoundError, InvalidAPIResponseError
from src.domain.ai.exceptions import ConnectionError, VoiceProcessingError, GeminiTimeoutError, GeminiUnavailableError, GeminiuUnauthorizedError
from src.domain.user.exceptions import TicketError, TicketAlreadyExistsError, TicketNotAvailableError, TicketNotFoundError, TicketRepositoryError, InvalidTicketDataError, DatabaseConnectionError
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
    
    # Parsing exceptions
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
    
    # AI Voice exceptions
    @app.exception_handler(VoiceProcessingError)
    async def voice_processing_error_handler(request: Request, exc: VoiceProcessingError):
        logger.error("Voice processing error: %s | URL: %s | IP: %s", 
                    str(exc), request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": str(exc),
                "error_type": "voice_processing_error",
                "suggestions": [
                    "Check your audio quality",
                    "Speak clearly and slowly",
                    "Use supported audio format (MP3, WAV, WEBM)",
                    "Reduce background noise"
                ]
            }
        )
    
    @app.exception_handler(GeminiuUnauthorizedError)
    async def gemini_unauthorized_error_handler(request: Request, exc: GeminiuUnauthorizedError):
        logger.error("Gemini API unauthorized: %s | URL: %s | IP: %s", 
                    str(exc), request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "message": "AI service authentication failed. Our team has been notified.",
                "error_type": "ai_service_unavailable",
                "suggestions": [
                    "Try again in a few minutes",
                    "Use regular text search instead"
                ]
            }
        )
    
    @app.exception_handler(GeminiUnavailableError)
    async def gemini_unavailable_error_handler(request: Request, exc: GeminiUnavailableError):
        logger.error("Gemini service unavailable: %s | URL: %s | IP: %s", 
                    str(exc), request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "message": "AI service temporarily unavailable. Please try again later.",
                "error_type": "ai_service_unavailable",
                "suggestions": [
                    "Try again in a few minutes",
                    "Use regular text search instead"
                ]
            }
        )
    
    @app.exception_handler(GeminiTimeoutError)
    async def gemini_timeout_error_handler(request: Request, exc: GeminiTimeoutError):
        logger.error("Gemini request timeout: %s | URL: %s | IP: %s", 
                    str(exc), request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_408_REQUEST_TIME,
            content={
                "message": "Voice processing timed out. Please try with a shorter audio file.",
                "error_type": "processing_timeout",
                "suggestions": [
                    "Record a shorter message (under 30 seconds)",
                    "Reduce file size",
                    "Try again with better internet connection"
                ]
            }
        )
    
    @app.exception_handler(ConnectionError)
    async def connection_error_handler(request: Request, exc: ConnectionError):
        logger.error("Network connection error: %s | URL: %s | IP: %s", 
                    str(exc), request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "message": "Network connection failed. Please check your internet and try again.",
                "error_type": "network_error",
                "suggestions": [
                    "Check your internet connection",
                    "Try again in a few moments",
                    "Use regular text search if the problem persists"
                ]
            }
        )
    
    #ticket error handler
    @app.exception_handler(TicketAlreadyExistsError)
    async def ticket_already_exists_error_handler(request: Request, exc: TicketAlreadyExistsError):
        logger.warning("Ticket already exists: %s | URL: %s | IP: %s", 
                    str(exc), request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message":"Ticket already exists."
            }
        )
    
    @app.exception_handler(TicketNotFoundError)
    async def ticket_not_found_error_handler(request: Request, exc: TicketAlreadyExistsError):
        logger.warning("Ticket not found for user: %s | URL: %s | IP: %s", 
                    str(exc), request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message":"Ticket not found."
            }
        )
    
    @app.exception_handler(TicketRepositoryError)
    async def ticket_common_exception_handler(request: Request, exc: TicketRepositoryError):
        logger.warning("Ticket repository error: %s | URL: %s | IP: %s", 
                    str(exc), request.url, request.client.host)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message":"An error occured during ordering ticket(s). Our admins are working on it."
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




