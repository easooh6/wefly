import uvicorn
import os

if __name__ == "__main__":
    # Запуск API-сервераa
    uvicorn.run(
        "src.presentation.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,  # Только для разработки
        log_level="info"
    )