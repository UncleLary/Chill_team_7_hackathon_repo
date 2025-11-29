
from typing import Any
from fastapi import HTTPException


class SAASException(HTTPException):
    pass

class InternalErrorException(SAASException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(500, detail)

class UserAlreadyExistsException(SAASException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(400, detail)

class EmailAlreadyExistsException(SAASException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(400, detail)

class UserDoesntExistsException(SAASException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(404, detail)

class InvalidPasswordException(SAASException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(400, detail)

class InvalidPasswordResetTokenException(SAASException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(400, detail)

class EitherEmailOrUserIdRequiredException(SAASException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(400, detail)

class InvalidTurnstileTokenException(SAASException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(400, detail)

class InvalidInvitationTokenException(SAASException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(400, detail)

class InvalidProductException(SAASException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(400, detail)

class ConflictingProductException(SAASException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(400, detail)

class InvalidUserEntitlementException(SAASException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(400, detail)

class InsufficientEntitlementBalanceException(SAASException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(402, detail)

class WebhookParseException(SAASException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(400, detail)

class WebhookSignatureCheckException(SAASException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(401, detail)

class WebhookUserNotFoundException(SAASException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(404, detail)

class WebhookSubscriptionNotFoundException(SAASException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(404, detail)

class InvalidPromptException(SAASException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(400, detail)
