from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dtos.console_dto import ConsoleCreateInput, ConsoleOutput
from src.application.dtos.game_dto import PaginatedGameResponse
from src.application.use_cases.console_use_cases import (
    CreateConsoleUseCase,
    DeleteConsoleUseCase,
    GetConsoleByIdUseCase,
    ListConsolesUseCase,
)
from src.application.use_cases.game_use_cases import ListGamesUseCase
from src.domain.entities.user import User
from src.infra.database.config import get_db
from src.infra.repositories.console_repository import ConsoleRepository
from src.infra.repositories.game_repository import GameRepository
from src.interface.api.dependencies import get_current_admin, get_current_user
from src.interface.api.v1.schemas.response import APIResponse

router = APIRouter()


@router.post("/", response_model=APIResponse[ConsoleOutput], status_code=status.HTTP_201_CREATED)
async def create_console(
    input_data: ConsoleCreateInput, db: AsyncSession = Depends(get_db), admin_user: User = Depends(get_current_admin)
):
    repo = ConsoleRepository(db)
    use_case = CreateConsoleUseCase(repo)
    result = await use_case.execute(input_data)
    return APIResponse(success=True, data=result)


@router.get("/", response_model=APIResponse[List[ConsoleOutput]])
async def list_consoles(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = ConsoleRepository(db)
    use_case = ListConsolesUseCase(repo)
    result = await use_case.execute()
    return APIResponse(success=True, data=result)


@router.get("/{id}", response_model=APIResponse[ConsoleOutput])
async def get_console(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),  # <--- Requisito: Usuários autenticados
):
    """
    Busca um console específico pelo ID.
    """
    repo = ConsoleRepository(db)
    use_case = GetConsoleByIdUseCase(repo)

    result = await use_case.execute(id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": f"Console with id {id} not found"},
        )

    return APIResponse(success=True, data=result)


@router.delete("/{id}", response_model=APIResponse[None])
async def delete_console(id: int, db: AsyncSession = Depends(get_db), admin_user: User = Depends(get_current_admin)):
    repo = ConsoleRepository(db)
    use_case = DeleteConsoleUseCase(repo)
    await use_case.execute(id)
    return APIResponse(success=True, data=None)


@router.get("/{console_id}/games", response_model=APIResponse[PaginatedGameResponse])
async def list_games_by_console(
    console_id: int,
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Itens por página"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),  # <--- Requisito: Usuários autenticados [cite: 58]
):
    """
    Lista todos os jogos associados a um console específico.
    Requisito do PDF: GET /consoles/{console_id}/games
    """
    # 1. (Opcional) Verificar se o console existe antes
    console_repo = ConsoleRepository(db)
    console_exists = await console_repo.get_by_id(console_id)
    if not console_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": f"Console {console_id} not found"},
        )

    # 2. Reutilizar a lógica de listar jogos, forçando o filtro console_id
    game_repo = GameRepository(db)
    use_case = ListGamesUseCase(game_repo)

    # Passamos o console_id da URL para o filtro do UseCase
    result = await use_case.execute(page=page, size=size, console_id=console_id)

    return APIResponse(success=True, data=result)
