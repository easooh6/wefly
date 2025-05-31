from fastapi import FastAPI
from src.presentation.routers.auth.auth import router as auth_router
from src.presentation.routers.user.user_routes import router as user_router
from src.presentation.routers.search.search import router as search_router
from src.presentation.middleware.error_handler import setup_exception_handler
from slowapi import _rate_limit_exceeded_handler, Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from src.infrastructure.logging.logger_config import setup_logging
limiter = Limiter(key_func=get_remote_address)
logger = setup_logging()

# Создание экземпляра FastAPI
app = FastAPI(
    title="WeFly API",
    description="API for WeFly application",
    version="0.1.0"
)
logger.info("WeFly API application started")

app.state.limiter = limiter

setup_exception_handler(app)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Подключение роутеров
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/user", tags=["User Profile"])
app.include_router(search_router, prefix="/search", tags=["Search"])

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("WeFly API application ended")