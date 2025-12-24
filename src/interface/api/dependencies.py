from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.infra.database.config import get_db
from src.infra.repositories.user_repository import UserRepository
from src.domain.entities.user import User, UserRole

# Define que o token vem da URL de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Valida o Token JWT e retorna o usuário atual.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # DEBUG: Printar o token recebido (apenas os primeiros caracteres)
        print(f"DEBUG: Token recebido: {token[:10]}...")

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        
        # DEBUG: Printar o ID extraído
        print(f"DEBUG: Payload User ID: {user_id}")

        if user_id is None:
            print("DEBUG: User ID é None")
            raise credentials_exception
            
    except JWTError as e:
        # DEBUG: Ver o erro real do JWT
        print(f"DEBUG: Erro ao decodificar JWT: {e}")
        raise credentials_exception

    repository = UserRepository(db)
    user = await repository.get_by_id(int(user_id))
    
    # DEBUG: Ver se achou no banco
    if user is None:
        print(f"DEBUG: Usuário {user_id} não encontrado no banco de dados.")
        raise credentials_exception
        
    return user

def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Valida se o usuário atual é um ADMIN (RBAC).
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user