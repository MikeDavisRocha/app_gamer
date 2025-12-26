from typing import Optional
from src.domain.interfaces.game_repository import IGameRepository
from src.domain.interfaces.console_repository import IConsoleRepository
from src.domain.entities.game import Game
from src.application.dtos.game_dto import GameCreateInput, GameOutput, PaginatedGameResponse
from src.core.exceptions import DomainException

class CreateGameUseCase:
    def __init__(self, game_repo: IGameRepository, console_repo: IConsoleRepository):
        self.game_repo = game_repo
        self.console_repo = console_repo

    async def execute(self, input_data: GameCreateInput) -> GameOutput:
        # 1. Validação de Consistência: O console existe?
        console = await self.console_repo.get_by_id(input_data.console_id)
        if not console:
            raise DomainException(f"Console ID {input_data.console_id} not found")

        # 2. Criação
        new_game = Game(id=None, name=input_data.name, console_id=input_data.console_id)
        saved_game = await self.game_repo.create(new_game)
        
        return GameOutput.model_validate(saved_game)

class ListGamesUseCase:
    def __init__(self, repository: IGameRepository):
        self.repository = repository

    async def execute(
        self, 
        page: int, 
        size: int, 
        name: Optional[str] = None, 
        console_id: Optional[int] = None
    ) -> PaginatedGameResponse:
        # 1. Cálculo do Offset (Paginação)
        skip = (page - 1) * size
        
        # 2. Busca no repositório
        games, total = await self.repository.list_with_filters(skip, size, name, console_id)
        
        # 3. Montagem da Resposta Paginada
        return PaginatedGameResponse(
            total=total,
            items=[GameOutput.model_validate(g) for g in games],
            page=page,
            size=size
        )

class DeleteGameUseCase:
    def __init__(self, repository: IGameRepository):
        self.repository = repository

    async def execute(self, id: int) -> None:
        success = await self.repository.delete(id)
        if not success:
            raise DomainException(f"Game {id} not found")

class GetGameByIdUseCase:
    def __init__(self, repository: IGameRepository):
        self.repository = repository

    async def execute(self, id: int) -> Optional[GameOutput]:
        game = await self.repository.get_by_id(id)
        if not game:
            return None
        return GameOutput.model_validate(game)