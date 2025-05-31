import logging
from pathlib import Path

def setup_logging():
    # ✅ Создание папки logs если её нет
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger("wefly")  # ✅ Переименовать для всего приложения
    logger.setLevel(logging.DEBUG)
    
    # ✅ Проверка что handlers не дублируются
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # ✅ Путь через pathlib
    file_handler = logging.FileHandler(log_dir / "wefly.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    

    return logger 