from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.config import get_db
from src.infra.repositories.user_repository import UserRepository
from src.application.use_cases.register_user import RegisterUserUseCase
from src.application.dtos.user_dto import UserCreateInput, UserOutput
from src.interface.api.v1.schemas.response import APIResponse
from src.core.exceptions import UserAlreadyExistsError

from src.application.use_cases.authenticate_user import AuthenticateUserUseCase
from src.application.dtos.auth_dto import LoginInput, TokenOutput
from src.core.exceptions import CredentialsError

router = APIRouter()

@router.post(
    "/register", 
    response_model=APIResponse[UserOutput], 
    status_code=status.HTTP_201_CREATED
)
async def register(
    user_input: UserCreateInput, 
    db: AsyncSession = Depends(get_db)
):
    """
    Registra um novo usuário no sistema.
    """
    try:
        # 1. Injeção de Dependência Manual
        repository = UserRepository(db)
        use_case = RegisterUserUseCase(repository)
        
        # 2. Execução
        new_user = await use_case.execute(user_input)
        
        # 3. Retorno no padrão do PDF
        return APIResponse(success=True, data=new_user)
    
    except UserAlreadyExistsError as e:
        # Tratamento básico por enquanto (será melhorado no Middleware Global na Fase 4)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "USER_EXISTS", "message": str(e)}
        )

@router.post(
    "/login",
    response_model=APIResponse[TokenOutput]
)
async def login(
    login_input: LoginInput,
    db: AsyncSession = Depends(get_db)
):
    """
    Autentica um usuário e retorna os tokens de acesso.
    """
    try:
        repository = UserRepository(db)
        use_case = AuthenticateUserUseCase(repository)
        
        token_result = await use_case.execute(login_input)
        
        return APIResponse(success=True, data=token_result)
    
    except CredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "AUTH_ERROR", "message": str(e)},
            headers={"WWW-Authenticate": "Bearer"},
        )