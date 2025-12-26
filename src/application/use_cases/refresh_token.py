from datetime import timedelta

from jose import JWTError, jwt

from src.application.dtos.auth_dto import RefreshTokenInput, TokenOutput
from src.core.config import settings
from src.core.exceptions import CredentialsError
from src.core.security import create_access_token
from src.domain.interfaces.user_repository import IUserRepository


class RefreshTokenUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def execute(self, input_data: RefreshTokenInput) -> TokenOutput:
        credentials_exception = CredentialsError("Invalid refresh token")

        # 1. Tenta decodificar o Refresh Token recebido
        try:
            payload = jwt.decode(input_data.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        # 2. Garante que o usuário ainda existe no banco
        user = await self.repository.get_by_id(int(user_id))
        if not user:
            raise credentials_exception

        # 3. Rotação de Tokens (Gera um novo Access e um novo Refresh)
        # Requisito do PDF: "expiração e rotação de tokens"
        new_access_token = create_access_token(
            subject=user.id, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        new_refresh_token = create_access_token(subject=user.id, expires_delta=timedelta(days=7))

        return TokenOutput(access_token=new_access_token, refresh_token=new_refresh_token)
