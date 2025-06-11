
class TicketError(Exception):
    """Базовое исключение домена билетов"""
    pass

class TicketNotFoundError(TicketError):
    """Билет не найден"""
    pass

class TicketAlreadyExistsError(TicketError):
    """Билет уже существует"""
    pass

class InvalidTicketDataError(TicketError):
    """Некорректные данные билета"""
    pass

class TicketNotAvailableError(TicketError):
    """Билет недоступен для бронирования"""
    pass

class DatabaseConnectionError(TicketError):
    """Ошибка подключения к БД"""
    pass

class TicketRepositoryError(TicketError):
    """Общая ошибка репозитория билетов"""
    pass