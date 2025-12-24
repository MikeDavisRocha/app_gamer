from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.config import get_db
from src.infra.repositories.user_repository import UserRepository
from src.application.use_cases.register_user import RegisterUserUseCase
from src.application.dtos.user_dto import UserCreateInput, UserOutput
from src.interface.api.v1.schemas.response import APIResponse
from src.core.exceptions import UserAlreadyExistsError

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