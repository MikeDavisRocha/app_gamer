from typing import List
from src.domain.interfaces.console_repository import IConsoleRepository
from src.domain.entities.console import Console
from src.application.dtos.console_dto import ConsoleCreateInput, ConsoleOutput
from src.core.exceptions import DomainException

class CreateConsoleUseCase:
    def __init__(self, repository: IConsoleRepository):
        self.repository = repository

    async def execute(self, input_data: ConsoleCreateInput) -> ConsoleOutput:
        # Aqui poderíamos validar se já existe um console com mesmo nome, por exemplo.
        new_console = Console(id=None, name=input_data.name, company=input_data.company)
        saved = await self.repository.create(new_console)
        return ConsoleOutput.model_validate(saved)

class ListConsolesUseCase:
    def __init__(self, repository: IConsoleRepository):
        self.repository = repository

    async def execute(self) -> List[ConsoleOutput]:
        consoles = await self.repository.list_all()
        return [ConsoleOutput.model_validate(c) for c in consoles]

class DeleteConsoleUseCase:
    def __init__(self, repository: IConsoleRepository):
        self.repository = repository

    async def execute(self, id: int) -> None:
        success = await self.repository.delete(id)
        if not success:
            raise DomainException(f"Console {id} not found")