class TryHardException(Exception):
    """Base exception for tryHard application"""
    pass


class AuthenticationError(TryHardException):
    """Authentication failed"""
    pass


class ValidationError(TryHardException):
    """Validation failed"""
    pass


class NotFoundError(TryHardException):
    """Resource not found"""
    pass


class PermissionError(TryHardException):
    """Permission denied"""
    pass


class RateLimitError(TryHardException):
    """Rate limit exceeded"""
    pass