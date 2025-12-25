from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.config import get_db
from src.interface.api.dependencies import get_current_user, get_current_admin
from src.infra.repositories.game_repository import GameRepository
from src.infra.repositories.console_repository import ConsoleRepository
from src.application.use_cases.game_use_cases import (
    CreateGameUseCase, ListGamesUseCase, DeleteGameUseCase
)
from src.application.dtos.game_dto import GameCreateInput, GameOutput, PaginatedGameResponse
from src.interface.api.v1.schemas.response import APIResponse
from src.domain.entities.user import User
from src.core.exceptions import DomainException

router = APIRouter()

@router.post("/", response_model=APIResponse[GameOutput], status_code=status.HTTP_201_CREATED)
async def create_game(
    input_data: GameCreateInput,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin) # <--- APENAS ADMIN [cite: 47]
):
    game_repo = GameRepository(db)
    console_repo = ConsoleRepository(db)
    
    use_case = CreateGameUseCase(game_repo, console_repo)
    try:
        result = await use_case.execute(input_data)
        return APIResponse(success=True, data=result)
    except DomainException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=APIResponse[PaginatedGameResponse])
async def list_games(
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Itens por página"),
    name: str = Query(None, description="Filtrar por nome do jogo"),
    console_id: int = Query(None, description="Filtrar por ID do console"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user) # <--- USUÁRIO LOGADO 
):
    repo = GameRepository(db)
    use_case = ListGamesUseCase(repo)
    result = await use_case.execute(page, size, name, console_id)
    return APIResponse(success=True, data=result)

@router.delete("/{id}", response_model=APIResponse[None])
async def delete_game(
    id: int,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin) # <--- APENAS ADMIN [cite: 60]
):
    try:
        repo = GameRepository(db)
        use_case = DeleteGameUseCase(repo)
        await use_case.execute(id)
        return APIResponse(success=True, data=None)
    except DomainException as e:
        raise HTTPException(status_code=404, detail=str(e))