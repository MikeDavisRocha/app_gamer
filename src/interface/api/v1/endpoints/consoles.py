from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.config import get_db
from src.interface.api.dependencies import get_current_user, get_current_admin
from src.infra.repositories.console_repository import ConsoleRepository
from src.application.use_cases.console_use_cases import (
    CreateConsoleUseCase, ListConsolesUseCase, DeleteConsoleUseCase
)
from src.application.dtos.console_dto import ConsoleCreateInput, ConsoleOutput
from src.interface.api.v1.schemas.response import APIResponse
from src.domain.entities.user import User

router = APIRouter()

@router.post("/", response_model=APIResponse[ConsoleOutput], status_code=status.HTTP_201_CREATED)
async def create_console(
    input_data: ConsoleCreateInput,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin)
):
    repo = ConsoleRepository(db)
    use_case = CreateConsoleUseCase(repo)
    result = await use_case.execute(input_data)
    return APIResponse(success=True, data=result)

@router.get("/", response_model=APIResponse[List[ConsoleOutput]])
async def list_consoles(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = ConsoleRepository(db)
    use_case = ListConsolesUseCase(repo)
    result = await use_case.execute()
    return APIResponse(success=True, data=result)

@router.delete("/{id}", response_model=APIResponse[None])
async def delete_console(
    id: int,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin)
):
    repo = ConsoleRepository(db)
    use_case = DeleteConsoleUseCase(repo)
    await use_case.execute(id)
    return APIResponse(success=True, data=None)