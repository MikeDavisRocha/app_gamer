from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dtos.game_dto import (
    GameCreateInput,
    GameOutput,
    PaginatedGameResponse,
)
from src.application.use_cases.game_use_cases import (
    CreateGameUseCase,
    DeleteGameUseCase,
    GetGameByIdUseCase,
    ListGamesUseCase,
)
from src.domain.entities.user import User
from src.infra.database.config import get_db
from src.infra.repositories.console_repository import ConsoleRepository
from src.infra.repositories.game_repository import GameRepository
from src.interface.api.dependencies import get_current_admin, get_current_user
from src.interface.api.v1.schemas.response import APIResponse

router = APIRouter()


@router.post("/", response_model=APIResponse[GameOutput], status_code=status.HTTP_201_CREATED)
async def create_game(
    input_data: GameCreateInput, db: AsyncSession = Depends(get_db), admin_user: User = Depends(get_current_admin)
):
    game_repo = GameRepository(db)
    console_repo = ConsoleRepository(db)
    use_case = CreateGameUseCase(game_repo, console_repo)
    result = await use_case.execute(input_data)
    return APIResponse(success=True, data=result)


@router.get("/", response_model=APIResponse[PaginatedGameResponse])
async def list_games(
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Itens por página"),
    name: Optional[str] = Query(None, description="Filtrar por nome"),
    console_id: Optional[int] = Query(None, description="Filtrar por console"),
    company: Optional[str] = Query(None, description="Filtrar por nome da empresa (ex: Nintendo)"),
    sort_by: Literal["name", "created_at"] = Query("name", description="Campo para ordenação"),
    sort_order: Literal["asc", "desc"] = Query("asc", description="Direção: 'asc' ou 'desc'"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Lista jogos com paginação, filtros e ordenação dinâmica.
    """
    repo = GameRepository(db)
    use_case = ListGamesUseCase(repo)

    # Passando os novos parâmetros para o Use Case
    result = await use_case.execute(
        page=page, size=size, name=name, console_id=console_id, company=company, sort_by=sort_by, sort_order=sort_order
    )

    return APIResponse(success=True, data=result)


@router.delete("/{id}", response_model=APIResponse[None])
async def delete_game(
    id: int,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin),  # <--- APENAS ADMIN [cite: 60]
):
    repo = GameRepository(db)
    use_case = DeleteGameUseCase(repo)
    await use_case.execute(id)
    return APIResponse(success=True, data=None)


@router.get("/{id}", response_model=APIResponse[GameOutput])
async def get_game(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),  # <--- Requisito: Usuários autenticados
):
    """
    Busca os detalhes de um jogo específico pelo ID.
    """
    repo = GameRepository(db)
    use_case = GetGameByIdUseCase(repo)

    result = await use_case.execute(id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": f"Game with id {id} not found"},
        )

    return APIResponse(success=True, data=result)
