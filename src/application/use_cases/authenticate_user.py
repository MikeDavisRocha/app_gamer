from datetime import timedelta

from src.application.dtos.auth_dto import LoginInput, TokenOutput
from src.core.config import settings
from src.core.exceptions import CredentialsError
from src.core.security import create_access_token, verify_password
from src.domain.interfaces.user_repository import IUserRepository


class AuthenticateUserUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def execute(self, input_data: LoginInput) -> TokenOutput:
        # 1. Busca o usuário
        user = await self.repository.get_by_email(input_data.email)

        # 2. Verifica se usuário existe e se a senha bate
        if not user or not verify_password(input_data.password, user.password_hash):
            raise CredentialsError("Email ou senha incorretos")

        # 3. Gera o Access Token (Curta duração: ex 30 min)
        access_token = create_access_token(
            subject=user.id, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        # 4. Gera o Refresh Token (Longa duração: ex 7 dias)
        # O edital pede Refresh Token[cite: 20]. Usamos a mesma função com tempo maior.
        refresh_token = create_access_token(subject=user.id, expires_delta=timedelta(days=7))

        return TokenOutput(access_token=access_token, refresh_token=refresh_token)
