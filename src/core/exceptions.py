class DomainException(Exception):
    """Base para erros de regra de negócio"""

    pass


class UserAlreadyExistsError(DomainException):
    """Lançado quando tenta registrar um email já existente"""

    pass


class CredentialsError(DomainException):
    """Lançado em falhas de login"""

    pass
