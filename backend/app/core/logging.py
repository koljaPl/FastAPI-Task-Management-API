import sys
import re
from pathlib import Path
from loguru import logger
from app.config import get_settings

settings = get_settings()

# Паттерны для скрытия чувствительных данных
SENSITIVE_PATTERNS = [
    (re.compile(r'(password["\s:=]+)([\w\S]+)', re.IGNORECASE), r'\1***'),
    (re.compile(r'(token["\s:=]+)([\w\S]+)', re.IGNORECASE), r'\1***'),
    (re.compile(r'(secret["\s:=]+)([\w\S]+)', re.IGNORECASE), r'\1***'),
    (re.compile(r'(api[_-]?key["\s:=]+)([\w\S]+)', re.IGNORECASE), r'\1***'),
    (re.compile(r'(authorization:\s*bearer\s+)([\w\S]+)', re.IGNORECASE), r'\1***'),
    (re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'), 'email@***'),
    (re.compile(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'), '****-****-****-****'),
]


def sanitize_message(record: dict) -> str:
    """Удалить чувствительные данные из сообщения"""
    message = record["message"]

    for pattern, replacement in SENSITIVE_PATTERNS:
        message = pattern.sub(replacement, message)

    return message


def format_record(record: dict) -> str:
    """
    Кастомный формат логов с санитизацией
    """
    # Санитизация сообщения
    safe_message = sanitize_message(record)

    # Базовый формат
    format_string = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    )

    # Добавить request_id если есть
    if "request_id" in record["extra"]:
        format_string += f"<yellow>req_id:{record['extra']['request_id']}</yellow> | "

    # Добавить user_id если есть
    if "user_id" in record["extra"]:
        format_string += f"<blue>user:{record['extra']['user_id']}</blue> | "

    format_string += "<level>{message}</level>\n"

    # Заменить оригинальное сообщение на санитизированное
    record["message"] = safe_message

    return format_string


def setup_logging():
    """
    Настройка логирования с Loguru
    """
    # Удалить дефолтный хендлер
    logger.remove()

    # Уровень логирования
    log_level = "DEBUG" if getattr(settings, 'DEBUG', False) else "INFO"

    # Console handler (stdout) с цветами
    logger.add(
        sys.stdout,
        format=format_record,
        level=log_level,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    # Создать директорию для логов
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # File handler - все логи
    logger.add(
        log_dir / "app.log",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
        level="DEBUG",
        rotation="100 MB",  # Ротация при достижении 100MB
        retention="30 days",  # Хранить 30 дней
        compression="zip",  # Сжимать старые логи
        serialize=False,
        backtrace=True,
        diagnose=True,
    )

    # File handler - только ошибки
    logger.add(
        log_dir / "errors.log",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
        level="ERROR",
        rotation="50 MB",
        retention="90 days",  # Ошибки хранить дольше
        compression="zip",
        serialize=False,
        backtrace=True,
        diagnose=True,
    )

    # JSON handler для продакшена (машиночитаемые логи)
    logger.add(
        log_dir / "app.json",
        format="{message}",
        level="INFO",
        rotation="100 MB",
        retention="30 days",
        compression="zip",
        serialize=True,  # JSON формат
    )

    logger.info("Logging initialized successfully")
    logger.debug(f"Log level: {log_level}")

    return logger


# Инициализация логгера при импорте
log = setup_logging()


# Вспомогательные функции для добавления контекста
def log_with_request(request_id: str):
    """Добавить request_id к логам"""
    return logger.bind(request_id=request_id)


def log_with_user(user_id: int):
    """Добавить user_id к логам"""
    return logger.bind(user_id=user_id)


def log_with_context(**kwargs):
    """Добавить произвольный контекст к логам"""
    return logger.bind(**kwargs)